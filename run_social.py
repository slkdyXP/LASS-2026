#!/usr/bin/env python3
"""Environment-driven, multi-round collective-estimation simulation."""
from __future__ import annotations

import argparse, datetime as dt, html, json, math, os, random, statistics, sys, urllib.error, urllib.request, time
from pathlib import Path
from typing import Any

FORBIDDEN = ("deliberately be wrong", "intentionally be wrong", "mimic human error", "target distribution", "log-normal", "lognormal", "answer incorrectly", "故意答错", "模仿人类误差", "目标误差分布")

def request(config: dict[str, Any], messages: list[dict[str, str]]) -> str:
    key = os.environ.get(config.get("api_key_env", "C2R_API_KEY"), "")
    if not key: raise RuntimeError("Missing API key")
    payload: dict[str, Any] = {"model": config["model"], "messages": messages, "temperature": config.get("temperature", .7), "max_tokens": config.get("max_tokens", 180)}
    if config.get("disable_thinking"): payload["thinking"] = {"type": "disabled"}
    last: Exception | None = None
    for attempt in range(int(config.get("request_retries", 3))):
        req = urllib.request.Request(config["base_url"].rstrip("/") + "/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json", "Authorization":f"Bearer {key}"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as res: body = json.loads(res.read().decode())
            content = body["choices"][0]["message"].get("content")
            if isinstance(content, str) and content.strip(): return content
            raise RuntimeError("Empty model content")
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, TypeError, RuntimeError, json.JSONDecodeError) as exc:
            last = exc
            if attempt + 1 < int(config.get("request_retries", 3)): time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Request failed after retries: {last}")

def extract_json(text: str) -> dict[str, Any]:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start: raise ValueError(f"No JSON object: {text[:160]}")
    data = json.loads(text[start:end + 1])
    estimate = data.get("estimate")
    if not isinstance(estimate, (int, float)) or estimate < 0: raise ValueError("estimate must be non-negative number")
    utterance = str(data.get("utterance", "")).strip()
    if not utterance: raise ValueError("utterance is empty")
    return {"estimate": round(estimate), "utterance": utterance[:700]}

def agent_messages(agent: dict[str, str], scenario: dict[str, Any], transcript: list[dict[str, Any]], own_memory: list[dict[str, Any]], phase: str) -> list[dict[str, str]]:
    system = "You are an autonomous member of a simulated social group. There is no human user. Stay in character. Do not claim to see the sealed reference card or its true value. Return JSON only: {\"estimate\": non-negative integer, \"utterance\": short natural group message}."
    public = "\n".join(f"R{e['round']} {e['agent_id']}: {e['utterance']} [belief={e['estimate']}]" for e in transcript[-32:]) or "No public conversation yet."
    own = "\n".join(f"R{e['round']}: belief={e['estimate']}; said={e['utterance']}" for e in own_memory[-4:]) or "No previous personal memory."
    broadcast = agent.get("persona_broadcast", "").strip()
    broadcast_context = f"\n\nYOUR PERSISTENT PERSONA BROADCAST:\n{broadcast}" if broadcast else ""
    messages = [{"role":"system","content":system}]
    if broadcast:
        messages.append({"role":"system","content":broadcast})
    user = f"ENVIRONMENT:\n{scenario['world_state']}\n\nYOUR PERSONA:\n{agent['persona']}{broadcast_context}\n\nPUBLIC GROUP CONVERSATION:\n{public}\n\nYOUR PRIVATE MEMORY:\n{own}\n\nPHASE: {phase}\nAct as an internal group participant. Form or revise your own estimate and contribute one concise message to the group."
    return messages + [{"role":"user","content":user}]

def make_population(config: dict[str, Any]) -> list[dict[str, str]]:
    templates = config["persona_templates"]
    population = [dict(config["focal_agent"], group="focal")]
    for index in range(config["population_size"] - 1):
        template = templates[index % len(templates)]
        population.append({"agent_id":f"agent_{index + 1:02d}", "group":template["group"], "persona":template["persona"], "persona_broadcast":template["broadcast"]})
    return population

def stats(values: list[int], truth: float) -> dict[str, float | int]:
    logs = [math.log((value + .5) / (truth + .5)) for value in values]
    return {"n":len(values), "estimate_mean":sum(values)/len(values), "estimate_median":statistics.median(values), "estimate_sd":statistics.stdev(values) if len(values)>1 else 0., "signed_log_error_mean":sum(logs)/len(logs), "signed_log_error_sd":statistics.stdev(logs) if len(logs)>1 else 0., "unique_estimate_rate":len(set(values))/len(values)}

