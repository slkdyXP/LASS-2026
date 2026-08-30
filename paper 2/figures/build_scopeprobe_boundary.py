#!/usr/bin/env python3
"""Build Figure 2 from the frozen ScopeProbe confirmation records.

The plot is intentionally descriptive. Cells aggregate registered checkpoints
within evidence categories and do not treat checkpoints as independent samples.
No values are simulated or imputed.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


METHODS = ("full_history", "summary", "reflection")
METHOD_LABELS = {
    "full_history": "Full History",
    "summary": "Summary",
    "reflection": "Reflection",
}

CATEGORY_SCENARIOS = {
    "Persistent\nworld": {
        "fish_world_regime",
        "long_history_late_world_shift",
        "public_goods_world_multiplier",
        "traffic_world_lane_closure",
    },
    "Named\nother": {
        "epidemic_other_violation",
        "fish_other_shift",
        "grid_bob_overuse",
        "public_goods_david_free_rider",
    },
    "Conditional\nother": {"auction_bob_conditional"},
    "Self-state\nchange": {
        "auction_self_need_shift",
        "team_self_capability_drop",
    },
    "Recovered": {"fish_world_anomaly_recovery"},
    "Negative\ncontrol": {
        "entity_binding_bob_not_david",
        "salience_other_storm_named",
    },
}


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def category_for(scenario_id: str) -> str:
    hits = [name for name, ids in CATEGORY_SCENARIOS.items() if scenario_id in ids]
    if len(hits) != 1:
        raise ValueError(f"Scenario must map to exactly one category: {scenario_id!r} -> {hits}")
    return hits[0]


def aggregate(records: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    observed_scenarios: set[str] = set()
    for record in records:
        method = record["baseline"]
        if method not in METHODS:
            continue
        scenario_id = record["scenario_id"]
        observed_scenarios.add(scenario_id)
        grouped[(method, category_for(scenario_id))].append(record)

    registered = set().union(*CATEGORY_SCENARIOS.values())
    if observed_scenarios != registered:
        missing = sorted(registered - observed_scenarios)
        extra = sorted(observed_scenarios - registered)
        raise ValueError(f"Unexpected confirmation coverage; missing={missing}, extra={extra}")

    rows: list[dict] = []
    for category in CATEGORY_SCENARIOS:
        for method in METHODS:
            items = grouped[(method, category)]
            if not items:
                raise ValueError(f"No records for {method}/{category}")
            errors = sum(not bool(x["scores"]["scope_correct"]) for x in items)
            leakage = float(np.mean([x["scores"]["protected_leakage"] for x in items]))
            rows.append(
                {
                    "category": category.replace("\n", " "),
                    "method": METHOD_LABELS[method],
                    "n_checkpoints": len(items),
                    "scope_errors": errors,
                    "scope_error_rate_pct": 100.0 * errors / len(items),
                    "mean_protected_leakage": leakage,
                }
            )
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_figure(rows: list[dict], output_stem: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7,
            "axes.titlesize": 8,
            "xtick.labelsize": 6.0,
            "ytick.labelsize": 7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )

    categories = list(CATEGORY_SCENARIOS)
    method_labels = [METHOD_LABELS[m] for m in METHODS]
    lookup = {(r["method"], r["category"]): r for r in rows}
    plain_categories = [c.replace("\n", " ") for c in categories]

    errors = np.array(
        [[lookup[(method, category)]["scope_error_rate_pct"] for category in plain_categories]
         for method in method_labels]
    )
    leakage = np.array(
        [[lookup[(method, category)]["mean_protected_leakage"] for category in plain_categories]
         for method in method_labels]
    )
    counts = [lookup[(method_labels[0], category)]["n_checkpoints"] for category in plain_categories]
    error_counts = np.array(
        [[lookup[(method, category)]["scope_errors"] for category in plain_categories]
         for method in method_labels]
    )

    error_cmap = LinearSegmentedColormap.from_list(
        "scope_error", ["#F7FAFC", "#FADBD5", "#D95F4E"]
    )
    leak_cmap = LinearSegmentedColormap.from_list(
        "scope_leakage", ["#F7FAFC", "#DCE9F6", "#3B6FB6"]
    )

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.35), constrained_layout=True)
    panels = (
        (axes[0], errors, error_cmap, 100.0, "a", "Scope error rate (%)"),
        (axes[1], leakage, leak_cmap, max(0.12, float(np.nanmax(leakage))), "b", "Protected-scope leakage"),
    )
    for ax, matrix, cmap, vmax, label, title in panels:
        image = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
        ax.set_title(title, loc="left", fontweight="bold", pad=7)
        ax.set_xticks(
            np.arange(len(categories)),
            [f"{name}\n$n$={n}" for name, n in zip(categories, counts)],
        )
        ax.set_yticks(np.arange(len(method_labels)), method_labels)
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if label == "a":
                    text = f"{int(error_counts[i, j])}/{counts[j]}\n{matrix[i, j]:.0f}%"
                else:
                    text = f"{matrix[i, j]:.3f}"
                color = "white" if matrix[i, j] > 0.58 * vmax else "#1F2933"
                ax.text(j, i, text, ha="center", va="center", fontsize=6.2, color=color)
        cbar = fig.colorbar(image, ax=ax, fraction=0.033, pad=0.018)
        cbar.ax.tick_params(labelsize=6, length=2)
        ax.text(-0.12, 1.13, label, transform=ax.transAxes, fontweight="bold", fontsize=9, va="top")

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--records",
        type=Path,
        default=Path("runs/combined-20260826-101634-645291/records.jsonl"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("paper 2/figures/scopeprobe_boundary"),
    )
    args = parser.parse_args()
    rows = aggregate(read_jsonl(args.records))
    write_csv(rows, args.output.with_suffix(".csv"))
    build_figure(rows, args.output)


if __name__ == "__main__":
    main()
