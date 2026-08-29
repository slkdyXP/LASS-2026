from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime
import json
from pathlib import Path
import random
import sys
from typing import Any

from .client import DeepSeekClient
from .claim_audit import audit_claims
from .closed_loop import VALID_CONDITIONS, run_fishery_episode
from .config import config_from_env
from .external_memory import (
    EXTERNAL_CONTROLLER_BASELINE,
    external_controller_config_from_env,
)
from .memory import BASELINES, COMPRESSED_BASELINES
from .mock import MockClient
from .runner import run_trial
from .scenarios import load_scenarios, scenario_public_dict
from .scoring import aggregate, markdown_report, score_probe


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCENARIOS = (
    PROJECT_ROOT / "configs" / "scenarios.json",
    PROJECT_ROOT / "configs" / "scenarios_broad.json",
    PROJECT_ROOT / "configs" / "scenarios_inferential.json",
)


def _scenario_paths(values: list[str] | None) -> list[Path]:
    return [Path(value) for value in values] if values else list(DEFAULT_SCENARIOS)


def _load_all_scenarios(values: list[str] | None):
    scenarios = []
    seen: set[str] = set()
    for path in _scenario_paths(values):
        for scenario in load_scenarios(path):
            if scenario.scenario_id in seen:
                raise SystemExit(f"Duplicate scenario id across files: {scenario.scenario_id}")
            seen.add(scenario.scenario_id)
            scenarios.append(scenario)
    return scenarios


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for value in values:
            handle.write(json.dumps(value, ensure_ascii=False) + "\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _build_client(
    args: argparse.Namespace,
    api_key: str,
    config: Any,
    usage_log_path: Path | None = None,
    usage_metadata: dict[str, Any] | None = None,
):
    if args.dry_run:
        return MockClient()
    if not api_key:
        raise SystemExit(f"API key for provider {config.provider!r} is empty.")
    return DeepSeekClient(
        api_key=api_key,
        base_url=config.base_url,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        timeout_seconds=config.timeout_seconds,
        retries=config.retries,
        provider=config.provider,
        usage_log_path=usage_log_path,
        usage_metadata=usage_metadata,
    )


