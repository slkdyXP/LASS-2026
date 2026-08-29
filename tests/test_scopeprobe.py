from __future__ import annotations

import json
from pathlib import Path
import unittest

from scopeprobe.client import parse_json_object
from scopeprobe.claim_audit import audit_claims
from scopeprobe.closed_loop import run_fishery_episode
from scopeprobe.external_memory import (
    ExternalControllerConfig,
    ExternalMemoryController,
    _normalize_packet,
)
from scopeprobe.memory import (
    ABLATION_HEADINGS,
    BASELINES,
    EVIDENCE_GATED_HEADINGS,
    FOUR_COMPONENT_EXCLUSIONS,
    HSCM_HEADINGS,
    _evidence_gated_instruction,
    _hscm_instruction,
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

    def test_hscm_preserves_exactly_six_typed_roles(self) -> None:
        instruction = _hscm_instruction()
        heading_block = instruction.split("Operational semantics and rules:", 1)[0]
        self.assertEqual(len(HSCM_HEADINGS), 6)
        for heading in HSCM_HEADINGS:
            self.assertIn(heading, heading_block)

    def test_external_controller_short_gate_is_dormant(self) -> None:
        controller = ExternalMemoryController(
            persona="Remain calm and fair.",
            config=ExternalControllerConfig(long_event_threshold=8, long_char_threshold=10_000),
        )
        packet = self._controller_packet("regeneration_lower", support=True)
        for _ in range(7):
            controller.apply_packet(packet, "brief observation", {"value": 5})
        self.assertFalse(controller.long_gate_active)
        self.assertEqual(controller.consolidated_keys, [])
        self.assertEqual(controller.hypothesis_keys, [])
        self.assertIn("DORMANT", controller.render())

    def test_external_controller_gate_promotes_accumulated_evidence(self) -> None:
        controller = ExternalMemoryController(
            persona="Remain calm and fair.",
            config=ExternalControllerConfig(long_event_threshold=8, long_char_threshold=10_000),
        )
        packet = self._controller_packet("regeneration_lower", support=True)
        for _ in range(8):
            controller.apply_packet(packet, "brief observation", {"value": 5})
        self.assertTrue(controller.long_gate_active)
        self.assertEqual(controller.gate_activated_at, 8)
        self.assertIn("regeneration_lower", controller.consolidated_keys)
        self.assertEqual(controller.persona, "Remain calm and fair.")

    def test_external_controller_self_overwrite_and_episode_bound(self) -> None:
        controller = ExternalMemoryController(
            persona="Stable persona.",
            config=ExternalControllerConfig(max_episodes=6),
        )
        for index in range(9):
            packet = self._controller_packet(f"claim_{index}", support=False)
            packet["self_updates"] = [{"field": "health", "value": str(index)}]
            packet["episodes"][0]["fact"] = f"event {index}"
            controller.apply_packet(packet, f"observation {index}", {"value": index})
        self.assertEqual(controller.self_state["health"], "8")
        self.assertEqual(len(controller.episodes), 6)
        self.assertEqual(controller.persona, "Stable persona.")

    def test_external_controller_renders_exactly_six_original_headings(self) -> None:
        controller = ExternalMemoryController(persona="Stable persona.")
        rendered = controller.render()
        for heading in EVIDENCE_GATED_HEADINGS:
            self.assertEqual(rendered.splitlines().count(heading), 1)

    def test_external_controller_runner_snapshot(self) -> None:
        scenario = load_scenarios(ROOT / "configs" / "scenarios.json")[0]
        records = run_trial(MockClient(), scenario, "hscm_external_controller", repeat=0)
        self.assertEqual(len(records), len(scenario.checkpoints))
        self.assertIsNotNone(records[0]["controller_snapshot"])
        json.dumps(records[0]["controller_snapshot"])

    def test_external_controller_verifies_active_hazard_from_same_scope_episode(self) -> None:
        packet = self._controller_packet("generation", support=True)
        packet["hazard"] = {
            "status": "active",
            "scope": "world",
            "target_agent": "none",
            "description": "Generation fell",
            "verified": False,
            "persistence": "unknown",
        }
        self.assertTrue(_normalize_packet(packet)["hazard"]["verified"])

    @staticmethod
    def _controller_packet(claim_key: str, *, support: bool) -> dict:
        return {
            "self_updates": [],
            "evidence": (
                [
                    {
                        "claim_key": claim_key,
                        "scope": "world",
                        "subject": "world",
                        "claim": "Regeneration is lower.",
                        "value": "lower",
                        "evidence_role": "state",
                        "condition": "unconditional",
                        "stance": "support",
                        "explicitly_documented": False,
                        "explicitly_persistent": False,
                    }
                ]
                if support
                else []
            ),
            "episodes": [
                {
                    "actor": "world",
                    "scope": "world",
                    "condition": "unconditional",
                    "fact": "A world event occurred.",
                    "resolved": False,
                }
            ],
            "hazard": {
                "status": "none",
                "scope": "none",
                "target_agent": "none",
                "description": "none",
                "verified": False,
                "persistence": "unknown",
            },
        }

    def test_broad_scenarios_load(self) -> None:
        scenarios = load_scenarios(ROOT / "configs" / "scenarios_broad.json")
        self.assertEqual(len(scenarios), 16)
        self.assertGreaterEqual(len({x.family for x in scenarios}), 6)

    def test_inferential_scenarios_load(self) -> None:
        scenarios = load_scenarios(ROOT / "configs" / "scenarios_inferential.json")
        self.assertEqual(len(scenarios), 6)
        self.assertIn("inferential", {x.evidence_level for x in scenarios})

    def test_long_scale_scenarios_are_factorial_and_labeled_as_trace_replay(self) -> None:
        scenarios = load_scenarios(ROOT / "configs" / "scenarios_long_scale.json")
        self.assertEqual(len(scenarios), 16)
        self.assertEqual({len(item.observations) for item in scenarios}, {50, 100})
        self.assertEqual({item.benchmark_adapter for item in scenarios}, {"govsim", "alympics"})
        self.assertTrue(all(item.trace_replay for item in scenarios))
        self.assertEqual(sum(len(item.observations) for item in scenarios), 1200)


if __name__ == "__main__":
    unittest.main()
