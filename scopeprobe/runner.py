from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from .client import ChatClient
from .evaluator import evaluate_checkpoint
from .memory import (
    COMPRESSED_BASELINES,
    MemoryState,
    active_context,
    choose_action,
    commit_round,
    prepare_observation,
    probe_beliefs,
)
from .scenarios import Scenario
from .scoring import score_probe


def run_trial(
    client: ChatClient,
    scenario: Scenario,
    baseline: str,
    repeat: int,
    evaluator_client: ChatClient | None = None,
) -> list[dict[str, Any]]:
    state = MemoryState(baseline=baseline)
    checkpoints = {cp.round: cp for cp in scenario.checkpoints}
    records: list[dict[str, Any]] = []
    for round_number, observation in enumerate(scenario.observations, start=1):
        prepare_observation(client, state, scenario, observation)
        decision_context = active_context(state, scenario, observation)
        action, action_raw = choose_action(client, decision_context, scenario)
        commit_round(client, state, scenario, observation, action)
        checkpoint = checkpoints.get(round_number)
        if checkpoint is None:
            continue
        probe, probe_raw, probe_context = probe_beliefs(
            client, state, scenario, observation, action, checkpoint
        )
        scores = score_probe(probe, checkpoint, float(action["value"]))
        memory_snapshot = (
            list(state.transcript)
            if baseline not in COMPRESSED_BASELINES and baseline != "direct"
            else state.compressed
        )
        evaluator, evaluator_raw = (None, None)
        if evaluator_client is not None:
            evaluator, evaluator_raw = evaluate_checkpoint(
                evaluator_client,
                scenario,
                checkpoint,
                memory_snapshot,
                probe,
                action,
            )
        records.append(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "scenario_id": scenario.scenario_id,
                "family": scenario.family,
                "matched_group": scenario.matched_group,
                "suite": scenario.suite,
                "axis": scenario.axis,
                "evidence_level": scenario.evidence_level,
                "temporal_pattern": scenario.temporal_pattern,
                "history_pressure": scenario.history_pressure,
                "baseline": baseline,
                "repeat": repeat,
                "round": round_number,
                "checkpoint": asdict(checkpoint),
                "observation": observation,
                "action": action,
                "probe": probe,
                "scores": scores,
                "memory_snapshot": memory_snapshot,
                "controller_snapshot": (
                    state.external_controller.audit_snapshot()
                    if state.external_controller is not None
                    else None
                ),
                "evaluator": evaluator,
                "raw": {
                    "decision_context": decision_context,
                    "action_response": action_raw,
                    "probe_context": probe_context,
                    "probe_response": probe_raw,
                    "evaluator_response": evaluator_raw,
                },
            }
        )
    return records
