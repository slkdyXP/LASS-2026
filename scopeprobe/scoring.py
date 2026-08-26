from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any

from .scenarios import Checkpoint, VALID_SCOPES


def _score(value: object) -> float:
    try:
        return min(1.0, max(0.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def score_probe(probe: dict[str, Any], checkpoint: Checkpoint, action_value: float) -> dict[str, Any]:
    updates_raw = probe.get("updates", {})
    if not isinstance(updates_raw, dict):
        updates_raw = {}
    updates = {scope: _score(updates_raw.get(scope, 0.0)) for scope in VALID_SCOPES - {"none"}}
    primary = str(probe.get("primary_scope", "none")).lower()
    scope_correct = primary == checkpoint.expected_scope
    protected = [updates.get(scope, 0.0) for scope in checkpoint.protected_scopes]
    leakage = mean(protected) if protected else 0.0
    max_leakage = max(protected, default=0.0)
    if checkpoint.expected_scope == "none":
        target_strength = 1.0 - max(updates.values(), default=0.0)
    else:
        target_strength = updates.get(checkpoint.expected_scope, 0.0)
    scope_margin = target_strength - max_leakage
    persona_stable = bool(probe.get("persona_changed", False)) == checkpoint.expected_persona_changed
    entity_correct = True
    if checkpoint.expected_target is not None:
        actual_target = str(probe.get("target_agent", "none")).strip().lower()
        entity_correct = actual_target == checkpoint.expected_target.strip().lower()
    generalization_correct = True
    if checkpoint.expected_group_generalization is not None:
        generalization_correct = bool(probe.get("generalizes_to_group", False)) == checkpoint.expected_group_generalization
    temporary_correct = (
        True
        if checkpoint.expected_temporary is None
        else bool(probe.get("change_is_temporary", False)) == checkpoint.expected_temporary
    )
    action_correct = True
    if checkpoint.action_min is not None:
        action_correct = action_correct and action_value >= checkpoint.action_min
    if checkpoint.action_max is not None:
        action_correct = action_correct and action_value <= checkpoint.action_max
    composite = mean(
        [
            float(scope_correct),
            target_strength,
            1.0 - leakage,
            float(persona_stable),
            float(temporary_correct),
            float(entity_correct),
            float(generalization_correct),
            float(action_correct),
        ]
    )
    return {
        "scope_correct": scope_correct,
        "target_strength": round(target_strength, 4),
        "protected_leakage": round(leakage, 4),
        "max_protected_leakage": round(max_leakage, 4),
        "scope_margin": round(scope_margin, 4),
        "persona_stable": persona_stable,
        "temporary_correct": temporary_correct,
        "entity_correct": entity_correct,
        "generalization_correct": generalization_correct,
        "action_correct": action_correct,
        "composite": round(composite, 4),
        "normalized_updates": updates,
    }


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(record["baseline"], record["scenario_id"])].append(record)
    rows: list[dict[str, Any]] = []
    for (baseline, scenario_id), items in sorted(grouped.items()):
        rows.append(
            {
                "baseline": baseline,
                "scenario_id": scenario_id,
                "n": len(items),
                "scope_accuracy": round(mean(float(x["scores"]["scope_correct"]) for x in items), 4),
                "mean_leakage": round(mean(x["scores"]["protected_leakage"] for x in items), 4),
                "mean_scope_margin": round(mean(x["scores"]["scope_margin"] for x in items), 4),
                "action_accuracy": round(mean(float(x["scores"]["action_correct"]) for x in items), 4),
                "persona_stability": round(mean(float(x["scores"]["persona_stable"]) for x in items), 4),
                "entity_accuracy": round(mean(float(x["scores"].get("entity_correct", True)) for x in items), 4),
                "generalization_accuracy": round(mean(float(x["scores"].get("generalization_correct", True)) for x in items), 4),
                "mean_composite": round(mean(x["scores"]["composite"] for x in items), 4),
            }
        )
    baseline_rows: list[dict[str, Any]] = []
    by_baseline: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_baseline[record["baseline"]].append(record)
    for baseline, items in sorted(by_baseline.items()):
        baseline_rows.append(
            {
                "baseline": baseline,
                "n": len(items),
                "scope_accuracy": round(mean(float(x["scores"]["scope_correct"]) for x in items), 4),
                "mean_leakage": round(mean(x["scores"]["protected_leakage"] for x in items), 4),
                "action_accuracy": round(mean(float(x["scores"]["action_correct"]) for x in items), 4),
                "persona_stability": round(mean(float(x["scores"]["persona_stable"]) for x in items), 4),
                "entity_accuracy": round(mean(float(x["scores"].get("entity_correct", True)) for x in items), 4),
                "generalization_accuracy": round(mean(float(x["scores"].get("generalization_correct", True)) for x in items), 4),
                "mean_composite": round(mean(x["scores"]["composite"] for x in items), 4),
            }
        )
    dimensions: dict[str, list[dict[str, Any]]] = {}
    for dimension in ("family", "axis", "evidence_level", "temporal_pattern", "history_pressure", "matched_group"):
        buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for record in records:
            buckets[(record["baseline"], str(record.get(dimension, "unknown")))].append(record)
        dimensions[dimension] = [
            {
                "baseline": baseline,
                dimension: value,
                "n": len(items),
                "scope_accuracy": round(mean(float(x["scores"]["scope_correct"]) for x in items), 4),
                "mean_leakage": round(mean(x["scores"]["protected_leakage"] for x in items), 4),
                "entity_accuracy": round(mean(float(x["scores"].get("entity_correct", True)) for x in items), 4),
                "action_accuracy": round(mean(float(x["scores"]["action_correct"]) for x in items), 4),
            }
            for (baseline, value), items in sorted(buckets.items())
        ]
    evaluator_items = [x for x in records if isinstance(x.get("evaluator"), dict)]
    evaluator_summary = None
    if evaluator_items:
        keys = (
            "wrong_scope_claim",
            "unsupported_blame",
            "world_overgeneralization",
            "group_overgeneralization",
            "persona_drift",
            "behavioral_consequence",
        )
        evaluator_summary = {
            key: round(mean(_score(x["evaluator"].get(key, 0.0)) for x in evaluator_items), 4)
            for key in keys
        }
        evaluator_summary["n"] = len(evaluator_items)
    return {
        "n_records": len(records),
        "by_baseline": baseline_rows,
        "by_baseline_scenario": rows,
        "by_dimension": dimensions,
        "evaluator": evaluator_summary,
    }


def markdown_report(summary: dict[str, Any], errors: list[dict[str, Any]]) -> str:
    lines = [
        "# ScopeProbe diagnostic report",
        "",
        "> These are diagnostic measurements, not evidence of a causal mechanism by themselves. Inspect raw prompts and outputs before using any claim in a paper.",
        "",
        "## Overall baseline results",
        "",
        "| Baseline | n | Scope accuracy | Protected leakage ↓ | Entity accuracy | Action accuracy | Persona stability | Composite |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["by_baseline"]:
        lines.append(
            f"| {row['baseline']} | {row['n']} | {row['scope_accuracy']:.3f} | "
            f"{row['mean_leakage']:.3f} | {row['entity_accuracy']:.3f} | {row['action_accuracy']:.3f} | "
            f"{row['persona_stability']:.3f} | {row['mean_composite']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Per-scenario results",
            "",
            "| Baseline | Scenario | n | Scope acc. | Leakage ↓ | Margin ↑ | Action acc. | Composite |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary["by_baseline_scenario"]:
        lines.append(
            f"| {row['baseline']} | {row['scenario_id']} | {row['n']} | "
            f"{row['scope_accuracy']:.3f} | {row['mean_leakage']:.3f} | "
            f"{row['mean_scope_margin']:.3f} | {row['action_accuracy']:.3f} | {row['mean_composite']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Results by experimental axis",
            "",
            "| Baseline | Axis | n | Scope acc. | Leakage ↓ | Entity acc. | Action acc. |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary.get("by_dimension", {}).get("axis", []):
        lines.append(
            f"| {row['baseline']} | {row['axis']} | {row['n']} | {row['scope_accuracy']:.3f} | "
            f"{row['mean_leakage']:.3f} | {row['entity_accuracy']:.3f} | {row['action_accuracy']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation gate",
            "",
            "Support for the proposed motivation requires repeated wrong-scope updates in memory baselines, meaningful protected-scope leakage, and an association with action errors. A low score caused only by the measurement probe, ambiguous wording, or arbitrary action thresholds is not sufficient.",
            "",
            f"Failed trials: {len(errors)}",
            "",
        ]
    )
    return "\n".join(lines)
