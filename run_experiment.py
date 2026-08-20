#!/usr/bin/env python3
"""Minimal C2R collective-estimation baseline; standard-library only."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import math
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

SYSTEM = "You answer numerical estimation questions. Return exactly one non-negative integer and no other text."
FORBIDDEN = ("deliberately be wrong", "intentionally be wrong", "mimic human error", "target distribution", "log-normal", "lognormal", "use this distribution", "answer incorrectly", "故意答错", "模仿人类误差", "目标误差分布")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_tasks(path: Path) -> list[dict[str, Any]]:
    tasks = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in tasks:
        if not {"task_id", "question", "truth"}.issubset(row):
            raise ValueError(f"Task missing task_id/question/truth: {row}")
        if float(row["truth"]) < 0:
            raise ValueError(f"truth must be non-negative: {row['task_id']}")
    return tasks


def num(value: float) -> str:
    return f"{value:.6g}" if math.isfinite(value) else "NA"


def json_safe(value: Any) -> Any:
    """JSON has no NaN; preserve unavailable statistics as null."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def sample_sd(xs: list[float]) -> float:
    return statistics.stdev(xs) if len(xs) > 1 else float("nan")


def skew(xs: list[float]) -> float:
    if len(xs) < 3:
        return float("nan")
    m, sd = mean(xs), sample_sd(xs)
    if not sd or not math.isfinite(sd):
        return float("nan")
    return sum(((x - m) / sd) ** 3 for x in xs) / len(xs)


def normal_cdf(x: float, mu: float, sd: float) -> float:
    if sd <= 0:
        return float(x >= mu)
    return 0.5 * (1 + math.erf((x - mu) / (sd * math.sqrt(2))))


def ks_distance(xs: list[float], cdf) -> float:
    if not xs:
        return float("nan")
    ordered = sorted(xs)
    n = len(ordered)
    return max(max(abs(cdf(x) - i / n), abs(cdf(x) - (i - 1) / n)) for i, x in enumerate(ordered, 1))


def fit_summary(xs: list[float]) -> dict[str, float | int | None]:
    if not xs:
        return {"n": 0}
    mu, sd = mean(xs), sample_sd(xs)
    normal_ks = ks_distance(xs, lambda x: normal_cdf(x, mu, sd)) if len(xs) > 1 else float("nan")
    positive = [x for x in xs if x > 0]
    lognormal_ks: float | None = None
    if len(positive) == len(xs) and len(xs) > 1:
        logs = [math.log(x) for x in xs]
        lmu, lsd = mean(logs), sample_sd(logs)
        lognormal_ks = ks_distance(xs, lambda x: normal_cdf(math.log(x), lmu, lsd))
    return {"n": len(xs), "mean": mu, "sd": sd, "skew": skew(xs), "normal_ks": normal_ks, "lognormal_ks": lognormal_ks}


def parse_estimate(text: str) -> int | None:
    cleaned = text.replace(",", "")
    match = re.search(r"(?<![\d.])(\d+(?:\.\d+)?)\s*(thousand|million|billion|k|m|b)?\b", cleaned, flags=re.IGNORECASE)
    if not match:
        return None
    value = float(match.group(1))
    multiplier = {"thousand": 1_000, "k": 1_000, "million": 1_000_000, "m": 1_000_000, "billion": 1_000_000_000, "b": 1_000_000_000}.get((match.group(2) or "").lower(), 1)
    value *= multiplier
    return round(value) if value >= 0 and math.isfinite(value) else None


