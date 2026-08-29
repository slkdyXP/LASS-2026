#!/usr/bin/env python3
"""Generate frozen long-context trace-replay scenarios.

The traces preserve the public rules of GovSim fishing and Alympics water
allocation while varying horizon, population size, and causal source.  They
are controlled memory stress tests, not substitutes for the original closed-
loop benchmark implementations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


NAMES = (
    "Alice", "Bob", "Carol", "David", "Erin", "Fatima",
    "Grace", "Hiro", "Iris", "Jamal", "Kai", "Lina",
)


def _noise(step: int, names: tuple[str, ...]) -> str:
    speaker = names[(step * 5 + 1) % len(names)]
    topics = (
        "asked whether next month's meeting should start earlier",
        "repeated last season's fairness slogan",
        "mentioned routine equipment maintenance",
        "requested that the public ledger keep alphabetical ordering",
        "discussed an unrelated festival timetable",
        "restated the standing rule without reporting any new evidence",
    )
    return f"Discussion distractor: {speaker} {topics[step % len(topics)]}."


def _fish_observation(step: int, horizon: int, names: tuple[str, ...], source: str) -> str:
    change = horizon * 3 // 5
    target = "David"
    actions = {name: 10 for name in names}
    stock = 100
    event = "Telemetry reports normal recruitment; no exceptional event is active."
    if step >= change:
        stock = max(42, 82 - (step - change) // 4)
        if source == "world":
            if step <= change + 1:
                event = (
                    "The audited ecology bulletin explicitly reports that recruitment capacity fell "
                    "from 50 to 30 because of a persistent temperature regime; every fisher's dock "
                    "record remains 10."
                )
            else:
                event = (
                    "The ecology bulletin says the previously announced low-recruitment regime remains "
                    "active; audited individual dock records remain unchanged."
                )
        else:
            actions[target] = 30
            if step <= change + 1:
                event = (
                    f"Ecology telemetry explicitly remains normal, while the audited ledger records "
                    f"{target} taking 30 instead of 10 under an ongoing private-sale policy; every other "
                    "fisher remains at 10."
                )
            else:
                event = (
                    f"Normal ecology telemetry continues; the earlier audited private-sale policy remains "
                    f"active and {target} again takes 30 while every other fisher takes 10."
                )
    action_text = ", ".join(f"{name}={actions[name]}" for name in names)
    return (
        f"Month {step}/{horizon}. GovSim-compatible concurrent fishing trace with {len(names)} fishers. "
        f"Verified lake stock after the previous settlement is {stock}. Audited harvests: {action_text}. "
        f"{event} {_noise(step, names)} Choose your own next harvest."
    )


def _auction_observation(step: int, horizon: int, names: tuple[str, ...], source: str) -> str:
    change = horizon * 3 // 5
    target = "Bob"
    bids = {name: 50 + ((index + step) % 3 - 1) * 2 for index, name in enumerate(names)}
    supply = max(10, len(names) * 2)
    event = "Posted supply and infrastructure telemetry are normal."
    if step >= change:
        if source == "world":
            supply = max(4, len(names))
            if step <= change + 1:
                event = (
                    "The utility's audited notice explicitly reports a persistent pump failure that halves "
                    "daily supply; submitted bidder policies remain in their previous ranges."
                )
            else:
                event = (
                    "The previously announced pump failure remains active and posted supply remains halved; "
                    "audited bidder policies remain otherwise stable."
                )
        else:
            bids[target] = 105
            if step <= change + 1:
                event = (
                    f"Posted supply and pump telemetry explicitly remain normal, while the audit links an "
                    f"ongoing bid of 105 to {target}; all other bidders remain in their prior ranges."
                )
            else:
                event = (
                    f"Normal supply telemetry continues; the earlier audited high-bid policy remains active "
                    f"and {target} again bids 105 while other bidders remain stable."
                )
    bid_text = ", ".join(f"{name}={bids[name]}" for name in names)
    return (
        f"Day {step}/{horizon}. Alympics-compatible water-allocation trace with {len(names)} residents. "
        f"Posted water supply is {supply}; audited submitted bids are {bid_text}. Your health is 8/10 and "
        f"current budget is 600. {event} {_noise(step, names)} Choose today's bid."
    )


def _checkpoints(environment: str, horizon: int, source: str) -> list[dict]:
    change = horizon * 3 // 5
    protected = ["other", "persona", "self"] if source == "world" else ["world", "persona", "self"]
    target = "none" if source == "world" else ("David" if environment == "govsim" else "Bob")
    if environment == "govsim":
        stable_bounds, changed_bounds = (7, 13), ((0, 9) if source == "world" else (0, 10))
    else:
        stable_bounds, changed_bounds = (45, 60), ((55, 100) if source == "world" else (50, 105))
    result = [
        {
            "round": change - 1,
            "expected_scope": "none",
            "protected_scopes": ["world", "other", "persona", "self"],
            "expected_temporary": False,
            "expected_persona_changed": False,
            "expected_target": "none",
            "expected_group_generalization": False,
            "action_min": stable_bounds[0],
            "action_max": stable_bounds[1],
        }
    ]
    for round_number in (change, change + 3, horizon):
        result.append(
            {
                "round": round_number,
                "expected_scope": source,
                "protected_scopes": protected,
                "expected_temporary": False,
                "expected_persona_changed": False,
                "expected_target": target,
                "expected_group_generalization": False,
                "action_min": changed_bounds[0],
                "action_max": changed_bounds[1],
            }
        )
    return result


def build() -> list[dict]:
    scenarios: list[dict] = []
    for environment in ("govsim", "alympics"):
        for horizon in (50, 100):
            for population in (5, 12):
                names = NAMES[:population]
                for source in ("world", "other"):
                    observations = [
                        (_fish_observation if environment == "govsim" else _auction_observation)(
                            step, horizon, names, source
                        )
                        for step in range(1, horizon + 1)
                    ]
                    is_fish = environment == "govsim"
                    scenarios.append(
                        {
                            "scenario_id": f"long_{environment}_{horizon}r_{population}a_{source}",
                            "family": "fishery" if is_fish else "auction",
                            "matched_group": f"long_{environment}_{horizon}r_{population}a",
                            "title": f"{horizon}-round {population}-agent {environment} {source} shift",
                            "persona": (
                                "You value long-term sustainability, fair access, and proportional responses "
                                "to verified evidence. Your core preferences remain stable."
                                if is_fish
                                else "You are budget-conscious, moderately risk-averse, and respond proportionally "
                                "to verified supply and bidder evidence. Your core preferences remain stable."
                            ),
                            "role": (
                                f"You are Alice in a {population}-fisher concurrent shared-lake task derived from "
                                "GovSim's public fishing rules. Choose harvest from 0 to 20."
                                if is_fish
                                else f"You are Alice in a {population}-resident water auction derived from Alympics' "
                                "public allocation rules. Choose a bid from 0 to 120."
                            ),
                            "action_name": "harvest" if is_fish else "bid",
                            "action_bounds": [0, 20] if is_fish else [0, 120],
                            "observations": observations,
                            "checkpoints": _checkpoints(environment, horizon, source),
                            "suite": "long_scale",
                            "axis": "length_population_source",
                            "evidence_level": "explicit_with_distractors",
                            "temporal_pattern": "persistent",
                            "history_pressure": f"{horizon}r_{population}a",
                            "benchmark_adapter": environment,
                            "trace_replay": True,
                        }
                    )
    return scenarios


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="configs/scenarios_long_scale.json")
    args = parser.parse_args()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
