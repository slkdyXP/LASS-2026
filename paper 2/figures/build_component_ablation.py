#!/usr/bin/env python3
"""Build Figure 5 from the pooled six-component ablation result grid."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb


FULL_EGM = "Full EGM"
ORDER = (
    "Persona",
    "Self state",
    "Consolidated models",
    "Open hypotheses",
    "Recent episodes",
    "Action policy",
)
NAVY_LIGHT = "#D8E0E9"
NAVY_DARK = "#36536F"
EGM_TEAL = "#177E78"


def read_rows(path: Path) -> list[dict[str, float | str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        raw = list(csv.DictReader(stream))
    rows: list[dict[str, float | str]] = []
    for row in raw:
        rows.append(
            {
                "configuration": row["configuration"],
                "n": int(row["n_checkpoints"]),
                "scope": float(row["scope_accuracy_pct"]),
                "action": float(row["action_accuracy_pct"]),
                "violation": float(row["mean_violation_pct"]),
                "delta_scope": float(row["delta_scope_pp"]),
                "delta_action": float(row["delta_action_pp"]),
                "delta_violation": float(row["delta_violation_pp"]),
            }
        )
    if [str(row["configuration"]) for row in rows] != [FULL_EGM, *ORDER]:
        raise ValueError("CSV must contain Full EGM followed by the six configured removals")
    if any(int(row["n"]) != 576 for row in rows):
        raise ValueError("Every pooled ablation row must contain 576 checkpoints")
    baseline = rows[0]
    if (baseline["scope"], baseline["action"], baseline["violation"]) != (96.18, 95.49, 0.71):
        raise ValueError("Full-EGM baseline must agree with the held-out EGM row")
    return rows


def severity_colors(values: np.ndarray) -> list[tuple[float, float, float]]:
    low = np.array(to_rgb(NAVY_LIGHT))
    high = np.array(to_rgb(NAVY_DARK))
    fraction = np.abs(values) / float(np.max(np.abs(values)))
    return [tuple(low + (0.18 + 0.82 * score) * (high - low)) for score in fraction]


def build(rows: list[dict[str, float | str]], output: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    removals = rows[1:]
    labels = [f"-{row['configuration']}" for row in removals]
    y = np.arange(len(removals))
    panels = (
        ("delta_scope", r"$\Delta$ scope accuracy (pp)", (-8.8, 0.7), "a", "negative"),
        ("delta_action", r"$\Delta$ action accuracy (pp)", (-19.0, 0.9), "b", "negative"),
        ("delta_violation", r"$\Delta$ mean violation (pp)", (-0.25, 4.55), "c", "positive"),
    )
    fig, axes = plt.subplots(1, 3, figsize=(7.12, 2.62), sharey=True, layout="constrained")
    fig.set_constrained_layout_pads(w_pad=0.035, h_pad=0.05, wspace=0.11, hspace=0.02)
    for index, (key, xlabel, limits, letter, direction) in enumerate(panels):
        ax = axes[index]
        values = np.array([float(row[key]) for row in removals])
        colors = severity_colors(values)
        ax.axvline(0, color=EGM_TEAL, lw=1.0, zorder=1)
        bars = ax.barh(y, values, height=0.60, color=colors, edgecolor="white", linewidth=0.45, zorder=3)
        for bar, value in zip(bars, values):
            side = 2.6 if value >= 0 else -2.6
            alignment = "left" if value >= 0 else "right"
            label = f"{value:+.2f}"
            ax.annotate(
                label,
                (value, bar.get_y() + bar.get_height() / 2),
                xytext=(side, 0),
                textcoords="offset points",
                ha=alignment,
                va="center",
                fontsize=6.4,
                color="#263849",
            )
        ax.set_xlim(*limits)
        ax.set_xlabel(xlabel)
        ax.tick_params(axis="y", length=0)
        ax.tick_params(axis="x", length=2.5, pad=2)
        ax.grid(axis="x", color="#E9EDF2", linewidth=0.55, zorder=0)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.text(-0.10, 1.04, letter, transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom")
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()
    for ax in axes[1:]:
        ax.tick_params(axis="y", labelleft=False)

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("component_ablation.csv"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("component_ablation"))
    args = parser.parse_args()
    build(read_rows(args.input), args.output)


if __name__ == "__main__":
    main()
