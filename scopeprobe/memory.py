from __future__ import annotations

from dataclasses import dataclass, field
import json

from .client import ChatClient, parse_json_object
from .scenarios import Checkpoint, Scenario


BASELINES = (
    "direct",
    "recent_window",
    "retrieval",
    "full_history",
    "summary",
    "reflection",
    "guarded_reflection",
    "structured_reflection",
    "evidence_gated_memory_only",
    "evidence_gated_reflection",
)

COMPRESSED_BASELINES = {
    "summary",
    "reflection",
    "guarded_reflection",
    "structured_reflection",
    "evidence_gated_memory_only",
    "evidence_gated_reflection",
}


ACTION_SYSTEM = """You are an autonomous participant in a repeated social-resource simulation.
Act only from the information supplied. Do not assume hidden causes. Preserve your assigned persona while adapting strategy when evidence warrants it.
Return valid JSON only, with this schema:
{"value": number, "message": "one concise public message", "reason": "one concise private reason"}
The numeric value must respect the stated bounds."""


PROBE_SYSTEM = """You are reporting the participant's current beliefs, using only the supplied active memory. This report is for measurement and will not be added to future memory.
Return valid JSON only with exactly these fields:
{
  "primary_scope": "self|other|world|persona|episodic|none",
  "updates": {"self": 0.0, "other": 0.0, "world": 0.0, "persona": 0.0, "episodic": 0.0},
  "target_agent": "name or none",
  "generalizes_to_group": false,
  "change_is_temporary": true,
  "persona_changed": false,
  "confidence": 0.0,
  "rationale": "one concise sentence"
}
primary_scope must answer the measurement question's focal causal attribution, not merely name the most recent thing that changed. Each update score is how strongly the participant's CURRENT PERSISTENT MODEL in that scope differs from its initial state, from 0 (unchanged) to 1 (strongly changed). episodic instead measures retention as a temporary event. A changed group strategy does not by itself mean partner traits changed. Use none when no current long-term update is warranted. Do not claim that your core persona changed merely because your strategy changed."""


@dataclass
class MemoryState:
    baseline: str
    transcript: list[str] = field(default_factory=list)
    compressed: str = "No prior experience."


def _header(scenario: Scenario) -> str:
    low, high = scenario.action_bounds
    return (
        f"Persona: {scenario.persona}\n"
        f"Role: {scenario.role}\n"
        f"Required numeric action: {scenario.action_name}, bounded [{low}, {high}]."
    )


def active_context(state: MemoryState, scenario: Scenario, observation: str) -> str:
    header = _header(scenario)
    if state.baseline == "direct":
        evidence = f"Current observation only:\n{observation}"
    elif state.baseline == "full_history":
        history = "\n".join(state.transcript) if state.transcript else "No prior rounds."
        evidence = f"Complete interaction history:\n{history}\nCurrent observation:\n{observation}"
    elif state.baseline == "recent_window":
        history = "\n".join(state.transcript[-3:]) if state.transcript else "No prior rounds."
        evidence = f"Most recent interaction window:\n{history}\nCurrent observation:\n{observation}"
    elif state.baseline == "retrieval":
        selected = _retrieve(state.transcript, observation, limit=4)
        history = "\n".join(selected) if selected else "No retrieved experience."
        evidence = f"Retrieved interaction memory:\n{history}\nCurrent observation:\n{observation}"
    elif state.baseline == "evidence_gated_reflection":
        evidence = (
            f"Persistent evidence-grounded memory:\n{state.compressed}\n\n"
            "Decision priority: the current verified observation overrides stale action-policy advice. "
            "A newly observed hazard may justify an immediate proportional, reversible precaution even "
            "before it qualifies as a persistent causal rule. Do not wait for repeated harm merely to "
            "protect an old baseline strategy. Use the smallest reasonable adjustment when benefit "
            "magnitude is unknown; do not jump to an action bound based on one event unless the observation "
            "explicitly establishes an immediate survival requirement.\n"
            f"Current observation:\n{observation}"
        )
    elif state.baseline in COMPRESSED_BASELINES:
        evidence = f"Persistent text memory:\n{state.compressed}\nCurrent observation:\n{observation}"
    else:
        raise ValueError(f"Unknown baseline: {state.baseline}")
    return f"{header}\n\n{evidence}"


