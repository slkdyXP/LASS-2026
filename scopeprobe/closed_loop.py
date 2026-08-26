from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable, Any

from .client import ChatClient
from .memory import MemoryState, active_context, choose_action, commit_round
from .scenarios import Scenario


AGENT_NAMES = ("Alice", "Bob", "Carol", "David", "Erin")
VALID_CONDITIONS = ("other_emergency", "world_contamination")


@dataclass
class FishAgent:
    name: str
    client: ChatClient
    state: MemoryState


def _scenario(name: str, baseline: str) -> Scenario:
    return Scenario(
        scenario_id=f"closed_loop_fish_{baseline}_{name}",
        family="fishery",
        matched_group="closed_loop_shock",
        title="Closed-loop shared fishery",
        persona=(
            "You value long-term sustainability, fair access, and proportionate responses to verified "
            "evidence. You avoid punishing unrelated partners for one participant's conditional behavior."
        ),
        role=(
            f"You are {name}, one of five fishers sharing a lake. Your harvest changes the common stock. "
            "Choose only your own harvest each round."
        ),
        action_name="harvest",
        action_bounds=(0, 20),
        observations=(),
        checkpoints=(),
        suite="closed_loop",
        axis="behavioral_consequence",
        evidence_level="explicit",
        temporal_pattern="recovery",
        history_pressure="medium",
    )


def run_fishery_episode(
    client_factory: Callable[[], ChatClient],
    baseline: str,
    condition: str,
    repeat: int,
    rounds: int = 7,
) -> dict[str, Any]:
    if condition not in VALID_CONDITIONS:
        raise ValueError(f"Unknown condition: {condition}")
    agents = {
        name: FishAgent(name=name, client=client_factory(), state=MemoryState(baseline=baseline))
        for name in AGENT_NAMES
    }
    scenarios = {name: _scenario(name, baseline) for name in AGENT_NAMES}
    stock = 100.0
    previous_outcome = "No prior round has occurred."
    records: list[dict[str, Any]] = []

    for round_number in range(1, rounds + 1):
        observation = (
            f"Round {round_number}. Current verified lake stock is {stock:.1f}. "
            f"Previous verified outcome: {previous_outcome} "
            "Under normal conditions, regeneration adds 50 fish after harvest, capped at stock 100. "
            "Choose your harvest for this round."
        )

        def act(name: str):
            agent = agents[name]
            scenario = scenarios[name]
            context = active_context(agent.state, scenario, observation)
            action, raw = choose_action(agent.client, context, scenario)
            return name, action, raw, context

        with ThreadPoolExecutor(max_workers=len(AGENT_NAMES)) as pool:
            decisions = dict()
            for name, action, raw, context in pool.map(act, AGENT_NAMES):
                decisions[name] = {"action": action, "raw": raw, "context": context}

        def remember(name: str):
            agent = agents[name]
            commit_round(
                agent.client,
                agent.state,
                scenarios[name],
                observation,
                decisions[name]["action"],
            )

        with ThreadPoolExecutor(max_workers=len(AGENT_NAMES)) as pool:
            list(pool.map(remember, AGENT_NAMES))

        chosen = {name: float(decisions[name]["action"]["value"]) for name in AGENT_NAMES}
        realized = dict(chosen)
        event = "No exceptional event occurred."
        if round_number == 4 and condition == "other_emergency":
            realized["David"] = 20.0
            event = (
                "David's verified emergency permit caused his realized harvest to be 20 for this round only; "
                "the permit expired at round end. Normal regeneration remained unchanged."
            )
        shock_loss = 0.0
        if round_number == 4 and condition == "world_contamination":
            shock_loss = 10.0
            event = (
                "A verified one-round contamination killed 10 fish after normal regeneration; authorities "
                "reported it cleared at round end. No fisher caused the contamination."
            )
        total_harvest = sum(realized.values())
        next_stock = min(100.0, max(0.0, stock - total_harvest) + 50.0)
        next_stock = max(0.0, next_stock - shock_loss)
        action_text = ", ".join(f"{name}={realized[name]:.1f}" for name in AGENT_NAMES)
        previous_outcome = (
            f"Round {round_number} realized harvests were {action_text}; total harvest={total_harvest:.1f}. "
            f"{event} Next stock became {next_stock:.1f}."
        )
        records.append(
            {
                "round": round_number,
                "stock_before": stock,
                "chosen_harvests": chosen,
                "realized_harvests": realized,
                "total_harvest": total_harvest,
                "event": event,
                "stock_after": next_stock,
                "messages": {name: decisions[name]["action"]["message"] for name in AGENT_NAMES},
                "reasons": {name: decisions[name]["action"]["reason"] for name in AGENT_NAMES},
                "memory_snapshots": {
                    name: agents[name].state.compressed
                    if isinstance(agents[name].state.compressed, str)
                    else str(agents[name].state.compressed)
                    for name in AGENT_NAMES
                },
            }
        )
        stock = next_stock

    non_david = tuple(name for name in AGENT_NAMES if name != "David")
    pre = sum(
        records[index]["realized_harvests"][name]
        for index in range(min(3, len(records)))
        for name in non_david
    ) / (min(3, len(records)) * len(non_david))
    response = (
        sum(records[4]["realized_harvests"][name] for name in non_david) / len(non_david)
        if len(records) >= 5
        else None
    )
    recovery = (
        sum(records[-1]["realized_harvests"][name] for name in non_david) / len(non_david)
    )
    return {
        "baseline": baseline,
        "condition": condition,
        "repeat": repeat,
        "rounds": records,
        "metrics": {
            "pre_event_non_david_mean": pre,
            "first_response_non_david_mean": response,
            "final_non_david_mean": recovery,
            "final_recovery_gap": abs(recovery - pre),
            "minimum_stock": min(item["stock_after"] for item in records),
            "final_stock": records[-1]["stock_after"],
            "total_group_harvest": sum(item["total_harvest"] for item in records),
        },
    }
