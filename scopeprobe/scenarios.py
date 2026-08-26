from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


VALID_SCOPES = {"self", "other", "world", "persona", "episodic", "none"}


@dataclass(frozen=True)
class Checkpoint:
    round: int
    expected_scope: str
    protected_scopes: tuple[str, ...]
    expected_temporary: bool | None
    expected_persona_changed: bool
    expected_target: str | None = None
    expected_group_generalization: bool | None = None
    probe_question: str | None = None
    action_min: float | None = None
    action_max: float | None = None


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    family: str
    matched_group: str
    title: str
    persona: str
    role: str
    action_name: str
    action_bounds: tuple[float, float]
    observations: tuple[str, ...]
    checkpoints: tuple[Checkpoint, ...]
    suite: str = "core"
    axis: str = "source_attribution"
    evidence_level: str = "explicit"
    temporal_pattern: str = "persistent"
    history_pressure: str = "low"


def load_scenarios(path: Path) -> list[Scenario]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    scenarios: list[Scenario] = []
    seen: set[str] = set()
    for item in raw:
        scenario_id = item["scenario_id"]
        if scenario_id in seen:
            raise ValueError(f"Duplicate scenario_id: {scenario_id}")
        seen.add(scenario_id)
        checkpoints = tuple(
            Checkpoint(
                round=cp["round"],
                expected_scope=cp["expected_scope"],
                protected_scopes=tuple(cp.get("protected_scopes", [])),
                expected_temporary=cp.get("expected_temporary"),
                expected_persona_changed=cp.get("expected_persona_changed", False),
                expected_target=cp.get("expected_target"),
                expected_group_generalization=cp.get("expected_group_generalization"),
                probe_question=cp.get("probe_question"),
                action_min=cp.get("action_min"),
                action_max=cp.get("action_max"),
            )
            for cp in item["checkpoints"]
        )
        if any(cp.expected_scope not in VALID_SCOPES for cp in checkpoints):
            raise ValueError(f"Invalid scope in {scenario_id}")
        observations = tuple(item["observations"])
        if any(cp.round < 1 or cp.round > len(observations) for cp in checkpoints):
            raise ValueError(f"Checkpoint out of range in {scenario_id}")
        scenarios.append(
            Scenario(
                scenario_id=scenario_id,
                family=item["family"],
                matched_group=item["matched_group"],
                title=item["title"],
                persona=item["persona"],
                role=item["role"],
                action_name=item["action_name"],
                action_bounds=tuple(item["action_bounds"]),
                observations=observations,
                checkpoints=checkpoints,
                suite=item.get("suite", "core"),
                axis=item.get("axis", "source_attribution"),
                evidence_level=item.get("evidence_level", "explicit"),
                temporal_pattern=item.get("temporal_pattern", "persistent"),
                history_pressure=item.get("history_pressure", "low"),
            )
        )
    return scenarios


def scenario_public_dict(scenario: Scenario) -> dict[str, Any]:
    return {
        "scenario_id": scenario.scenario_id,
        "family": scenario.family,
        "matched_group": scenario.matched_group,
        "title": scenario.title,
        "persona": scenario.persona,
        "role": scenario.role,
        "action_name": scenario.action_name,
        "action_bounds": scenario.action_bounds,
        "observations": scenario.observations,
        "checkpoints": [cp.__dict__ for cp in scenario.checkpoints],
        "suite": scenario.suite,
        "axis": scenario.axis,
        "evidence_level": scenario.evidence_level,
        "temporal_pattern": scenario.temporal_pattern,
        "history_pressure": scenario.history_pressure,
    }