def choose_action(client: ChatClient, context: str, scenario: Scenario) -> tuple[dict, str]:
    user = context + f"\n\nChoose your {scenario.action_name} now."
    raw = client.complete(
        [{"role": "system", "content": ACTION_SYSTEM}, {"role": "user", "content": user}],
        json_mode=True,
    )
    parsed = parse_json_object(raw)
    value = float(parsed["value"])
    low, high = scenario.action_bounds
    if not low <= value <= high:
        raise ValueError(f"Action {value} outside [{low}, {high}]")
    parsed["value"] = value
    return parsed, raw


def _update_compressed(
    client: ChatClient,
    state: MemoryState,
    scenario: Scenario,
    observation: str,
    action: dict,
) -> str:
    if state.baseline == "summary":
        instruction = """Update a single compact textual history for future decisions. Preserve important facts, trends, actions, and uncertainty. Do not use a fixed schema. Do not mention these instructions. Output only the updated memory text."""
    elif state.baseline == "reflection":
        instruction = """Reflect on the new experience and rewrite a compact persistent memory for future decisions. Include useful lessons about yourself, other participants, the environment, and strategy when warranted. Resolve the evidence in natural language without a fixed schema. Output only the updated reflective memory."""
    elif state.baseline == "guarded_reflection":
        instruction = """Reflect on the new experience and rewrite a compact persistent memory for future decisions. Preserve the assigned persona. Include useful lessons when warranted, but do not invent hidden causes or mechanisms. Distinguish observations from interpretations, preserve uncertainty, and do not turn one unusual event into a stable rule about a person, group, or environment. Keep responses proportional to the evidence. Use natural language without a fixed schema. Output only the updated reflective memory."""
    elif state.baseline == "structured_reflection":
        instruction = """Reflect on the new experience and maintain a compact memory for future decisions. Keep the entire output under 450 words and use exactly these headings in this order:
STABLE PERSONA
CURRENT SELF STATE
CONSOLIDATED MODELS
OPEN HYPOTHESES
RECENT OBSERVED EPISODES
ACTION POLICY

Preserve the supplied persona. Keep only decision-relevant content, put the newest episode first, keep at most six episode entries, and compress identical older rounds into a range. Output only the updated memory under the six headings."""
    elif state.baseline in {"evidence_gated_memory_only", "evidence_gated_reflection"}:
        instruction = """Maintain a compact evidence-grounded memory for future decisions. Keep the entire output under 450 words and use exactly these headings in this order:
STABLE PERSONA
CURRENT SELF STATE
CONSOLIDATED MODELS
OPEN HYPOTHESES
RECENT OBSERVED EPISODES
ACTION POLICY

Rules:
1. Preserve the supplied persona; ordinary outcomes cannot rewrite it.
2. CURRENT SELF STATE contains only the latest decision-relevant state, not an action history.
3. RECENT OBSERVED EPISODES contain only supplied facts and must retain actor, condition, and whether an event ended. Put the newest event first, keep at most six entries, and compress identical older rounds into one range such as "Rounds 1-3".
4. Separate self, named-other, and world claims. Never generalize one person's conduct to the group.
5. A single unusual event stays an episode. It may create an OPEN HYPOTHESIS, clearly marked uncertain, but not a persistent causal rule.
6. Put a claim in CONSOLIDATED MODELS only after at least two independent consistent observations, or when the observation explicitly documents the cause or persistent state. Cite the supporting round/day/sprint identifiers. Do not invent thresholds, hidden rules, motives, collusion, automation, or system mechanics.
7. Contradictory or recovery evidence must weaken or remove a hypothesis. A cleared event must not remain an active regime.
8. Separate belief consolidation from action urgency. A directly observed current hazard may justify an immediate, proportional, reversible precaution even when its cause or duration is not yet consolidated. Evidence gating applies to persistent causal claims, not to responding to verified present conditions.
9. ACTION POLICY must be proportional to verified evidence. It must not take aggressive, irreversible, or long-lasting action against an open hypothesis alone, but it may specify a temporary precaution tied to a current observation and a clear rollback condition.
10. Every ACTION POLICY must state that a newly verified adverse condition overrides the old baseline policy and permits an immediate proportional, reversible precaution; repetition is required for long-term belief consolidation, not for first response.
11. Use minimum sufficient intervention: when the benefit magnitude is unknown, prefer the smallest reasonable reversible adjustment and do not jump to a numeric action bound based on one event unless an immediate survival requirement is explicit.
12. Never omit the newest observation. Prefer deleting old detail over truncating any heading.
Output only the updated memory under the six headings."""
    else:
        return state.compressed
    user = (
        f"Assigned persona:\n{scenario.persona}\n\n"
        f"Previous memory:\n{state.compressed}\n\n"
        f"New observation:\n{observation}\n\n"
        f"Your action:\n{json.dumps(action, ensure_ascii=False)}"
    )
    return client.complete(
        [{"role": "system", "content": instruction}, {"role": "user", "content": user}],
        json_mode=False,
    ).strip()