def call_openai(config: dict[str, Any], prompt: str, persona_broadcast: str = "") -> str:
    base = str(config["base_url"]).rstrip("/")
    key = os.environ.get(str(config.get("api_key_env", "C2R_API_KEY")), "")
    messages = [{"role": "system", "content": SYSTEM}]
    if persona_broadcast.strip():
        messages.append({"role": "system", "content": persona_broadcast})
    messages.append({"role": "user", "content": prompt})
    payload: dict[str, Any] = {"model": config["model"], "messages": messages, "temperature": config.get("temperature", 0.7), "max_tokens": config.get("max_tokens", 128)}
    if config.get("seed") is not None:
        payload["seed"] = config["seed"]
    if config.get("disable_thinking"):
        # DeepSeek's OpenAI-compatible API accepts this field; other compatible servers may ignore it.
        payload["thinking"] = {"type": "disabled"}
    last_error: Exception | None = None
    for attempt in range(int(config.get("request_retries", 1))):
        req = urllib.request.Request(base + "/chat/completions", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                body = json.loads(response.read().decode("utf-8"))
            message = body["choices"][0]["message"]
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content
            finish_reason = body["choices"][0].get("finish_reason")
            raise RuntimeError(f"Empty model content (finish_reason={finish_reason!r}, message_fields={sorted(message)}).")
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, TypeError, RuntimeError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt + 1 < int(config.get("request_retries", 1)):
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Model request failed after {config.get('request_retries', 1)} attempts: {last_error}")


def constraint_report(config: dict[str, Any], tasks: list[dict[str, Any]]) -> dict[str, Any]:
    all_truth_strings = {str(int(float(t["truth"]))) for t in tasks}
    rows = []
    for agent in config["agents"]:
        intervention = str(agent.get("intervention", ""))
        broadcast = str(agent.get("persona_broadcast", ""))
        control_text = intervention + "\n" + broadcast
        lower = control_text.lower()
        leakage = sum(value in control_text.replace(",", "") for value in all_truth_strings)
        forbidden = sum(term in lower for term in FORBIDDEN)
        share = len(control_text) / max(1, len(control_text) + 110)
        burden = min(1.0, 0.65 * share + 0.20 * min(1, forbidden) + 0.15 * min(1, leakage))
        rows.append({"agent_id": agent["agent_id"], "control_level": config.get("control_level", "undeclared"), "intervention_characters": len(intervention), "persona_broadcast_characters": len(broadcast), "persona_broadcast_delivery": "every_agent_task_call" if broadcast else "none", "intervention_token_share_proxy": share, "truth_leakage_count": leakage, "direct_behavior_instruction_count": forbidden, "constraint_burden_proxy": burden, "invalid_for_minimal_control_claim": bool(leakage or forbidden)})
    return {"metric_status": "heuristic_proxy_not_validated_scale", "definition": "0.65*intervention_char_share + 0.20*behavior-injection-indicator + 0.15*truth-leakage-indicator", "agents": rows}


def svg_histogram(xs: list[float]) -> str:
    width, height, left, bottom = 900, 360, 55, 315
    if not xs:
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><text x="30" y="40">No parsed estimates.</text></svg>'
    lo, hi = min(xs), max(xs)
    if lo == hi:
        lo, hi = lo - 1, hi + 1
    bins = 16
    counts = [0] * bins
    for x in xs:
        idx = min(bins - 1, int((x - lo) / (hi - lo) * bins))
        counts[idx] += 1
    peak = max(counts) or 1
    bars = []
    for i, count in enumerate(counts):
        x = left + i * (820 / bins)
        h = 240 * count / peak
        bars.append(f'<rect x="{x:.1f}" y="{bottom-h:.1f}" width="{820/bins-2:.1f}" height="{h:.1f}" fill="#3b82f6" opacity=".76"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><style>text{{font:13px sans-serif;fill:#1f2937}}</style><rect width="100%" height="100%" fill="white"/><text x="55" y="26">Signed log-error distribution (all parsed estimates)</text><line x1="55" y1="315" x2="875" y2="315" stroke="#374151"/><line x1="55" y1="55" x2="55" y2="315" stroke="#374151"/>{''.join(bars)}<text x="55" y="340">{lo:.3f}</text><text x="810" y="340">{hi:.3f}</text></svg>'''


def analyse(rows: list[dict[str, Any]], tasks: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    valid = [r for r in rows if r.get("estimate") is not None]
    errors = [r["signed_log_error"] for r in valid]
    per_task = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in valid:
        grouped[row["task_id"]].append(row)
    task_map = {t["task_id"]: t for t in tasks}
    ratios = []
    for task_id, values in grouped.items():
        estimates = [float(x["estimate"]) for x in values]
        item = task_map[task_id]
        sd = sample_sd(estimates)
        ratio = sd / float(item["human_sd"]) if item.get("human_sd") not in (None, 0) and math.isfinite(sd) else None
        if ratio is not None:
            ratios.append(ratio)
        per_task.append({"task_id": task_id, "truth": item["truth"], "n": len(estimates), "estimate_mean": mean(estimates), "estimate_sd": sd, "median": statistics.median(estimates), "human_sd": item.get("human_sd"), "sd_ratio": ratio})
    by_agent_task: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in valid:
        by_agent_task[(row["agent_id"], row["task_id"])].append(row["signed_log_error"])
    agent_means_by_task: dict[str, list[float]] = defaultdict(list)
    within_sds = []
    for (_, task_id), values in by_agent_task.items():
        agent_means_by_task[task_id].append(mean(values))
        if len(values) > 1:
            within_sds.append(sample_sd(values))
    between_sds = [sample_sd(values) for values in agent_means_by_task.values() if len(values) > 1]
    between = mean([x for x in between_sds if math.isfinite(x)]) if between_sds else float("nan")
    within = mean([x for x in within_sds if math.isfinite(x)]) if within_sds else float("nan")
    diversity = {"definition": "Between-agent variation is calculated from each agent's mean signed log-error within a task; within-agent variation is repeat-sampling variation for the same agent-task.", "between_agent_sd_mean": between, "within_agent_sd_mean": within, "between_to_within_ratio": between / within if math.isfinite(between) and math.isfinite(within) and within > 0 else None, "interpretation": "A ratio cannot be calculated with one sample per agent-task. Increase samples_per_agent_task to >=2 before claiming agent-level differentiation beyond decoding noise."}
    summary = {"parsed_n": len(valid), "unparsed_n": len(rows) - len(valid), "signed_log_error": fit_summary(errors), "agent_differentiation": diversity, "integer_rate": mean([float(r["estimate"] == round(r["estimate"])) for r in valid]), "round_to_10_rate": mean([float(r["estimate"] % 10 == 0) for r in valid]), "round_to_100_rate": mean([float(r["estimate"] % 100 == 0) for r in valid]), "mean_sd_ratio_if_human_reference_available": mean(ratios) if ratios else None, "warning": "Fit statistics are descriptive. A human-match claim requires verified public human microdata, held-out tasks, and pre-specified comparison."}
    return summary, per_task, svg_histogram(errors)


def write_html(out: Path, config: dict[str, Any], summary: dict[str, Any], constraint: dict[str, Any]) -> None:
    blocks = [f"<h1>C2R run: {html.escape(str(config.get('run_name', 'unnamed')))}</h1>", f"<p><b>Backend:</b> {html.escape(str(config['backend']))}.</p>", "<h2>Summary</h2><pre>" + html.escape(json.dumps(summary, ensure_ascii=False, indent=2)) + "</pre>", "<h2>Constraint audit</h2><pre>" + html.escape(json.dumps(constraint, ensure_ascii=False, indent=2)) + "</pre>", '<h2>Distribution</h2><img src="distribution.svg" alt="signed log error histogram">']
    (out / "report.html").write_text("<!doctype html><meta charset='utf-8'>" + "\n".join(blocks), encoding="utf-8")


def reanalyse_existing(run_dir: Path) -> int:
    config = load_json(run_dir / "config_frozen.json")
    rows = [json.loads(line) for line in (run_dir / "raw_results.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    task_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        estimate = parse_estimate(str(row.get("raw_response", "")))
        row["estimate"] = estimate
        row["error"] = None if estimate is not None else "No numeric estimate parsed from model response."
        row.pop("signed_log_error", None)
        if estimate is not None:
            row["signed_log_error"] = math.log((estimate + 0.5) / (float(row["truth"]) + 0.5))
        task_map.setdefault(row["task_id"], {"task_id": row["task_id"], "truth": row["truth"]})
    with (run_dir / "raw_results.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    constraint_path = run_dir / "constraint_report.json"
    constraint = load_json(constraint_path) if constraint_path.exists() else constraint_report(config, list(task_map.values()))
    summary, per_task, svg = analyse(rows, list(task_map.values()))
    summary.update({"run_name": config.get("run_name"), "backend": config["backend"], "task_n": len(task_map), "agent_n": len(config["agents"]), "samples_per_agent_task": config.get("samples_per_agent_task", 1), "reanalysed_from_raw": True})
    summary, constraint = json_safe(summary), json_safe(constraint)
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    (run_dir / "distribution.svg").write_text(svg, encoding="utf-8")
    with (run_dir / "per_task.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["task_id", "truth", "n", "estimate_mean", "estimate_sd", "median", "human_sd", "sd_ratio"]
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(per_task)
    write_html(run_dir, config, summary, constraint)
    print(f"Reanalysed: {run_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config")
    group.add_argument("--reanalyze-run")
    args = parser.parse_args()
    if args.reanalyze_run:
        return reanalyse_existing(Path(args.reanalyze_run).resolve())
    config_path = Path(args.config).resolve()
    config = load_json(config_path)
    for key in ("backend", "tasks_path", "output_root", "agents"):
        if key not in config:
            raise ValueError(f"Missing config key: {key}")
    if config["backend"] != "openai_compatible":
        raise ValueError("This baseline only permits backend=openai_compatible; synthetic/mock backends are intentionally disabled.")
    tasks = load_tasks((config_path.parent / config["tasks_path"]).resolve())
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = (config_path.parent / config["output_root"] / stamp).resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "config_frozen.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = []
    total = len(tasks) * len(config["agents"]) * int(config.get("samples_per_agent_task", 1))
    index = 0
    for task in tasks:
        for agent in config["agents"]:
            prompt = f"{agent.get('intervention', '')}\n\nQuestion: {task['question']}"
            for sample in range(int(config.get("samples_per_agent_task", 1))):
                index += 1
                try:
                    broadcast = str(agent.get("persona_broadcast", ""))
                    raw = call_openai(config, prompt, broadcast)
                    estimate, error = parse_estimate(raw), None
                except Exception as exc:
                    raw, estimate, error = "", None, f"{type(exc).__name__}: {exc}"
                row: dict[str, Any] = {"task_id": task["task_id"], "agent_id": agent["agent_id"], "sample": sample, "truth": task["truth"], "prompt": prompt, "persona_broadcast": str(agent.get("persona_broadcast", "")), "raw_response": raw, "estimate": estimate, "error": error}
                if estimate is not None:
                    row["signed_log_error"] = math.log((estimate + 0.5) / (float(task["truth"]) + 0.5))
                rows.append(row)
                print(f"[{index}/{total}] {task['task_id']} {agent['agent_id']}: {'ok' if estimate is not None else 'error'}", flush=True)
    with (out / "raw_results.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    if not any(row.get("estimate") is not None for row in rows):
        raise RuntimeError(f"No model response could be parsed. Raw errors were saved to {out / 'raw_results.jsonl'}.")
    constraint = constraint_report(config, tasks)
    summary, per_task, svg = analyse(rows, tasks)
    summary.update({"run_name": config.get("run_name"), "backend": config["backend"], "task_n": len(tasks), "agent_n": len(config["agents"]), "samples_per_agent_task": config.get("samples_per_agent_task", 1)})
    summary, constraint = json_safe(summary), json_safe(constraint)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    (out / "constraint_report.json").write_text(json.dumps(constraint, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    (out / "distribution.svg").write_text(svg, encoding="utf-8")
    with (out / "per_task.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["task_id", "truth", "n", "estimate_mean", "estimate_sd", "median", "human_sd", "sd_ratio"]
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(per_task)
    write_html(out, config, summary, constraint)
    print(f"Completed: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
