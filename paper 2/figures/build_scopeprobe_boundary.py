#!/usr/bin/env python3
"""Build Figure 2 from the three-model frozen ScopeProbe result grid.

The checked-in CSV is the plot source. Error-rate bars pool the three models
within an evidence category (n=144); their intervals are Wilson 95% intervals.
Leakage bars are equal-weight model means, with a thin range spanning the three
model-level means rather than a checkpoint-level confidence interval.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


CATEGORIES = ("Persistent", "Named other", "Conditional", "Self-state", "Recovered", "Control")
METHODS = ("Direct", "Summary", "Reflection")
MODELS = ("DS", "GPT", "Claude")
METHOD_COLORS = {
    "Direct": "#8A97A8",
    "Summary": "#5B87B3",
    "Reflection": "#C65D4F",
}
SHORT_LABELS = ("Persist.", "Named", "Cond.", "Self", "Recov.", "Control")


def read_rows(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    parsed: list[dict[str, object]] = []
    for row in rows:
        parsed.append(
            {
                "model": row["model"],
                "category": row["category"],
                "method": row["method"],
                "n": int(row["n_checkpoints"]),
                "errors": int(row["scope_errors"]),
                "leakage": float(row["mean_protected_leakage"]),
            }
        )
    expected = {(model, category, method) for model in MODELS for category in CATEGORIES for method in METHODS}
    observed = {(r["model"], r["category"], r["method"]) for r in parsed}
    if observed != expected or len(parsed) != len(expected):
        raise ValueError("CSV must contain exactly one row for every model/category/updater cell")
    if any(r["n"] != 48 for r in parsed):
        raise ValueError("Every model/category/updater cell must contain 48 checkpoints")
    return parsed


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    radius = z * math.sqrt((p * (1.0 - p) + z * z / (4.0 * n)) / n) / denom
    return center - radius, center + radius


def summarize(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, float]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["category"]), str(row["method"]))].append(row)

    summary: dict[tuple[str, str], dict[str, float]] = {}
    for category in CATEGORIES:
        for method in METHODS:
            items = grouped[(category, method)]
            if {item["model"] for item in items} != set(MODELS):
                raise ValueError(f"Incomplete model coverage for {category}/{method}")
            errors = sum(int(item["errors"]) for item in items)
            n = sum(int(item["n"]) for item in items)
            low, high = wilson_interval(errors, n)
            leakage_values = [float(item["leakage"]) for item in items]
            summary[(category, method)] = {
                "errors": errors,
                "n": n,
                "rate": 100.0 * errors / n,
                "ci_low": 100.0 * low,
                "ci_high": 100.0 * high,
                "leakage": float(np.mean(leakage_values)),
                "leakage_low": min(leakage_values),
                "leakage_high": max(leakage_values),
            }

    expected_errors = {"Direct": 57, "Summary": 95, "Reflection": 174}
    actual_errors = {method: sum(int(summary[(category, method)]["errors"]) for category in CATEGORIES) for method in METHODS}
    if actual_errors != expected_errors:
        raise ValueError(f"Pooled error totals disagree with Table 2: {actual_errors}")
    return summary


def build_figure(summary: dict[tuple[str, str], dict[str, float]], output_stem: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "axes.linewidth": 0.8,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )

    x = np.arange(len(CATEGORIES))
    width = 0.22
    fig, axes = plt.subplots(1, 2, figsize=(7.12, 2.62), layout="constrained")
    fig.set_constrained_layout_pads(w_pad=0.035, h_pad=0.06, wspace=0.12, hspace=0.02)

    handles = []
    for method_index, method in enumerate(METHODS):
        positions = x + (method_index - 1) * width
        values = np.array([summary[(category, method)]["rate"] for category in CATEGORIES])
        lower = np.array([summary[(category, method)]["ci_low"] for category in CATEGORIES])
        upper = np.array([summary[(category, method)]["ci_high"] for category in CATEGORIES])
        bars = axes[0].bar(
            positions,
            values,
            width=width,
            color=METHOD_COLORS[method],
            edgecolor="white",
            linewidth=0.45,
            zorder=3,
            label=method,
        )
        axes[0].errorbar(
            positions,
            values,
            yerr=np.vstack((values - lower, upper - values)),
            fmt="none",
            ecolor="#374151",
            elinewidth=0.65,
            capsize=1.8,
            capthick=0.65,
            zorder=4,
        )
        handles.append(bars[0])

        leakage = np.array([summary[(category, method)]["leakage"] for category in CATEGORIES])
        leakage_low = np.array([summary[(category, method)]["leakage_low"] for category in CATEGORIES])
        leakage_high = np.array([summary[(category, method)]["leakage_high"] for category in CATEGORIES])
        axes[1].bar(
            positions,
            leakage,
            width=width,
            color=METHOD_COLORS[method],
            edgecolor="white",
            linewidth=0.45,
            zorder=3,
        )
        axes[1].vlines(positions, leakage_low, leakage_high, color="#374151", linewidth=0.65, zorder=4)
        axes[1].hlines(leakage_low, positions - 0.025, positions + 0.025, color="#374151", linewidth=0.65, zorder=4)
        axes[1].hlines(leakage_high, positions - 0.025, positions + 0.025, color="#374151", linewidth=0.65, zorder=4)

    common_labels = [f"{label}\n$n$=144" for label in SHORT_LABELS]
    panels = (
        (axes[0], "Scope error rate (%)", (0.0, 43.0), np.arange(0, 41, 10), "a"),
        (axes[1], "Protected-scope leakage", (0.0, 0.135), (0.00, 0.05, 0.10), "b"),
    )
    for ax, ylabel, ylim, ticks, panel_label in panels:
        ax.set_xlim(-0.55, len(CATEGORIES) - 0.45)
        ax.set_ylim(*ylim)
        ax.set_yticks(ticks)
        ax.set_xticks(x, common_labels)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", length=0, pad=3)
        ax.tick_params(axis="y", length=2.5, pad=2)
        ax.grid(axis="y", color="#E9EDF2", linewidth=0.55, zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.text(-0.10, 1.04, panel_label, transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom")

    fig.legend(
        handles,
        METHODS,
        loc="upper center",
        ncol=3,
        bbox_to_anchor=(0.5, 1.08),
        columnspacing=1.6,
        handlelength=1.3,
        handletextpad=0.45,
    )
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("scopeprobe_boundary.csv"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("scopeprobe_boundary"))
    args = parser.parse_args()
    build_figure(summarize(read_rows(args.input)), args.output)


if __name__ == "__main__":
    main()