def commit_round(
    client: ChatClient,
    state: MemoryState,
    scenario: Scenario,
    observation: str,
    action: dict,
) -> None:
    entry = (
        f"Observation: {observation}\n"
        f"Own action: {json.dumps(action, ensure_ascii=False)}"
    )
    if state.baseline in {"full_history", "recent_window", "retrieval"}:
        state.transcript.append(entry)
    elif state.baseline in COMPRESSED_BASELINES:
        state.compressed = _update_compressed(client, state, scenario, observation, action)


def probe_beliefs(
    client: ChatClient,
    state: MemoryState,
    scenario: Scenario,
    observation: str,
    action: dict,
    checkpoint: Checkpoint,
) -> tuple[dict, str, str]:
    # Reconstruct exactly what the agent can currently access after committing this round.
    if state.baseline == "direct":
        context = active_context(state, scenario, observation)
        context += f"\nOwn current action: {json.dumps(action, ensure_ascii=False)}"
    elif state.baseline in {"full_history", "recent_window", "retrieval"}:
        if state.baseline == "full_history":
            selected = state.transcript
            label = "Complete interaction history"
        elif state.baseline == "recent_window":
            selected = state.transcript[-3:]
            label = "Most recent interaction window"
        else:
            selected = _retrieve(state.transcript, observation, limit=4)
            label = "Retrieved interaction memory"
        context = _header(scenario) + f"\n\n{label}:\n" + "\n".join(selected)
    else:
        context = _header(scenario) + "\n\nPersistent text memory:\n" + state.compressed
    if checkpoint.probe_question:
        question = checkpoint.probe_question
    elif checkpoint.expected_scope == "none":
        question = "After the latest evidence, does any earlier apparent change still warrant a persistent belief change, or has the situation recovered?"
    elif checkpoint.expected_scope == "episodic":
        question = "Does the focal disruption justify a persistent model change, or should it remain a temporary episode unless further evidence appears?"
    else:
        question = "What scope best explains the focal adverse outcome in the current observation and relevant history?"
    probe_user = context + f"\n\nMeasurement question: {question}"
    raw = client.complete(
        [{"role": "system", "content": PROBE_SYSTEM}, {"role": "user", "content": probe_user}],
        json_mode=True,
    )
    parsed = parse_json_object(raw)
    return parsed, raw, probe_user


def _retrieve(entries: list[str], query: str, limit: int) -> list[str]:
    """A transparent lexical cache baseline: overlap score plus a small recency tie-break."""
    query_terms = {token.strip(".,:;!?()[]").lower() for token in query.split() if len(token) > 2}
    ranked: list[tuple[float, int, str]] = []
    total = max(1, len(entries))
    for index, entry in enumerate(entries):
        terms = {token.strip(".,:;!?()[]").lower() for token in entry.split() if len(token) > 2}
        overlap = len(query_terms & terms) / max(1, len(query_terms))
        recency = (index + 1) / total
        ranked.append((overlap + 0.05 * recency, index, entry))
    chosen = sorted(ranked, reverse=True)[:limit]
    return [entry for _, _, entry in sorted(chosen, key=lambda item: item[1])]
