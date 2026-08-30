from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any

from .client import ChatClient
from .memory import MemoryState, active_context, choose_action, commit_round, prepare_observation, probe_beliefs
from .scenarios import Checkpoint, Scenario


DOMAINS = ("fishery", "auction", "public_goods")
CONDITIONS = ("control", "other_transient", "world_transient")


@dataclass
class ConsequenceAgent:
    client: ChatClient
    state: MemoryState


def _scenario(domain: str, baseline: str) -> Scenario:
    if domain == "fishery":
        return Scenario(
            scenario_id=f"consequence_fishery_{baseline}", family="fishery", matched_group="consequence_fishery",
            title="Controlled fishery consequence chain", persona="You value long-term sustainability and fair access. You avoid overreacting to weak evidence.",
            role="You are Erin, one of five fishers sharing a regenerating lake. Choose your own harvest each round.",
            action_name="harvest", action_bounds=(0, 20), observations=(), checkpoints=(), suite="consequence",
            axis="belief_action_environment", temporal_pattern="transient_recovery", history_pressure="medium",
        )
    if domain == "auction":
        return Scenario(
            scenario_id=f"consequence_auction_{baseline}", family="auction", matched_group="consequence_auction",
            title="Controlled water-auction consequence chain", persona="You are budget-conscious, moderately risk-averse, and care about fair access to water.",
            role="You are Erin in a five-resident daily water auction. Bid for two water units while preserving health and budget.",
            action_name="bid", action_bounds=(0, 120), observations=(), checkpoints=(), suite="consequence",
            axis="belief_action_environment", temporal_pattern="transient_recovery", history_pressure="medium",
        )
    return Scenario(
        scenario_id=f"consequence_public_goods_{baseline}", family="public_goods", matched_group="consequence_public_goods",
        title="Controlled public-goods consequence chain", persona="You value reciprocity, fairness, and collective returns.",
        role="You are Erin in a five-person public project. Choose your contribution from an endowment of 20 each round.",
        action_name="contribution", action_bounds=(0, 20), observations=(), checkpoints=(), suite="consequence",
        axis="belief_action_environment", temporal_pattern="transient_recovery", history_pressure="medium",
    )


def _probe_checkpoint(round_number: int, condition: str) -> Checkpoint:
    if condition == "control":
        return Checkpoint(
            round=round_number, expected_scope="none",
            protected_scopes=("world", "other", "persona", "self"),
            expected_temporary=True, expected_persona_changed=False,
            expected_target="none", expected_group_generalization=False,
            probe_question=(
                "No exceptional disruption has occurred. Does the evidence justify any persistent "
                "belief change or exceptional response?"
            ),
        )
    if round_number == 5:
        scope = "other" if condition == "other_transient" else "episodic"
        protected = ("world", "persona", "self") if scope == "other" else ("other", "persona", "self")
        question = "What scope caused the verified one-round disruption, and does it justify only a temporary response?"
    else:
        scope = "none"
        protected = ("world", "other", "persona", "self")
        question = "The disruption was explicitly resolved and normal conditions have continued. Does it still justify any active persistent belief or ongoing exceptional response?"
    return Checkpoint(
        round=round_number, expected_scope=scope, protected_scopes=protected,
        expected_temporary=True, expected_persona_changed=False,
        expected_target="David" if condition == "other_transient" and round_number == 5 else "none",
        expected_group_generalization=False, probe_question=question,
    )


def _fish_observation(round_number: int, stock: float, previous: str, partner_target: float) -> str:
    return (
        f"Round {round_number}. WORLD STATE: verified lake stock is {stock:.1f}; normal regeneration adds 50 after harvest, capped at 100. "
        f"PREVIOUS SETTLEMENT: {previous} CURRENT PUBLIC PLANS: Alice, Bob, Carol, and David each announce {partner_target:.0f}. "
        "Choose your own harvest."
    )


