from __future__ import annotations

import json
from pathlib import Path
import unittest

from scopeprobe.client import parse_json_object
from scopeprobe.claim_audit import audit_claims
from scopeprobe.closed_loop import run_fishery_episode
from scopeprobe.memory import (
    ABLATION_HEADINGS,
    BASELINES,
    EVIDENCE_GATED_HEADINGS,
    FOUR_COMPONENT_EXCLUSIONS,
    _evidence_gated_instruction,
)
from scopeprobe.mock import MockClient
from scopeprobe.runner import run_trial
from scopeprobe.scenarios import load_scenarios


ROOT = Path(__file__).resolve().parent.parent


class ScopeProbeTests(unittest.TestCase):
    def test_scenarios_load(self) -> None:
        scenarios = load_scenarios(ROOT / "configs" / "scenarios.json")
        self.assertEqual(len(scenarios), 7)
        self.assertGreaterEqual(sum(len(x.checkpoints) for x in scenarios), 10)

    def test_json_parser_handles_fence(self) -> None:
        self.assertEqual(parse_json_object("```json\n{\"x\": 1}\n```"), {"x": 1})

    def test_claim_audit_schema(self) -> None:
        audit, raw = audit_claims(
            MockClient(),
            ["Round 1: all participants choose 5."],
            "Observed Round 1 without adding a causal rule.",
            {"value": 5, "message": "stable", "reason": "observed"},
        )
        self.assertFalse(audit["overgeneralization_present"])
        self.assertEqual(audit["claims"], [])
        self.assertTrue(raw)

    def test_closed_loop_smoke(self) -> None:
        episode = run_fishery_episode(
            MockClient,
            baseline="evidence_gated_memory_only",
            condition="world_contamination",
            repeat=0,
            rounds=5,
        )
        self.assertEqual(len(episode["rounds"]), 5)
        self.assertIn("final_stock", episode["metrics"])

    def test_all_baselines_reach_checkpoints(self) -> None:
        scenario = load_scenarios(ROOT / "configs" / "scenarios.json")[0]
        for baseline in BASELINES:
            records = run_trial(MockClient(), scenario, baseline, repeat=0)
            self.assertEqual(len(records), len(scenario.checkpoints))
            for record in records:
                self.assertIn("scores", record)
                self.assertIn("probe", record)
                json.dumps(record)

    def test_each_ablation_removes_exactly_one_memory_heading(self) -> None:
        for baseline, removed in ABLATION_HEADINGS.items():
            instruction = _evidence_gated_instruction(removed)
            heading_block = instruction.split("Rules:", 1)[0]
            self.assertNotIn(removed, heading_block, baseline)
            for retained in EVIDENCE_GATED_HEADINGS:
                if retained != removed:
                    self.assertIn(retained, heading_block, baseline)

    def test_four_component_baseline_and_ablations(self) -> None:
        for baseline, excluded in FOUR_COMPONENT_EXCLUSIONS.items():
            instruction = _evidence_gated_instruction(excluded)
            heading_block = instruction.split("Rules:", 1)[0]
            for heading in EVIDENCE_GATED_HEADINGS:
                if heading in excluded:
                    self.assertNotIn(heading, heading_block, baseline)
                else:
                    self.assertIn(heading, heading_block, baseline)
            expected_sections = 4 if baseline == "four_component_memory" else 3
            self.assertIn(f"under the {expected_sections} headings", instruction)

    def test_broad_scenarios_load(self) -> None:
        scenarios = load_scenarios(ROOT / "configs" / "scenarios_broad.json")
        self.assertEqual(len(scenarios), 16)
        self.assertGreaterEqual(len({x.family for x in scenarios}), 6)

    def test_inferential_scenarios_load(self) -> None:
        scenarios = load_scenarios(ROOT / "configs" / "scenarios_inferential.json")
        self.assertEqual(len(scenarios), 6)
        self.assertIn("inferential", {x.evidence_level for x in scenarios})


if __name__ == "__main__":
    unittest.main()
