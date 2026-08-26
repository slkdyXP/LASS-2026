from __future__ import annotations

import json
from typing import Any

from .client import ChatClient, parse_json_object
from .scenarios import Checkpoint, Scenario


EVALUATOR_SYSTEM = """You are a conservative evaluator of a social simulation agent. The experimental ground truth is supplied only for evaluation; do not reinterpret it. Assess whether the agent's persistent memory, belief report, or action contains cross-scope contamination.
Return JSON only:
{
  "wrong_scope_claim": 0.0,
  "unsupported_blame": 0.0,
  "world_overgeneralization": 0.0,
  "group_overgeneralization": 0.0,
  "persona_drift": 0.0,
  "behavioral_consequence": 0.0,
  "evidence_quote": "exact short quote or none",
  "rationale": "one sentence"
}
Scores range from 0 (absent) to 1 (clear). Do not mark a strategy adjustment as persona drift. Do not penalize uncertainty when the evidence is genuinely incomplete."""


def evaluate_checkpoint(
    client: ChatClient,
    scenario: Scenario,
    checkpoint: Checkpoint,
    memory_snapshot: object,
    probe: dict[str, Any],
    action: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    truth = {
        "expected_scope": checkpoint.expected_scope,
        "protected_scopes": checkpoint.protected_scopes,
        "expected_target": checkpoint.expected_target,
        "expected_group_generalization": checkpoint.expected_group_generalization,
        "expected_temporary": checkpoint.expected_temporary,
        "expected_persona_changed": checkpoint.expected_persona_changed,
    }
    user = json.dumps(
        {
            "scenario": scenario.title,
            "persona": scenario.persona,
            "ground_truth": truth,
            "persistent_memory": memory_snapshot,
            "belief_probe": probe,
            "action": action,
        },
        ensure_ascii=False,
    )
    raw = client.complete(
        [{"role": "system", "content": EVALUATOR_SYSTEM}, {"role": "user", "content": user}],
        json_mode=True,
    )
    return parse_json_object(raw), raw

