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
import numpy as np


METHODS = ("full_history", "summary", "reflection")
METHOD_LABELS = {
    "full_history": "Direct",
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
            "axes.titlesize": 8.2,
            "xtick.labelsize": 6.2,
            "ytick.labelsize": 6.8,
            "axes.linewidth": 0.7,
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

    short_labels = ("Persist.", "Named", "Cond.", "Self", "Recov.", "Control")
    method_colors = ("#8492A6", "#5F8FB8", "#C65D52")
    bar_width = 0.23
    x = np.arange(len(categories))
    fig, axes = plt.subplots(1, 2, figsize=(7.12, 2.38), layout="constrained")
    fig.set_constrained_layout_pads(w_pad=0.03, h_pad=0.06, wspace=0.10, hspace=0.02)
    panels = (
        (axes[0], errors, "Scope error rate (%)", (0.0, 100.0), np.arange(0, 101, 25), "a"),
        (axes[1], leakage, "Protected-scope leakage", (0.0, 0.18), np.arange(0.0, 0.181, 0.05), "b"),
    )
    handles = []
    for ax, matrix, ylabel, limits, ticks, panel_label in panels:
        for index, (method, color) in enumerate(zip(method_labels, method_colors)):
            bars = ax.bar(
                x + (index - 1) * bar_width,
                matrix[index],
                width=bar_width,
                color=color,
                edgecolor="white",
                linewidth=0.35,
                label=method,
                zorder=3,
            )
            if ax is axes[0]:
                handles.append(bars[0])
        ax.set_xlim(-0.55, len(categories) - 0.45)
        ax.set_ylim(*limits)
        ax.set_yticks(ticks)
        ax.set_xticks(x, [f"{name}\n$n$={n}" for name, n in zip(short_labels, counts)])
        ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", length=0, pad=3)
        ax.tick_params(axis="y", length=2.5, pad=2)
        ax.grid(axis="y", color="#E7E4DE", linewidth=0.55, zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.text(-0.10, 1.06, panel_label, transform=ax.transAxes, fontweight="bold",
                fontsize=8.8, va="bottom")

    fig.legend(handles, method_labels, loc="upper center", ncol=3,
               bbox_to_anchor=(0.5, 1.10), columnspacing=1.4, handlelength=1.2,
               handletextpad=0.45, frameon=False)

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
