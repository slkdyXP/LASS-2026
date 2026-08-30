#!/usr/bin/env python3
"""Validate, analyze, and plot controlled consequence-chain experiments.

The script refuses an unbalanced matrix by default. It reports raw outcomes and
matched shock-minus-control contrasts; it never silently imputes failed episodes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, spearmanr, wilcoxon


METHOD_LABELS = {
    "full_history": "Full history",
    "reflection": "Reflection",
    "hscm_external_controller": "EGM",
}
COLORS = {
    "full_history": "#3B6FB6",
    "reflection": "#D95F4E",
    "hscm_external_controller": "#2B8C6B",
}
CONDITION_LABELS = {
    "control": "No shock",
    "other_transient": "Named-other shock",
    "world_transient": "World shock",
}
CONDITION_MARKERS = {"control": "^", "other_transient": "o", "world_transient": "s"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator, n_boot: int = 10_000) -> tuple[float, float]:
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return float("nan"), float("nan")
    if len(values) == 1:
        return float(values[0]), float(values[0])
    means = np.mean(rng.choice(values, size=(n_boot, len(values)), replace=True), axis=1)
    return tuple(float(x) for x in np.quantile(means, [0.025, 0.975]))


def load_episodes(run_dirs: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    episodes: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, int]] = set()
    for run_dir in run_dirs:
        for episode in read_jsonl(run_dir / "episodes.jsonl"):
            key = (episode["baseline"], episode["domain"], episode["condition"], int(episode["repeat"]))
            if key in seen:
                raise SystemExit(f"Duplicate episode key: {key}")
            seen.add(key)
            episodes.append(episode)
        error_path = run_dir / "errors.jsonl"
        if error_path.exists():
            errors.extend(read_jsonl(error_path))
    return episodes, errors


def validate_balance(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    methods = sorted({x["baseline"] for x in episodes})
    domains = sorted({x["domain"] for x in episodes})
    conditions = sorted({x["condition"] for x in episodes})
    repeats = sorted({int(x["repeat"]) for x in episodes})
    observed = Counter((x["baseline"], x["domain"], x["condition"], int(x["repeat"])) for x in episodes)
    missing = [
        (m, d, c, r) for m in methods for d in domains for c in conditions for r in repeats
        if observed[(m, d, c, r)] != 1
    ]
    return {
        "methods": methods, "domains": domains, "conditions": conditions,
        "repeats": repeats, "missing_or_duplicated": missing,
        "balanced": not missing and "control" in conditions,
    }


def frames(episodes: list[dict[str, Any]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    episode_rows: list[dict[str, Any]] = []
    round_rows: list[dict[str, Any]] = []
    for item in episodes:
        base = {
            "method": item["baseline"], "domain": item["domain"],
            "condition": item["condition"], "repeat": int(item["repeat"]),
        }
        rounds = item["rounds"]
        actions = np.asarray([float(record["action"]["value"]) for record in rounds])
        if item["domain"] == "fishery":
            oracle = np.full(len(rounds), 10.0)
            if item["condition"] != "control":
                oracle[4] = 8.0
        elif item["domain"] == "auction":
            oracle = np.full(len(rounds), 50.0)
        else:
            oracle = np.full(len(rounds), 10.0)
        post = slice(4, None)
        derived: dict[str, float] = {
            "oracle_normalized_action_mae": float(np.mean(np.abs(actions[post] - oracle[post])) / (
                120.0 if item["domain"] == "auction" else 20.0
            )),
            "oracle_extreme_action_rounds": float(np.sum(
                (actions[post] <= (12.0 if item["domain"] == "auction" else 2.0))
                | (actions[post] >= (108.0 if item["domain"] == "auction" else 18.0))
            )),
        }
        if item["domain"] == "fishery":
            derived["oracle_private_yield_loss"] = float(max(0.0, np.sum(oracle[post] - actions[post])))
            derived["oracle_resource_deficit"] = float(np.mean([
                max(0.0, 100.0 - float(record["outcome"]["stock"])) for record in rounds[4:]
            ]))
        elif item["domain"] == "auction":
            derived["oracle_post_recovery_wasted_bid"] = float(sum(
                max(0.0, actions[i] - 50.0) if rounds[i]["outcome"]["won"] else 0.0
                for i in range(4, len(rounds))
            ))
            derived["oracle_post_recovery_missed_allocations"] = float(sum(
                not bool(rounds[i]["outcome"]["won"]) for i in range(4, len(rounds))
            ))
            action_text = " ".join(
                str(rounds[i]["action"].get(key, ""))
                for i in range(4, len(rounds)) for key in ("reason", "message")
            )
            patterns = (
                r"above Erin", r"beat Erin", r"Erin(?:'s|’s) bid",
                r"Erin (?:may|might|bid|returned|was|has|will)", r"compete.*Erin", r"tie.*Erin",
            )
            derived["explicit_self_other_confusion"] = float(any(
                re.search(pattern, action_text, re.IGNORECASE) for pattern in patterns
            ))
        else:
            actual = sum(float(record["outcome"]["group_welfare"]) for record in rounds[4:])
            derived["oracle_post_recovery_group_welfare_loss"] = float(max(0.0, 150.0 * (len(rounds)-4) - actual))
        episode_rows.append({**base, **item["metrics"], **derived})
        for record in item["rounds"]:
            round_rows.append({
                **base, "round": int(record["round"]),
                "action": float(record["action"]["value"]), **record["outcome"],
            })
    return pd.DataFrame(episode_rows), pd.DataFrame(round_rows)


def matched_effects(episode_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    outcome_metric = {
        "fishery": "oracle_private_yield_loss",
        "auction": "oracle_post_recovery_wasted_bid",
        "public_goods": "oracle_post_recovery_group_welfare_loss",
    }
    for (method, domain, repeat), group in episode_df.groupby(["method", "domain", "repeat"]):
        controls = group[group.condition == "control"]
        if len(controls) != 1:
            continue
        control = controls.iloc[0]
        for _, shock in group[group.condition != "control"].iterrows():
            metric = outcome_metric[domain]
            rows.append({
                "method": method, "domain": domain, "condition": shock.condition,
                "repeat": int(repeat),
                "delta_overgeneralization": float(shock.late_overgeneralization - control.late_overgeneralization),
                "delta_action_deviation": float(shock.persistent_action_deviation - control.persistent_action_deviation),
                "outcome_metric": metric,
                "outcome_harm": float(shock[metric] - control[metric]),
                "outcome_harm_fraction": float(shock[metric] - control[metric]) / {
                    "fishery": 80.0, "auction": 560.0, "public_goods": 1200.0
                }[domain],
            })
    return pd.DataFrame(rows, columns=[
        "method", "domain", "condition", "repeat", "delta_overgeneralization",
        "delta_action_deviation", "outcome_metric", "outcome_harm", "outcome_harm_fraction",
    ])


def style() -> None:
    mpl.rcParams.update({
        "font.family": "Arial", "font.size": 7, "axes.labelsize": 8,
        "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "axes.linewidth": 0.7, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.major.size": 3, "ytick.major.size": 3, "legend.fontsize": 6.5,
        "figure.dpi": 150, "savefig.dpi": 600, "pdf.fonttype": 42, "ps.fonttype": 42,
    })


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(0.01, 1.10, label, transform=ax.transAxes, fontsize=10,
            fontweight="bold", va="top", ha="left")


def point_ci(ax: plt.Axes, data: pd.DataFrame, metric: str, rng: np.random.Generator) -> None:
    methods = [m for m in METHOD_LABELS if m in set(data.method)]
    conditions = [c for c in ("control", "other_transient", "world_transient") if c in set(data.condition)]
    offsets = np.linspace(-0.18, 0.18, len(conditions)) if conditions else [0]
    for j, condition in enumerate(conditions):
        for i, method in enumerate(methods):
            values = data[(data.method == method) & (data.condition == condition)][metric].astype(float).to_numpy()
            center = float(np.mean(values)); low, high = bootstrap_ci(values, rng)
            x = i + offsets[j]
            marker = CONDITION_MARKERS[condition]
            ax.errorbar(x, center, yerr=[[center-low], [high-center]], fmt=marker,
                        color=COLORS[method], markerfacecolor=("white" if condition == "world_transient" else COLORS[method]),
                        markersize=4, capsize=2, lw=1, label=CONDITION_LABELS[condition] if i == 0 else None)
    ax.set_xticks(range(len(methods)), [METHOD_LABELS[m] for m in methods], rotation=20, ha="right")
    ax.spines[["top", "right"]].set_visible(False)


def make_main_figure(episode_df: pd.DataFrame, effect_df: pd.DataFrame, output: Path) -> None:
    style(); rng = np.random.default_rng(20260830)
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.2), constrained_layout=True)
    ax = axes[0, 0]
    point_ci(ax, episode_df, "late_overgeneralization", rng)
    ax.set_ylabel("Late cognitive overgeneralization")
    ax.set_ylim(bottom=0); ax.legend(frameon=False, loc="upper right")
    panel_label(ax, "a")

    ax = axes[0, 1]
    point_ci(ax, episode_df, "persistent_action_deviation", rng)
    ax.set_ylabel("Persistent action deviation")
    panel_label(ax, "b")

    ax = axes[1, 0]
    domains = [d for d in ("fishery", "auction", "public_goods") if d in set(effect_df.domain)]
    methods = [m for m in METHOD_LABELS if m in set(effect_df.method)]
    width = 0.24
    for j, method in enumerate(methods):
        centers, lows, highs = [], [], []
        for domain in domains:
            vals = 100.0 * effect_df[(effect_df.method == method) & (effect_df.domain == domain)].outcome_harm_fraction.to_numpy(float)
            centers.append(np.mean(vals)); lo, hi = bootstrap_ci(vals, rng); lows.append(lo); highs.append(hi)
        x = np.arange(len(domains)) + (j - (len(methods)-1)/2)*width
        centers_arr = np.asarray(centers)
        ax.bar(x, centers_arr, width=width, color=COLORS[method], alpha=.88, label=METHOD_LABELS[method])
        ax.errorbar(x, centers_arr, yerr=[centers_arr-np.asarray(lows), np.asarray(highs)-centers_arr],
                    fmt="none", ecolor="black", lw=.7, capsize=1.5)
    ax.axhline(0, color="#444444", lw=.6)
    ax.set_xticks(range(len(domains)), [d.replace("_", " ").title() for d in domains])
    ax.set_ylabel("Control-adjusted post-recovery harm\n(% of domain range)")
    ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, ncol=1)
    panel_label(ax, "c")

    ax = axes[1, 1]
    for method in methods:
        sub = effect_df[effect_df.method == method]
        ax.scatter(sub.delta_overgeneralization, sub.delta_action_deviation, s=18,
                   color=COLORS[method], alpha=.75, edgecolor="white", linewidth=.3,
                   label=METHOD_LABELS[method])
    valid = effect_df[["delta_overgeneralization", "delta_action_deviation"]].dropna()
    if len(valid) >= 3:
        rho, p = spearmanr(valid.delta_overgeneralization, valid.delta_action_deviation)
        ax.text(.03, .97, f"Spearman $\\rho$={rho:.2f}, $P$={p:.3g}", transform=ax.transAxes, va="top")
    ax.axhline(0, color="#777", lw=.5); ax.axvline(0, color="#777", lw=.5)
    ax.set_xlabel("Shock-induced cognitive change")
    ax.set_ylabel("Shock-induced persistent action change")
    ax.spines[["top", "right"]].set_visible(False)
    panel_label(ax, "d")

    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        fig.savefig(output / f"consequence_main.{suffix}", bbox_inches="tight")
    plt.close(fig)


def make_trajectory_figure(round_df: pd.DataFrame, output: Path) -> None:
    style()
    domains = [d for d in ("fishery", "auction", "public_goods") if d in set(round_df.domain)]
    fig, axes = plt.subplots(len(domains), 2, figsize=(7.2, 2.0*len(domains)), squeeze=False, constrained_layout=True)
    for i, domain in enumerate(domains):
        for j, condition in enumerate(("other_transient", "world_transient")):
            ax = axes[i, j]
            data = round_df[(round_df.domain == domain) & (round_df.condition == condition)]
            for method in METHOD_LABELS:
                sub = data[data.method == method]
                if sub.empty: continue
                grouped = sub.groupby("round").action
                x = np.asarray(sorted(grouped.groups)); means = grouped.mean().reindex(x).to_numpy()
                sem = grouped.sem().reindex(x).fillna(0).to_numpy()
                ax.plot(x, means, color=COLORS[method], lw=1.3, label=METHOD_LABELS[method])
                ax.fill_between(x, means-1.96*sem, means+1.96*sem, color=COLORS[method], alpha=.14, linewidth=0)
            ax.axvspan(3.7, 4.3, color="#999999", alpha=.16, lw=0)
            ax.axvline(4, color="#555", lw=.6, ls="--")
            ax.set_title(f"{domain.replace('_',' ').title()} · {CONDITION_LABELS[condition]}")
            ax.set_xlabel("Round"); ax.set_ylabel("Agent action")
            ax.spines[["top", "right"]].set_visible(False)
            if i == 0 and j == 1: ax.legend(frameon=False, loc="best")
            panel_label(ax, chr(ord("a") + i*2+j))
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        fig.savefig(output / f"consequence_trajectories.{suffix}", bbox_inches="tight")
    plt.close(fig)


def make_identity_figure(episode_df: pd.DataFrame, output: Path) -> None:
    style(); auction = episode_df[episode_df.domain == "auction"].copy()
    methods = [m for m in ("reflection", "hscm_external_controller") if m in set(auction.method)]
    fig, axes = plt.subplots(1, 2, figsize=(3.35, 1.85), constrained_layout=True)
    fig.set_constrained_layout_pads(w_pad=0.08, h_pad=0.04, wspace=0.12, hspace=0.02)
    ax = axes[0]
    for i, method in enumerate(methods):
        vals = auction[auction.method == method].explicit_self_other_confusion.to_numpy(float)
        rate = float(np.mean(vals)); n = len(vals); z = 1.96
        center = (rate + z*z/(2*n))/(1+z*z/n)
        half = z*np.sqrt(rate*(1-rate)/n + z*z/(4*n*n))/(1+z*z/n)
        ax.bar(i, 100*rate, color=COLORS[method], width=.62)
        ax.errorbar(i, 100*rate, yerr=[[100*(rate-max(0,center-half))],[100*(min(1,center+half)-rate)]],
                    fmt="none", ecolor="black", capsize=2, lw=.8)
        ax.text(i, 100*rate+3, f"{int(vals.sum())}/{n}", ha="center", fontsize=7)
    ax.set_xticks(range(len(methods)), [METHOD_LABELS[m] for m in methods])
    ax.set_xlim(-0.72, len(methods) - 0.28)
    ax.set_ylabel("Self-as-competitor\ntrajectories (%)"); ax.set_ylim(0, 100)
    ax.spines[["top", "right"]].set_visible(False); panel_label(ax, "a")

    ax = axes[1]
    rng = np.random.default_rng(20260830)
    for i, method in enumerate(methods):
        vals = auction[auction.method == method].oracle_post_recovery_wasted_bid.to_numpy(float)
        jitter = rng.uniform(-.10, .10, size=len(vals))
        ax.scatter(i+jitter, vals, color=COLORS[method], s=15, alpha=.65, edgecolor="white", linewidth=.3)
        center=np.mean(vals); low,high=bootstrap_ci(vals,rng)
        ax.errorbar(i,center,yerr=[[center-low],[high-center]],fmt="_",markersize=10,
                    color="black",capsize=2,lw=.9)
    ax.set_xticks(range(len(methods)), [METHOD_LABELS[m] for m in methods])
    ax.set_xlim(-0.72, len(methods) - 0.28)
    ax.set_ylabel("Excess post-recovery\nbid expenditure")
    ax.spines[["top", "right"]].set_visible(False); panel_label(ax, "b")
    for suffix in ("pdf", "svg", "png"):
        fig.savefig(output / f"consequence_identity_confusion.{suffix}", bbox_inches="tight")
    plt.close(fig)


def write_audit_samples(episodes: list[dict[str, Any]], episode_df: pd.DataFrame, output: Path) -> None:
    scores = {
        (row.method, row.domain, row.condition, int(row.repeat)):
        float(row.late_overgeneralization) + 2.0 * float(row.oracle_normalized_action_mae)
        for row in episode_df.itertuples()
    }
    selected = sorted(
        episodes,
        key=lambda x: scores[(x["baseline"], x["domain"], x["condition"], int(x["repeat"]))],
        reverse=True,
    )[:15]
    lines = [
        "# High-signal raw-log audit sample", "",
        "> Mechanically selected by late overgeneralization + 2 × oracle-normalized action MAE. "
        "Selection is not a human correctness judgment.", "",
    ]
    for item in selected:
        key = (item["baseline"], item["domain"], item["condition"], int(item["repeat"]))
        lines.extend([
            f"## {key[0]} · {key[1]} · {key[2]} · repeat {key[3]}", "",
            f"- Selection score: {scores[key]:.4f}",
            f"- Actions: {[float(x['action']['value']) for x in item['rounds']]}",
            f"- Late probe: `{json.dumps(item['probes'][-1]['probe'], ensure_ascii=False)}`", "",
            "### Post-event action reasons", "",
        ])
        for record in item["rounds"][4:]:
            lines.append(
                f"- Round {record['round']}: {record['action']['value']} — "
                f"{record['action'].get('reason', '')}"
            )
        memory = item["rounds"][-1].get("memory_snapshot", "not retained in this pilot")
        if isinstance(memory, list): memory = "\n".join(str(x) for x in memory)
        lines.extend(["", "### Final memory excerpt", "", "```text", str(memory)[-3000:], "```", ""])
    (output / "audit_samples.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    episodes, errors = load_episodes(args.run_dir)
    design = validate_balance(episodes)
    if not design["balanced"] and not args.allow_incomplete:
        raise SystemExit(f"Refusing unbalanced analysis; missing/duplicated cells: {design['missing_or_duplicated'][:10]}")
    episode_df, round_df = frames(episodes)
    effect_df = matched_effects(episode_df)
    args.output.mkdir(parents=True, exist_ok=True)
    episode_df.to_csv(args.output / "episode_metrics.csv", index=False)
    round_df.to_csv(args.output / "round_metrics.csv", index=False)
    effect_df.to_csv(args.output / "matched_effects.csv", index=False)
    rng = np.random.default_rng(20260830)
    stats = {
        "design": design, "source_runs": [str(x.resolve()) for x in args.run_dir],
        "episodes": len(episodes), "source_error_records": len(errors),
        "matched_effects": [], "paired_method_comparisons": [],
    }
    for keys, group in effect_df.groupby(["method", "domain", "condition"]):
        method, domain, condition = keys
        for metric in ("delta_overgeneralization", "delta_action_deviation", "outcome_harm"):
            values = group[metric].to_numpy(float); low, high = bootstrap_ci(values, rng)
            stats["matched_effects"].append({
                "method": method, "domain": domain, "condition": condition, "metric": metric,
                "n": len(values), "mean": float(np.mean(values)), "ci95": [low, high],
            })
    pair_keys = ["domain", "condition", "repeat"]
    for metric in ("late_overgeneralization", "oracle_normalized_action_mae", "oracle_extreme_action_rounds"):
        pivot = episode_df.pivot(index=pair_keys, columns="method", values=metric)
        for comparator in ("full_history", "hscm_external_controller"):
            if comparator not in pivot or "reflection" not in pivot:
                continue
            paired = pivot[["reflection", comparator]].dropna()
            diff = (paired["reflection"] - paired[comparator]).to_numpy(float)
            low, high = bootstrap_ci(diff, rng)
            try:
                test = wilcoxon(paired["reflection"], paired[comparator], zero_method="pratt", alternative="two-sided")
                statistic, p_value = float(test.statistic), float(test.pvalue)
                if not np.isfinite(p_value):
                    statistic, p_value = 0.0, 1.0
            except ValueError:
                statistic, p_value = 0.0, 1.0
            stats["paired_method_comparisons"].append({
                "metric": metric, "reflection_minus": comparator, "n_pairs": len(diff),
                "mean_difference": float(np.mean(diff)), "ci95": [low, high],
                "wilcoxon_statistic": statistic, "wilcoxon_p": p_value,
            })
    valid = effect_df[["delta_overgeneralization", "delta_action_deviation"]].dropna()
    if len(valid) >= 3:
        rho, p_value = spearmanr(valid.delta_overgeneralization, valid.delta_action_deviation)
        stats["shock_delta_spearman"] = {"n": len(valid), "rho": float(rho), "p": float(p_value)}
    auction = episode_df[episode_df.domain == "auction"]
    stats["explicit_self_other_confusion"] = {}
    for method, group in auction.groupby("method"):
        count = int(group.explicit_self_other_confusion.sum())
        stats["explicit_self_other_confusion"][method] = {
            "count": count, "n": len(group), "rate": count / len(group)
        }
    if {"reflection", "full_history"}.issubset(stats["explicit_self_other_confusion"]):
        a = stats["explicit_self_other_confusion"]["reflection"]
        b = stats["explicit_self_other_confusion"]["full_history"]
        test = fisher_exact([[a["count"], a["n"]-a["count"]], [b["count"], b["n"]-b["count"]]])
        stats["explicit_self_other_confusion"]["fisher_reflection_vs_full_history_p"] = float(test.pvalue)
    usage_records: list[dict[str, Any]] = []
    for run_dir in args.run_dir:
        usage_path = run_dir / "usage.jsonl"
        if usage_path.exists(): usage_records.extend(read_jsonl(usage_path))
    stats["usage"] = {
        "calls": len(usage_records),
        "prompt_tokens": sum(int(x.get("prompt_tokens", 0)) for x in usage_records),
        "completion_tokens": sum(int(x.get("completion_tokens", 0)) for x in usage_records),
        "cache_hit_tokens": sum(int(x.get("cache_hit_tokens", 0)) for x in usage_records),
        "resolved_models": sorted({x.get("resolved_model") for x in usage_records if x.get("resolved_model")}),
    }
    (args.output / "analysis.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    report = [
        "# Consequence-chain analysis", "",
        f"- Episodes: {len(episodes)}", f"- Balanced matrix: {design['balanced']}",
        f"- Source error records: {len(errors)}", f"- Model calls: {stats['usage']['calls']}", "",
        "## Paired method comparisons", "",
        "| Metric | Contrast | n | Mean difference | 95% bootstrap CI | Wilcoxon P |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for item in stats["paired_method_comparisons"]:
        report.append(
            f"| {item['metric']} | Reflection − {METHOD_LABELS.get(item['reflection_minus'], item['reflection_minus'])} "
            f"| {item['n_pairs']} | {item['mean_difference']:.4f} | "
            f"[{item['ci95'][0]:.4f}, {item['ci95'][1]:.4f}] | {item['wilcoxon_p']:.4g} |"
        )
    report.extend(["", "> Wilcoxon P values are descriptive because trajectories are clustered within only three domains.", ""])
    (args.output / "report.md").write_text("\n".join(report), encoding="utf-8")
    make_main_figure(episode_df, effect_df, args.output)
    make_trajectory_figure(round_df, args.output)
    make_identity_figure(episode_df, args.output)
    write_audit_samples(episodes, episode_df, args.output)
    print(f"Analyzed {len(episodes)} episodes; figures and tables: {args.output}")


if __name__ == "__main__":
    main()