def run_command(args: argparse.Namespace) -> int:
    config, api_key = config_from_env(
        PROJECT_ROOT,
        provider=args.provider,
        model=args.model,
        temperature=args.temperature,
        repeats=args.repeats,
        seed=args.seed,
    )
    scenarios = _load_all_scenarios(args.scenarios)
    if args.scenario:
        selected = set(args.scenario)
        scenarios = [item for item in scenarios if item.scenario_id in selected]
        missing = selected - {item.scenario_id for item in scenarios}
        if missing:
            raise SystemExit(f"Unknown scenario ids: {sorted(missing)}")
    if args.suite:
        scenarios = [item for item in scenarios if item.suite in set(args.suite)]
    if args.domain:
        scenarios = [item for item in scenarios if item.family in set(args.domain)]
    if args.axis:
        scenarios = [item for item in scenarios if item.axis in set(args.axis)]
    if not scenarios:
        raise SystemExit("No scenarios remain after filtering")
    baselines = args.baseline or list(BASELINES)
    invalid = set(baselines) - set(BASELINES)
    if invalid:
        raise SystemExit(f"Unknown baselines: {sorted(invalid)}")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    output_dir = Path(args.output or PROJECT_ROOT / "runs" / stamp).resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    external_controller_config = (
        external_controller_config_from_env().to_dict()
        if EXTERNAL_CONTROLLER_BASELINE in baselines
        else None
    )
    _write_json(
        output_dir / "manifest.json",
        {
            "config": config.to_dict(),
            "dry_run": args.dry_run,
            "baselines": baselines,
            "scenario_ids": [item.scenario_id for item in scenarios],
            "scenarios": [scenario_public_dict(item) for item in scenarios],
            "external_controller_config": external_controller_config,
            "warning": "Dry-run outputs are plumbing checks and must not be reported as experimental evidence." if args.dry_run else None,
        },
    )
    jobs = [
        (scenario, baseline, repeat)
        for repeat in range(config.repeats)
        for scenario in scenarios
        for baseline in baselines
    ]
    random.Random(config.seed).shuffle(jobs)
    estimated_calls = 0
    for scenario, baseline, _ in jobs:
        estimated_calls += len(scenario.observations) + len(scenario.checkpoints)
        if baseline in COMPRESSED_BASELINES:
            estimated_calls += len(scenario.observations)
        if args.external_evaluator:
            estimated_calls += len(scenario.checkpoints)
    print(
        f"Planned: {len(scenarios)} scenarios × {len(baselines)} baselines × "
        f"{config.repeats} repeats = {len(jobs)} trials; approximately {estimated_calls} model calls",
        flush=True,
    )
    records_path, errors_path = output_dir / "records.jsonl", output_dir / "errors.jsonl"
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    def execute(job: tuple[Any, str, int]):
        scenario, baseline, repeat = job
        client = _build_client(
            args,
            api_key,
            config,
            output_dir / "usage.jsonl",
            {
                "scenario_id": scenario.scenario_id,
                "baseline": baseline,
                "repeat": repeat,
            },
        )
        return job, run_trial(
            client,
            scenario,
            baseline,
            repeat,
            evaluator_client=client if args.external_evaluator else None,
        )

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        future_map = {pool.submit(execute, job): job for job in jobs}
        completed = 0
        for future in as_completed(future_map):
            scenario, baseline, repeat = future_map[future]
            try:
                _, trial_records = future.result()
                records.extend(trial_records)
                _append_jsonl(records_path, trial_records)
            except Exception as exc:  # preserve the rest of a costly batch
                error = {
                    "scenario_id": scenario.scenario_id,
                    "baseline": baseline,
                    "repeat": repeat,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
                errors.append(error)
                _append_jsonl(errors_path, [error])
            completed += 1
            print(f"[{completed}/{len(jobs)}] {scenario.scenario_id} / {baseline} / repeat {repeat}", flush=True)
    summary = aggregate(records)
    _write_json(output_dir / "summary.json", summary)
    (output_dir / "report.md").write_text(markdown_report(summary, errors), encoding="utf-8")
    print(f"Results: {output_dir}")
    print(f"Successful checkpoint records: {len(records)}; failed trials: {len(errors)}")
    return 0 if records else 2


def summarize_command(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    records = _read_jsonl(run_dir / "records.jsonl")
    errors = _read_jsonl(run_dir / "errors.jsonl")
    if not records:
        raise SystemExit(f"No records found in {run_dir}")
    summary = aggregate(records)
    _write_json(run_dir / "summary.json", summary)
    (run_dir / "report.md").write_text(markdown_report(summary, errors), encoding="utf-8")
    print(f"Updated {run_dir / 'report.md'} from {len(records)} records")
    return 0


def combine_command(args: argparse.Namespace) -> int:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    output_dir = Path(args.output or PROJECT_ROOT / "runs" / f"combined-{stamp}").resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    sources: list[str] = []
    seen: set[tuple[Any, ...]] = set()
    current_checkpoints = {}
    if args.rescore:
        for scenario in _load_all_scenarios(None):
            for checkpoint in scenario.checkpoints:
                current_checkpoints[(scenario.scenario_id, checkpoint.round)] = checkpoint
    for value in args.run_dir:
        run_dir = Path(value).resolve()
        sources.append(str(run_dir))
        for record in _read_jsonl(run_dir / "records.jsonl"):
            key = (
                record.get("scenario_id"),
                record.get("baseline"),
                record.get("repeat"),
                record.get("round"),
            )
            if key in seen:
                raise SystemExit(f"Duplicate checkpoint across source runs: {key}")
            if args.rescore:
                checkpoint = current_checkpoints.get((record.get("scenario_id"), record.get("round")))
                if checkpoint is None:
                    raise SystemExit(f"No current checkpoint definition for {key}")
                record["checkpoint"] = asdict(checkpoint)
                record["scores"] = score_probe(
                    record["probe"], checkpoint, float(record["action"]["value"])
                )
            seen.add(key)
            records.append(record)
        errors.extend(_read_jsonl(run_dir / "errors.jsonl"))
    if not records:
        raise SystemExit("No records found in source runs")
    _append_jsonl(output_dir / "records.jsonl", records)
    if errors:
        _append_jsonl(output_dir / "errors.jsonl", errors)
    summary = aggregate(records)
    _write_json(output_dir / "summary.json", summary)
    _write_json(
        output_dir / "manifest.json",
        {"kind": "combined", "source_runs": sources, "rescored_with_current_scenarios": args.rescore},
    )
    (output_dir / "report.md").write_text(markdown_report(summary, errors), encoding="utf-8")
    print(f"Combined {len(records)} records from {len(sources)} runs: {output_dir}")
    return 0


def validate_command(args: argparse.Namespace) -> int:
    scenarios = _load_all_scenarios(args.scenarios)
    print(f"Valid: {len(scenarios)} scenarios, {sum(len(x.checkpoints) for x in scenarios)} checkpoints")
    for scenario in scenarios:
        print(f"- {scenario.scenario_id}: {len(scenario.observations)} rounds, matched_group={scenario.matched_group}")
    return 0


def audit_claims_command(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    records = _read_jsonl(run_dir / "records.jsonl")
    if not records:
        raise SystemExit(f"No records found in {run_dir}")
    if args.baseline:
        selected_baselines = set(args.baseline)
        invalid = selected_baselines - set(BASELINES)
        if invalid:
            raise SystemExit(f"Unknown baselines: {sorted(invalid)}")
        records = [record for record in records if record["baseline"] in selected_baselines]
        if not records:
            raise SystemExit("No records remain after baseline filtering")
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    scenarios = {item["scenario_id"]: item for item in manifest.get("scenarios", [])}
    missing = {record["scenario_id"] for record in records} - set(scenarios)
    if missing:
        raise SystemExit(f"Manifest lacks scenarios required for audit: {sorted(missing)}")
    config, api_key = config_from_env(
        PROJECT_ROOT,
        provider=args.provider,
        model=args.model,
        temperature=args.temperature,
    )
    if not api_key:
        raise SystemExit(f"API key for provider {config.provider!r} is empty.")
    output_path = run_dir / "claim_audits.jsonl"
    if output_path.exists():
        raise SystemExit(f"Refusing to overwrite existing audit: {output_path}")

    def execute(record: dict[str, Any]):
        client = DeepSeekClient(
            api_key=api_key,
            base_url=config.base_url,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout_seconds=config.timeout_seconds,
            retries=config.retries,
            provider=config.provider,
            usage_log_path=run_dir / "claim_audit_usage.jsonl",
        )
        scenario = scenarios[record["scenario_id"]]
        source = scenario["observations"][: int(record["round"])]
        audit, raw = audit_claims(client, source, record["memory_snapshot"], record["action"])
        return {
            "scenario_id": record["scenario_id"],
            "baseline": record["baseline"],
            "repeat": record["repeat"],
            "round": record["round"],
            "audit": audit,
            "raw_response": raw,
        }

    completed: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        future_map = {pool.submit(execute, record): record for record in records}
        for index, future in enumerate(as_completed(future_map), start=1):
            record = future_map[future]
            try:
                result = future.result()
                completed.append(result)
                _append_jsonl(output_path, [result])
            except Exception as exc:
                errors.append(
                    {
                        "scenario_id": record["scenario_id"],
                        "baseline": record["baseline"],
                        "repeat": record["repeat"],
                        "round": record["round"],
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                )
            print(f"[{index}/{len(records)}] claim audit", flush=True)

    by_baseline: dict[str, list[dict[str, Any]]] = {}
    for item in completed:
        by_baseline.setdefault(item["baseline"], []).append(item["audit"])
    summary = {
        "warning": "Model-assisted audit; manually verify positive claims before publication.",
        "records": len(completed),
        "errors": errors,
        "baselines": {
            baseline: {
                "n": len(items),
                "overgeneralization_rate": sum(bool(x.get("overgeneralization_present")) for x in items) / len(items),
                "mean_unsupported_claims": sum(float(x.get("unsupported_claim_count", 0)) for x in items) / len(items),
                "invented_mechanism_rate": sum(bool(x.get("invented_mechanism")) for x in items) / len(items),
                "hypothesis_as_fact_rate": sum(bool(x.get("hypothesis_as_fact")) for x in items) / len(items),
                "group_generalization_rate": sum(bool(x.get("group_generalization")) for x in items) / len(items),
                "stale_after_recovery_rate": sum(bool(x.get("stale_after_recovery")) for x in items) / len(items),
                "action_reliance_rate": sum(bool(x.get("action_relies_on_unsupported_claim")) for x in items) / len(items),
            }
            for baseline, items in sorted(by_baseline.items())
        },
    }
    _write_json(run_dir / "claim_audit_summary.json", summary)
    if errors:
        _write_json(run_dir / "claim_audit_errors.json", errors)
    print(f"Claim audits: {len(completed)} completed, {len(errors)} failed")
    return 0 if completed else 2


def closed_loop_command(args: argparse.Namespace) -> int:
    config, api_key = config_from_env(
        PROJECT_ROOT,
        provider=args.provider,
        model=args.model,
        temperature=args.temperature,
        repeats=args.repeats,
        seed=args.seed,
    )
    if not api_key and not args.dry_run:
        raise SystemExit(f"API key for provider {config.provider!r} is empty.")
    baselines = args.baseline or ["reflection", "evidence_gated_memory_only"]
    invalid = set(baselines) - set(BASELINES)
    if invalid:
        raise SystemExit(f"Unknown baselines: {sorted(invalid)}")
    conditions = args.condition or list(VALID_CONDITIONS)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    output_dir = Path(args.output or PROJECT_ROOT / "runs" / f"closed-loop-{stamp}").resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    _write_json(
        output_dir / "manifest.json",
        {
            "kind": "closed_loop_fishery",
            "config": config.to_dict(),
            "dry_run": args.dry_run,
            "baselines": baselines,
            "conditions": conditions,
            "rounds": args.rounds,
        },
    )

    def factory():
        if args.dry_run:
            return MockClient()
        return DeepSeekClient(
            api_key=api_key,
            base_url=config.base_url,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout_seconds=config.timeout_seconds,
            retries=config.retries,
            provider=config.provider,
            usage_log_path=output_dir / "usage.jsonl",
        )

    jobs = [
        (baseline, condition, repeat)
        for repeat in range(config.repeats)
        for condition in conditions
        for baseline in baselines
    ]
    random.Random(config.seed).shuffle(jobs)
    print(
        f"Planned closed loop: {len(jobs)} episodes; approximately "
        f"{len(jobs) * args.rounds * 10} model calls",
        flush=True,
    )
    episodes: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for index, (baseline, condition, repeat) in enumerate(jobs, start=1):
        try:
            episode = run_fishery_episode(factory, baseline, condition, repeat, rounds=args.rounds)
            episodes.append(episode)
            _append_jsonl(output_dir / "episodes.jsonl", [episode])
        except Exception as exc:
            error = {
                "baseline": baseline,
                "condition": condition,
                "repeat": repeat,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
            errors.append(error)
            _append_jsonl(output_dir / "errors.jsonl", [error])
        print(f"[{index}/{len(jobs)}] {baseline} / {condition} / repeat {repeat}", flush=True)
    _write_json(
        output_dir / "summary.json",
        {"episodes": len(episodes), "failed": len(errors), "metrics": [x["metrics"] for x in episodes]},
    )
    print(f"Closed-loop results: {output_dir}; successful={len(episodes)}, failed={len(errors)}")
    return 0 if episodes else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scopeprobe")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="Validate scenario definitions")
    validate.add_argument("--scenarios", action="append", default=None, help="Scenario JSON; repeat to merge files")
    validate.set_defaults(func=validate_command)

    run = sub.add_parser("run", help="Run controlled diagnostic trials")
    run.add_argument("--scenarios", action="append", default=None, help="Scenario JSON; repeat to merge files")
    run.add_argument("--scenario", action="append", help="Scenario id; repeat to select multiple")
    run.add_argument("--suite", action="append", help="Filter by suite: core, breadth, or stress")
    run.add_argument("--domain", action="append", help="Filter by domain/family")
    run.add_argument("--axis", action="append", help="Filter by experimental axis")
    run.add_argument("--baseline", action="append", choices=BASELINES)
    run.add_argument("--repeats", type=int, default=5)
    run.add_argument("--workers", type=int, default=2)
    run.add_argument("--seed", type=int, default=20260826)
    run.add_argument("--temperature", type=float, default=0.2)
    run.add_argument("--model", default=None)
    run.add_argument("--provider", choices=("deepseek", "openai", "claude"), default="deepseek")
    run.add_argument("--output", default=None)
    run.add_argument("--dry-run", action="store_true", help="Use mock responses; tests plumbing only")
    run.add_argument("--external-evaluator", action="store_true", help="Add a privileged evaluator call at each checkpoint")
    run.set_defaults(func=run_command)

    summarize = sub.add_parser("summarize", help="Recompute a report from an existing run")
    summarize.add_argument("run_dir")
    summarize.set_defaults(func=summarize_command)

    combine = sub.add_parser("combine", help="Combine disjoint run directories into one report")
    combine.add_argument("run_dir", nargs="+")
    combine.add_argument("--output", default=None)
    combine.add_argument("--rescore", action="store_true", help="Recompute labels and scores from current scenario definitions")
    combine.set_defaults(func=combine_command)

    audit = sub.add_parser("audit-claims", help="Run a model-assisted claim-level overgeneralization audit")
    audit.add_argument("run_dir")
    audit.add_argument("--workers", type=int, default=2)
    audit.add_argument("--baseline", action="append", choices=BASELINES)
    audit.add_argument("--temperature", type=float, default=0.0)
    audit.add_argument("--model", default=None)
    audit.add_argument("--provider", choices=("deepseek", "openai", "claude"), default="deepseek")
    audit.set_defaults(func=audit_claims_command)

    closed = sub.add_parser("closed-loop", help="Run a five-agent closed-loop shared-fishery experiment")
    closed.add_argument("--baseline", action="append", choices=BASELINES)
    closed.add_argument("--condition", action="append", choices=VALID_CONDITIONS)
    closed.add_argument("--repeats", type=int, default=2)
    closed.add_argument("--rounds", type=int, default=7)
    closed.add_argument("--temperature", type=float, default=0.2)
    closed.add_argument("--model", default=None)
    closed.add_argument("--provider", choices=("deepseek", "openai", "claude"), default="deepseek")
    closed.add_argument("--seed", type=int, default=20260826)
    closed.add_argument("--output", default=None)
    closed.add_argument("--dry-run", action="store_true")
    closed.set_defaults(func=closed_loop_command)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