def _auction_observation(round_number: int, budget: float, health: int, previous: str) -> str:
    return (
        f"Day {round_number}. SELF STATE: budget={budget:.1f}, health={health}/10, daily need=2. WORLD STATE: normal posted supply is 6 units. "
        f"PREVIOUS SETTLEMENT: {previous} CURRENT POSTED BIDS: Alice=48, Bob=45, Carol=52, David=54. Three bidders receive two units each. "
        "Choose today's bid; winners pay their own bid."
    )


def _public_observation(round_number: int, previous_action: float, previous: str) -> str:
    return (
        f"Round {round_number}. SELF STATE: endowment=20; your previous contribution={previous_action:.1f}. WORLD RULE: each participant receives 0.4 times total contribution under normal operation. "
        f"PREVIOUS SETTLEMENT: {previous} CURRENT PUBLIC PLANS: partners normally contribute 10 and use proportional reciprocity to your last observed contribution. "
        "Choose your contribution."
    )


def _late_overgeneralization(probe: dict[str, Any]) -> float:
    updates = probe.get("updates") if isinstance(probe.get("updates"), dict) else {}
    persistent = max(float(updates.get(k, 0.0) or 0.0) for k in ("self", "other", "world", "persona"))
    flags = [
        probe.get("primary_scope") not in {"none", "episodic"},
        not bool(probe.get("change_is_temporary", True)),
        bool(probe.get("generalizes_to_group", False)),
        bool(probe.get("persona_changed", False)),
    ]
    return min(1.0, 0.5 * persistent + 0.125 * sum(flags))


