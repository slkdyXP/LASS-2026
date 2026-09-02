#!/usr/bin/env python3
"""Build Figure 4 from the three-model auction identity-failure results."""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


MODELS = ("DS", "GPT", "Claude")
METHODS = ("Reflection", "EGM")
COLORS = {"Reflection": "#C65D4F", "EGM": "#177E78"}
MARKERS = {"DS": "o", "GPT": "s", "Claude": "^"}
IDENTITY_COUNTS = {
    "DS": {"Reflection": 17, "EGM": 2},
    "GPT": {"Reflection": 14, "EGM": 1},
    "Claude": {"Reflection": 12, "EGM": 1},
}
POOLED_IDENTITY_CI = {"Reflection": (37.8, 58.0), "EGM": (1.7, 10.9)}
BID_CI = {"Reflection": (26.75, 30.18), "EGM": (4.13, 5.47)}
BID_EXCESS = {
    "DS": {
        "Reflection": [18, 20, 22, 23, 24, 24, 25, 26, 27, 28, 28, 29, 29, 30, 30,
                       31, 31, 32, 32, 33, 33, 34, 35, 36, 37, 38, 40, 42, 48, 58],
        "EGM": [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6,
                6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 10, 11, 12, 14],
    },
    "GPT": {
        "Reflection": [14, 16, 18, 20, 21, 22, 22, 23, 24, 25, 25, 26, 26, 27, 27,
                       28, 28, 29, 29, 30, 30, 31, 32, 33, 34, 35, 36, 38, 43, 52],
        "EGM": [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4,
                5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 10, 12],
    },
    "Claude": {
        "Reflection": [12, 14, 16, 18, 19, 20, 20, 21, 22, 22, 23, 23, 24, 24, 25,
                       25, 26, 26, 27, 27, 28, 29, 30, 31, 32, 33, 34, 36, 40, 48],
        "EGM": [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4,
                4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8, 8, 9, 11],
    },
}


def validate() -> None:
    for model in MODELS:
        for method in METHODS:
            if len(BID_EXCESS[model][method]) != 30:
                raise ValueError(f"Expected 30 auction trajectories for {model}/{method}")
    pooled_reflection = sum(IDENTITY_COUNTS[model]["Reflection"] for model in MODELS)
    pooled_egm = sum(IDENTITY_COUNTS[model]["EGM"] for model in MODELS)
    if (pooled_reflection, pooled_egm) != (43, 4):
        raise ValueError("Identity-count totals must equal 43/90 and 4/90")
    expected_means = {"Reflection": 28.47, "EGM": 4.80}
    for method, expected in expected_means.items():
        values = [value for model in MODELS for value in BID_EXCESS[model][method]]
        if not np.isclose(np.mean(values), expected, atol=0.01):
            raise ValueError(f"Pooled {method} bid mean does not match the result grid")


def build(output: Path) -> None:
    validate()
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.2,
            "axes.labelsize": 7.6,
            "xtick.labelsize": 7,
            "ytick.labelsize": 6.8,
            "axes.linewidth": 0.8,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(3.35, 2.30), layout="constrained")
    fig.set_constrained_layout_pads(w_pad=0.04, h_pad=0.05, wspace=0.20, hspace=0.02)

    positions = np.arange(len(METHODS))
    pooled_pct = np.array([
        100.0 * sum(IDENTITY_COUNTS[model][method] for model in MODELS) / 90.0
        for method in METHODS
    ])
    lower = np.array([POOLED_IDENTITY_CI[method][0] for method in METHODS])
    upper = np.array([POOLED_IDENTITY_CI[method][1] for method in METHODS])
    axes[0].bar(
        positions,
        pooled_pct,
        width=0.62,
        color=[COLORS[method] for method in METHODS],
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    axes[0].errorbar(
        positions,
        pooled_pct,
        yerr=np.vstack((pooled_pct - lower, upper - pooled_pct)),
        fmt="none",
        ecolor="#374151",
        elinewidth=0.75,
        capsize=2.2,
        capthick=0.75,
        zorder=4,
    )
    for model_index, model in enumerate(MODELS):
        for method_index, method in enumerate(METHODS):
            model_pct = 100.0 * IDENTITY_COUNTS[model][method] / 30.0
            axes[0].scatter(
                positions[method_index] + (-0.13, 0.0, 0.13)[model_index],
                model_pct,
                marker=MARKERS[model],
                s=22,
                color=COLORS[method],
                edgecolor="white",
                linewidth=0.45,
                zorder=5,
            )
    axes[0].set_xticks(positions, METHODS)
    axes[0].set_ylim(0, 70)
    axes[0].set_yticks((0, 20, 40, 60))
    axes[0].set_ylabel("Self-as-competitor\ntrajectories (%)")
    axes[0].grid(axis="y", color="#E9EDF2", linewidth=0.55, zorder=0)
    axes[0].spines[["top", "right"]].set_visible(False)
    axes[0].text(-0.12, 1.04, "a", transform=axes[0].transAxes, fontweight="bold", fontsize=9, va="bottom")

    rng = np.random.default_rng(20260831)
    for method_index, method in enumerate(METHODS):
        values = np.array([value for model in MODELS for value in BID_EXCESS[model][method]], dtype=float)
        violin = axes[1].violinplot(values, positions=[method_index], widths=0.68, showextrema=False)
        for body in violin["bodies"]:
            body.set_facecolor(COLORS[method])
            body.set_edgecolor("none")
            body.set_alpha(0.15)
        for model in MODELS:
            model_values = np.asarray(BID_EXCESS[model][method], dtype=float)
            jitter = rng.uniform(-0.19, 0.19, size=len(model_values))
            axes[1].scatter(
                method_index + jitter,
                model_values,
                marker=MARKERS[model],
                s=12,
                color=COLORS[method],
                alpha=0.55,
                linewidth=0.0,
                zorder=3,
            )
        mean = float(np.mean(values))
        ci_low, ci_high = BID_CI[method]
        axes[1].errorbar(
            method_index,
            mean,
            yerr=[[mean - ci_low], [ci_high - mean]],
            fmt="D",
            markersize=4.0,
            markerfacecolor="white",
            markeredgecolor=COLORS[method],
            markeredgewidth=1.0,
            color="#374151",
            ecolor="#374151",
            elinewidth=0.75,
            capsize=2.0,
            zorder=5,
        )
    axes[1].axhline(0, color="#177E78", linewidth=0.8, linestyle="--", zorder=1)
    axes[1].set_xticks(positions, METHODS)
    axes[1].set_ylim(-4, 64)
    axes[1].set_yticks((0, 20, 40, 60))
    axes[1].set_ylabel("Excess post-recovery\nbid expenditure")
    axes[1].grid(axis="y", color="#E9EDF2", linewidth=0.55, zorder=0)
    axes[1].spines[["top", "right"]].set_visible(False)
    axes[1].text(-0.12, 1.04, "b", transform=axes[1].transAxes, fontweight="bold", fontsize=9, va="bottom")

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build(Path(__file__).with_name("consequence_identity_confusion"))
