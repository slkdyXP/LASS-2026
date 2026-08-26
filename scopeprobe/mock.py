from __future__ import annotations

import json
import re


class MockClient:
    """Deterministic client for plumbing tests only; never use its output as evidence."""

    def complete(self, messages: list[dict[str, str]], *, json_mode: bool = False) -> str:
        system = messages[0]["content"]
        user = messages[-1]["content"]
        if "reporting the participant's current beliefs" in system:
            lowered = user.lower()
            if "own daily need" in lowered or "raises your own daily need" in lowered:
                scope = "self"
            elif "david" in lowered and ("32" in lowered or "takes 20" in lowered):
                scope = "other"
            elif "bob" in lowered and "health" in lowered:
                scope = "other"
            elif "contamination" in lowered:
                scope = "episodic"
            elif "regeneration" in lowered or "supply" in lowered:
                scope = "world"
            else:
                scope = "none"
            updates = {name: 0.05 for name in ("self", "other", "world", "persona", "episodic")}
            if scope != "none":
                updates[scope] = 0.85
            return json.dumps(
                {
                    "primary_scope": scope,
                    "updates": updates,
                    "target_agent": "David" if "david" in lowered else "none",
                    "generalizes_to_group": False,
                    "change_is_temporary": "temporary" in lowered or "contamination" in lowered or "health" in lowered,
                    "persona_changed": False,
                    "confidence": 0.8,
                    "rationale": "Mock diagnostic response.",
                }
            )
        if "conservative evaluator" in system:
            return json.dumps(
                {
                    "wrong_scope_claim": 0.1,
                    "unsupported_blame": 0.0,
                    "world_overgeneralization": 0.0,
                    "group_overgeneralization": 0.0,
                    "persona_drift": 0.0,
                    "behavioral_consequence": 0.0,
                    "evidence_quote": "none",
                    "rationale": "Mock evaluator response.",
                }
            )
        if "conservative forensic annotator" in system:
            return json.dumps(
                {
                    "overgeneralization_present": False,
                    "unsupported_claim_count": 0,
                    "invented_mechanism": False,
                    "hypothesis_as_fact": False,
                    "group_generalization": False,
                    "stale_after_recovery": False,
                    "action_relies_on_unsupported_claim": False,
                    "claims": [],
                    "rationale": "Mock claim audit response.",
                }
            )
        if "Return valid JSON only" in system:
            match = re.search(r"bounded \[(-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?)\]", user)
            if not match:
                raise ValueError("Mock could not locate action bounds")
            low, high = float(match.group(1)), float(match.group(2))
            value = (low + high) / 2
            return json.dumps({"value": value, "message": "Proceed cautiously.", "reason": "Mock action."})
        return (user[-1200:] if len(user) > 1200 else user).replace("Output only the updated memory text.", "")