def run_consequence_episode(
    client: ChatClient,
    baseline: str,
    domain: str,
    condition: str,
    repeat: int,
    rounds: int = 12,
) -> dict[str, Any]:
    if domain not in DOMAINS or condition not in CONDITIONS:
        raise ValueError(f"Unsupported consequence setting: {domain}/{condition}")
    if rounds < 12:
        raise ValueError("Consequence episodes require at least 12 rounds for the frozen probes at 5, 8, and 12")
    scenario = _scenario(domain, baseline)
    agent = ConsequenceAgent(client=client, state=MemoryState(baseline=baseline))
    records: list[dict[str, Any]] = []
    probes: list[dict[str, Any]] = []
    stock, budget, health = 100.0, 600.0, 8
    previous_action = 10.0 if domain != "auction" else 50.0
    previous = "No prior settlement; no exceptional event is active."

    for round_number in range(1, rounds + 1):
        if domain == "fishery":
            partner_target = 8.0 if condition != "control" and round_number == 5 else 10.0
            observation = _fish_observation(round_number, stock, previous, partner_target)
        elif domain == "auction":
            observation = _auction_observation(round_number, budget, health, previous)
        else:
            observation = _public_observation(round_number, previous_action, previous)

        prepare_observation(client, agent.state, scenario, observation)
        context = active_context(agent.state, scenario, observation)
        action, raw = choose_action(client, context, scenario)
        commit_round(client, agent.state, scenario, observation, action)
        value = float(action["value"])

        if domain == "fishery":
            partner = {"Alice": partner_target, "Bob": partner_target, "Carol": partner_target, "David": partner_target}
            notice = "No exceptional event occurred; normal regeneration remained active."
            if round_number == 4 and condition == "other_transient":
                partner["David"] = 20.0
                notice = "David unexpectedly harvested 20 while the others stayed at 10. Regeneration telemetry remained normal; no motive or lasting policy was documented."
            shock = 0.0
            if round_number == 4 and condition == "world_transient":
                shock = 10.0
                notice = "A contamination incident killed 10 fish after normal regeneration. Water tests identified the contaminant and the source was removed after settlement; no fisher caused it."
            total = value + sum(partner.values())
            next_stock = max(0.0, min(100.0, stock - total + 50.0) - shock)
            previous = f"Audited harvests were Erin={value:.1f}, " + ", ".join(f"{k}={v:.1f}" for k, v in partner.items()) + f". {notice} Next stock={next_stock:.1f}."
            outcome = {"stock": next_stock, "group_total": total, "payoff": value}
            stock = next_stock
        elif domain == "auction":
            budget += 40.0
            bids = {"Alice": 48.0, "Bob": 45.0, "Carol": 52.0, "David": 54.0, "Erin": min(value, budget)}
            supply = 6
            notice = "No exceptional event occurred; normal supply and ordinary bid policies remained active."
            if round_number == 4 and condition == "other_transient":
                bids["Bob"] = 100.0
                notice = "Bob's public health was 2/10 and he bid 100. His next public health reading is 8/10 and his newly posted bid is back to 45. Supply telemetry did not change."
            if round_number == 4 and condition == "world_transient":
                supply = 4
                notice = "A pump outage reduced supply to 4. The repair log now reports the pump operational and the next posted supply is 6; bidder policies did not change."
            winners = [name for name, _ in sorted(bids.items(), key=lambda x: (-x[1], x[0]))[: supply // 2]]
            won = "Erin" in winners
            if won:
                budget -= bids["Erin"]
                health = min(10, health + 2)
            else:
                health -= 1
            previous = f"Supply={supply}; bids=" + ", ".join(f"{k}={v:.1f}" for k, v in bids.items()) + f"; winners={','.join(winners)}. {notice}"
            outcome = {"budget": budget, "health": health, "won": won, "premium": max(0.0, value - 54.0)}
        else:
            partner_level = 10.0 if round_number <= 4 else max(5.0, min(10.0, previous_action))
            contributions = {"Alice": partner_level, "Bob": partner_level, "Carol": partner_level, "David": partner_level, "Erin": value}
            multiplier = 0.4
            notice = "No exceptional event occurred; the normal project multiplier remained active."
            if round_number == 4 and condition == "other_transient":
                contributions["David"] = 0.0
                notice = "David unexpectedly contributed 0 while the other partners contributed 10. His next public plan returns to 10; the project multiplier did not change."
            if round_number == 4 and condition == "world_transient":
                multiplier = 0.15
                notice = "An equipment failure reduced the multiplier to 0.15. The repair log now reports normal operation and the next posted multiplier is 0.40; participant policies did not change."
            total = sum(contributions.values())
            public_return = multiplier * total
            payoff = 20.0 - value + public_return
            group_welfare = 5 * 20.0 + (5 * multiplier - 1.0) * total
            previous = "Contributions=" + ", ".join(f"{k}={v:.1f}" for k, v in contributions.items()) + f"; multiplier={multiplier:.2f}; return/person={public_return:.1f}. {notice}"
            outcome = {"total_contribution": total, "group_welfare": group_welfare, "payoff": payoff, "partner_level": partner_level}
        previous_action = value

        if round_number in (5, 8, 12):
            cp = _probe_checkpoint(round_number, condition)
            probe, probe_raw, probe_context = probe_beliefs(client, agent.state, scenario, observation, action, cp)
            probes.append({"round": round_number, "probe": probe, "raw": probe_raw, "context": probe_context})
        records.append({
            "round": round_number, "observation": observation, "action": action, "action_raw": raw,
            "outcome": outcome, "previous_settlement": previous,
            "memory_snapshot": (
                list(agent.state.transcript)
                if baseline in {"full_history", "recent_window", "retrieval"}
                else agent.state.compressed
            ),
            "controller_snapshot": (
                agent.state.external_controller.audit_snapshot()
                if agent.state.external_controller is not None else None
            ),
        })

    actions = [float(x["action"]["value"]) for x in records]
    pre = mean(actions[:3])
    post = actions[4:]
    late_probe = probes[-1]["probe"]
    metrics: dict[str, Any] = {
        "pre_action_mean": pre,
        "post_absolute_deviation": mean(abs(x - pre) for x in post),
        "persistent_action_deviation": mean(abs(x - pre) for x in actions[-3:]),
        "late_overgeneralization": _late_overgeneralization(late_probe),
        "late_primary_scope": late_probe.get("primary_scope"),
        "late_group_generalization": bool(late_probe.get("generalizes_to_group", False)),
        "persona_changed": bool(late_probe.get("persona_changed", False)),
        "late_scope_error": late_probe.get("primary_scope") not in {"none", "episodic"},
    }
    if domain == "fishery":
        metrics.update({
            "minimum_stock": min(x["outcome"]["stock"] for x in records),
            "final_stock": records[-1]["outcome"]["stock"],
            "total_harvest": sum(x["outcome"]["group_total"] for x in records),
            "overharvest_rounds": sum(actions[i] > pre + 2 for i in range(4, rounds)),
            "overcautious_rounds": sum(actions[i] < pre - 2 for i in range(4, rounds)),
            "post_recovery_focal_harvest": sum(actions[4:]),
            "post_recovery_stock_deficit": mean(100.0 - x["outcome"]["stock"] for x in records[4:]),
        })
    elif domain == "auction":
        metrics.update({
            "final_budget": budget, "final_health": health, "survived": health > 0,
            "cumulative_bid_premium": sum(x["outcome"]["premium"] for x in records),
            "overbid_rounds": sum(actions[i] > pre + 15 for i in range(4, rounds)),
            "post_recovery_bid_expenditure": sum(
                actions[i] if records[i]["outcome"]["won"] else 0.0 for i in range(4, rounds)
            ),
            "post_recovery_health_loss": max(0, records[3]["outcome"]["health"] - health),
        })
    else:
        metrics.update({
            "cumulative_group_welfare": sum(x["outcome"]["group_welfare"] for x in records),
            "final_partner_contribution": records[-1]["outcome"]["partner_level"],
            "retaliation_rounds": sum(actions[i] < pre - 3 for i in range(4, rounds)),
            "cumulative_contribution": sum(x["outcome"]["total_contribution"] for x in records),
            "post_recovery_group_welfare": sum(x["outcome"]["group_welfare"] for x in records[4:]),
            "post_recovery_focal_payoff": sum(x["outcome"]["payoff"] for x in records[4:]),
        })
    return {
        "baseline": baseline, "domain": domain, "condition": condition, "repeat": repeat,
        "rounds": records, "probes": probes, "metrics": metrics,
    }


def summarize_consequence_episodes(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in episodes:
        grouped.setdefault(item["baseline"], []).append(item)
    result: dict[str, Any] = {"episodes": len(episodes), "baselines": {}}
    for baseline, items in sorted(grouped.items()):
        numeric_keys = sorted(set.intersection(*[
            {k for k, v in x["metrics"].items() if isinstance(v, (int, float, bool))}
            for x in items
        ]))
        result["baselines"][baseline] = {
            "n": len(items),
            "metrics": {key: mean(float(x["metrics"][key]) for x in items) for key in numeric_keys},
            "by_domain_condition": {
                f"{domain}/{condition}": {
                    key: mean(float(x["metrics"][key]) for x in items if x["domain"] == domain and x["condition"] == condition)
                    for key in numeric_keys
                }
                for domain in DOMAINS for condition in CONDITIONS
                if any(x["domain"] == domain and x["condition"] == condition for x in items)
            },
        }
    return result


def consequence_markdown_report(summary: dict[str, Any], errors: list[dict[str, Any]]) -> str:
    lines = [
        "# Controlled consequence-chain experiment",
        "",
        "> Real-model evidence only when `dry_run` is false. Control-adjusted effects must be computed "
        "from a complete, balanced matrix; raw component metrics are retained in `episodes.jsonl`.",
        "",
        f"- Successful episodes: {summary.get('episodes', 0)}",
        f"- Failed episodes: {len(errors)}",
        "",
    ]
    for baseline, item in summary.get("baselines", {}).items():
        lines.extend([f"## {baseline}", "", f"n = {item['n']}", ""])
        for key, value in item.get("metrics", {}).items():
            lines.append(f"- {key}: {value:.4f}")
        lines.append("")
    if errors:
        lines.extend(["## Errors", ""])
        for error in errors:
            lines.append(
                f"- {error.get('domain')}/{error.get('condition')}/{error.get('baseline')} "
                f"repeat {error.get('repeat')}: {error.get('error_type')}: {error.get('error')}"
            )
    return "\n".join(lines) + "\n"
