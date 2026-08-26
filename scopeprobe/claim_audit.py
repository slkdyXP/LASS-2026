from __future__ import annotations

import json
from typing import Any

from .client import ChatClient, parse_json_object


CLAIM_AUDIT_SYSTEM = """You are a conservative forensic annotator auditing an agent memory against the complete source evidence supplied below.

An unsupported overgeneralization is a persistent or action-guiding claim that goes beyond the evidence, including an invented causal mechanism, hidden rule, numeric threshold, stable trait, group property, or lasting regime. Do not count:
- facts explicitly stated in the source evidence;
- direct arithmetic that uses the correct number of participants and stated quantities;
- a possibility clearly kept in an OPEN HYPOTHESIS and marked uncertain;
- a proportional temporary precaution tied only to a verified current hazard;
- a stable claim supported by at least two independent consistent observations.

Count a claim when the memory presents a weakly supported possibility as a fact, consolidated lesson, or action premise. A condition-specific belief about one named participant is not a group generalization. A recovered event is stale only if the memory still treats it as currently active or persistently action-guiding.

Return valid JSON only with exactly this schema:
{
  "overgeneralization_present": false,
  "unsupported_claim_count": 0,
  "invented_mechanism": false,
  "hypothesis_as_fact": false,
  "group_generalization": false,
  "stale_after_recovery": false,
  "action_relies_on_unsupported_claim": false,
  "claims": [
    {"quote": "exact short quote from memory", "type": "mechanism|trait|group|regime|threshold|stale", "support_gap": "why source evidence is insufficient"}
  ],
  "rationale": "one concise overall explanation"
}

List at most three distinct unsupported claims. Set unsupported_claim_count to the number listed. If none exist, use an empty claims list. Judge only the supplied memory, not whether the benchmark's expected label is correct."""


def audit_claims(
    client: ChatClient,
    source_observations: list[str],
    memory_snapshot: str | list[str],
    action: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    memory_text = (
        "\n\n".join(memory_snapshot) if isinstance(memory_snapshot, list) else memory_snapshot
    )
    evidence = "\n".join(
        f"E{index}: {observation}"
        for index, observation in enumerate(source_observations, start=1)
    )
    user = (
        f"COMPLETE SOURCE EVIDENCE THROUGH THIS CHECKPOINT:\n{evidence}\n\n"
        f"MEMORY TO AUDIT:\n{memory_text}\n\n"
        f"CURRENT ACTION:\n{json.dumps(action, ensure_ascii=False)}"
    )
    raw = client.complete(
        [
            {"role": "system", "content": CLAIM_AUDIT_SYSTEM},
            {"role": "user", "content": user},
        ],
        json_mode=True,
    )
    parsed = parse_json_object(raw)
    return parsed, raw
