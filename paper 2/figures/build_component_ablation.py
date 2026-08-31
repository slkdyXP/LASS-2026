#!/usr/bin/env python3
"""Plot six-section leave-one-out effects from saved held-out checkpoints."""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


CONTROL = "evidence_gated_memory_only"
VARIANTS = (
    ("ablate_stable_persona", "Persona"),
    ("ablate_current_self_state", "Self state"),
    ("ablate_consolidated_models", "Models"),
    ("ablate_open_hypotheses", "Hypotheses"),
    ("ablate_recent_observed_episodes", "Episodes"),
    ("ablate_action_policy", "Action policy"),
)


def action_range(record: dict) -> float:
    match = re.search(
        r"bounded \[(-?[\d.]+),\s*(-?[\d.]+)\]",
        record["raw"]["decision_context"],
    )
    if not match:
        raise ValueError(f"Missing action bounds for {record['scenario_id']}")
    return float(match.group(2)) - float(match.group(1))


def aggregate(path: Path) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    wanted = {CONTROL, *(name for name, _ in VARIANTS)}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record["baseline"] in wanted:
            grouped[record["baseline"]].append(record)
    if any(len(grouped[name]) != 48 for name in wanted):
        raise ValueError({name: len(grouped[name]) for name in wanted})

    def summarize(name: str) -> dict:
        records = grouped[name]
        violations = []
        for record in records:
            value = float(record["action"]["value"])
            low = record["checkpoint"].get("action_min")
            high = record["checkpoint"].get("action_max")
            distance = max(
                (float(low) - value) if low is not None else 0.0,
                (value - float(high)) if high is not None else 0.0,
                0.0,
            )
            violations.append(100.0 * distance / action_range(record))
        return {
            "scope": 100.0 * np.mean([r["scores"]["scope_correct"] for r in records]),
            "action": 100.0 * np.mean([r["scores"]["action_correct"] for r in records]),
            "violation": float(np.mean(violations)),
        }

    control = summarize(CONTROL)
    rows = []
    for name, label in VARIANTS:
        values = summarize(name)
        rows.append(
            {
                "component_removed": label,
                "n_checkpoints": 48,
                "scope_accuracy_pct": values["scope"],
                "action_accuracy_pct": values["action"],
                "mean_violation_pct": values["violation"],
                "delta_scope_pp": values["scope"] - control["scope"],
                "delta_action_pp": values["action"] - control["action"],
                "delta_violation_pp": values["violation"] - control["violation"],
            }
        )
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(rows: list[dict], output: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7,
            "axes.titlesize": 7.5,
            "xtick.labelsize": 6.2,
            "ytick.labelsize": 6.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    labels = [f"-{r['component_removed']}" for r in rows]
    action = np.array([r["delta_action_pp"] for r in rows])
    violation = np.array([r["delta_violation_pp"] for r in rows])
    y = np.arange(len(labels))
    fig, axes = plt.subplots(1, 2, figsize=(3.35, 2.40), sharey=True, layout="constrained")
    fig.set_constrained_layout_pads(w_pad=0.03, h_pad=0.03, wspace=0.10, hspace=0.02)

    configs = (
        (axes[0], action, "$\\Delta$ action acc. (pp)", (-25.5, 6.5)),
        (axes[1], violation, "$\\Delta$ violation (pp)", (-0.65, 4.35)),
    )
    for panel, (ax, values, xlabel, limits) in enumerate(configs):
        ax.axvline(0, color="#8B8B86", lw=0.7, zorder=0)
        harmful = values < 0 if panel == 0 else values > 0
        colors = ["#C65D52" if is_harmful else "#A9B3BE" for is_harmful in harmful]
        ax.barh(y, values, height=0.58, color=colors, edgecolor="white", linewidth=0.45,
                zorder=2)
        for yi, value, is_harmful in zip(y, values, harmful):
            place_right = value >= 0
            offset = 2.5 if place_right else -2.5
            align = "left" if place_right else "right"
            ax.annotate(f"{value:+.1f}", (value, yi), xytext=(offset, 0),
                        textcoords="offset points", ha=align, va="center", fontsize=5.6,
                        color="#7E332D" if is_harmful else "#4F5862")
        ax.set_xlim(*limits)
        ax.set_xlabel(xlabel)
        ax.tick_params(axis="y", length=0)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="x", color="#ECE9E3", lw=0.5)
        ax.text(-0.12, 1.06, chr(ord("a") + panel), transform=ax.transAxes,
                fontweight="bold", fontsize=8.5, va="top")
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--records",
        type=Path,
        default=Path("runs/ablation-combined-20260827/records.jsonl"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("paper 2/figures/component_ablation"),
    )
    args = parser.parse_args()
    rows = aggregate(args.records)
    write_csv(rows, args.output.with_suffix(".csv"))
    build(rows, args.output)


if __name__ == "__main__":
    main()