def write_report(out: Path, config: dict[str, Any], snapshots: list[dict[str, Any]], constraint: dict[str, Any]) -> None:
    rows = "".join("<tr>" + "".join(f"<td>{html.escape(str(row.get(key, '')))}</td>" for key in ("round","n","estimate_mean","estimate_median","estimate_sd","signed_log_error_sd","unique_estimate_rate","focal_estimate")) + "</tr>" for row in snapshots)
    page = f"<!doctype html><meta charset='utf-8'><style>body{{font:15px system-ui;margin:32px}}table{{border-collapse:collapse}}td,th{{border:1px solid #ccc;padding:6px}}</style><h1>{html.escape(config['run_name'])}</h1><p>Population={config['population_size']}; rounds={config['rounds']}; all dialogue is agent-to-agent inside a shared environment.</p><h2>Distribution by round</h2><table><tr><th>round</th><th>n</th><th>mean</th><th>median</th><th>SD</th><th>log-error SD</th><th>unique rate</th><th>focal</th></tr>{rows}</table><h2>Constraint audit</h2><pre>{html.escape(json.dumps(constraint, ensure_ascii=False, indent=2))}</pre>"
    (out / "report.html").write_text(page, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", default="config.social.json"); args = parser.parse_args()
    root = Path(args.config).resolve(); config = json.loads(root.read_text(encoding="utf-8"))
    if config.get("backend") != "openai_compatible": raise ValueError("Only real OpenAI-compatible models are allowed.")
    population, scenario = make_population(config), config["scenario"]
    randomizer = random.Random(config.get("seed", 0)); memories = {agent["agent_id"]: [] for agent in population}; transcript: list[dict[str, Any]] = []
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"); out = root.parent / config.get("output_root", "social_runs") / stamp; out.mkdir(parents=True)
    (out / "config_frozen.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    total = len(population) + config["rounds"] * (1 + config["peer_speakers_per_round"]); done = 0
    def act(agent: dict[str, str], round_id: int, phase: str) -> None:
        nonlocal done
        done += 1
        raw = request(config, agent_messages(agent, scenario, transcript, memories[agent["agent_id"]], phase))
        data = extract_json(raw); event = {"round":round_id, "agent_id":agent["agent_id"], "group":agent["group"], **data, "raw_response":raw}
        transcript.append(event); memories[agent["agent_id"]].append(event); print(f"[{done}/{total}] R{round_id} {agent['agent_id']}: {data['estimate']}", flush=True)
    for agent in population: act(agent, 0, "Privately inspect the shared environment, form an initial belief, then introduce your view to the group.")
    snapshots = []
    def snapshot(round_id: int) -> None:
        latest = [memories[a["agent_id"]][-1]["estimate"] for a in population]
        focal = memories["focal"][-1]["estimate"]
        snapshots.append({"round":round_id, **stats(latest, scenario["truth"]), "focal_estimate":focal})
    snapshot(0)
    peers = population[1:]; cursor = 0
    for round_id in range(1, config["rounds"] + 1):
        act(population[0], round_id, "Respond to the group so far, state whether you revise your view, and invite or address disagreement.")
        selected = [peers[(cursor + offset) % len(peers)] for offset in range(config["peer_speakers_per_round"])]
        cursor = (cursor + config["peer_speakers_per_round"]) % len(peers)
        randomizer.shuffle(selected)
        for agent in selected: act(agent, round_id, "Respond to the focal agent and other visible group messages. You may revise your own estimate or maintain it with a reason.")
        snapshot(round_id)
    (out / "trajectory.jsonl").write_text("".join(json.dumps(event, ensure_ascii=False) + "\n" for event in transcript), encoding="utf-8")
    with (out / "distribution_by_round.json").open("w", encoding="utf-8") as handle: json.dump(snapshots, handle, ensure_ascii=False, indent=2)
    all_broadcasts = [a["persona_broadcast"] for a in population]
    control = "\n".join(all_broadcasts).lower(); possible_deliveries = len(population) + config["rounds"] * (1 + config["peer_speakers_per_round"])
    broadcast_agents = sum(bool(text.strip()) for text in all_broadcasts)
    constraint = {"control_level":"L1" if broadcast_agents else "L0", "population_size":len(population), "rounds":config["rounds"], "persona_broadcast_agents":broadcast_agents, "persona_broadcast_delivery_count":possible_deliveries if broadcast_agents else 0, "broadcast_characters_total":sum(map(len, all_broadcasts)), "truth_leakage_count":sum(str(scenario["truth"]) in text.replace(",", "") for text in all_broadcasts), "direct_behavior_instruction_count":sum(term in control for term in FORBIDDEN), "invalid_for_minimal_control_claim":any(term in control for term in FORBIDDEN) or any(str(scenario["truth"]) in text.replace(",", "") for text in all_broadcasts)}
    (out / "constraint_report.json").write_text(json.dumps(constraint, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(out, config, snapshots, constraint)
    print(f"Completed: {out}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
