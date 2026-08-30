from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import os
import re
from typing import Any

from .client import ChatClient, parse_json_object
from .scenarios import Scenario


EXTERNAL_CONTROLLER_BASELINE = "hscm_external_controller"

EVENT_EXTRACTOR_SYSTEM = """You are a conservative structured event parser for an external agent-memory controller.
Extract only information explicitly supplied in the current observation. Do not infer hidden causes, motives, stable traits, thresholds, coordination, or system rules. Reuse a known claim_key when the observation supports, contradicts, or resolves the same proposition. A claim is explicitly_documented only when the observation explicitly documents its cause or persistent state, not merely because a fact is written in the observation.

Return valid JSON only with exactly this schema:
{
  "self_updates": [{"field": "short_key", "value": "latest explicit value"}],
  "evidence": [{
    "claim_key": "stable_variable_key_without_round_or_value",
    "scope": "self|other|world",
    "subject": "self|world|named agent",
    "claim": "short proposition that could matter across rounds",
    "value": "current observed value or state",
    "evidence_role": "state|cause|behavior",
    "condition": "explicit condition or unconditional",
    "stance": "support|contradict|resolve",
    "explicitly_documented": false,
    "explicitly_persistent": false
  }],
  "episodes": [{
    "actor": "self|world|named agent|group",
    "scope": "self|other|world|episodic",
    "condition": "explicit condition or unconditional",
    "fact": "one concise observed fact",
    "resolved": false
  }],
  "hazard": {
    "status": "none|active|resolved",
    "scope": "self|other|world|episodic|none",
    "target_agent": "name or none",
    "description": "one concise verified condition or none",
    "verified": false,
    "persistence": "unknown|temporary|persistent"
  }
}

Use at most four evidence items and four episodes. A normal stable round may have no hazard. A named participant's explicitly condition-dependent emergency behavior is other-scoped and conditional, not a group trait. A documented facility, supply, generation, weather, or regeneration change is world-scoped. Recovery observations must use resolved=true and stance resolve when a known claim or event has ended."""

EVENT_EXTRACTOR_SYSTEM += """

Priority rule: when the observation contains a changed, adverse, causal, conditional, or resolved fact, allocate evidence and episode slots to those facts before repeated normal baselines or unchanged per-agent values. Never spend every available slot enumerating stable actors while omitting a documented environmental change, named-agent deviation, recovery notice, or active hazard."""

# Claim keys identify variables, not events or values. For example, use
# ``cooling_capacity`` in every cycle and put ``30`` or ``15`` in ``value``.
EVENT_EXTRACTOR_SYSTEM += """

Identity rule: claim_key MUST identify the same underlying variable across time. Never put a round, day, cycle, sprint, timestamp, or observed value in claim_key. Put the changing state in value. Examples: use claim_key=cooling_capacity with value=30 and later the same claim_key=cooling_capacity with value=15; use claim_key=bob_bid_policy with condition=health<=2, not bob_bid_day8. Reuse a catalog key whenever its variable and subject match. An ordinary repeated observation supports the current value. If the value changes, still reuse the same variable key; the external controller performs the state transition. evidence_role=cause only when the observation explicitly identifies that variable as a cause, not merely as an observed state or consequence."""


@dataclass(frozen=True)
class ExternalControllerConfig:
    long_event_threshold: int = 8
    long_char_threshold: int = 4000
    consolidation_threshold: int = 2
    max_episodes: int = 6
    max_catalog_items: int = 32

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


def external_controller_config_from_env() -> ExternalControllerConfig:
    return ExternalControllerConfig(
        long_event_threshold=int(os.getenv("HSCM_LONG_EVENT_THRESHOLD", "8")),
        long_char_threshold=int(os.getenv("HSCM_LONG_CHAR_THRESHOLD", "4000")),
        consolidation_threshold=int(os.getenv("HSCM_CONSOLIDATION_THRESHOLD", "2")),
        max_episodes=int(os.getenv("HSCM_MAX_EPISODES", "6")),
        max_catalog_items=int(os.getenv("HSCM_MAX_CATALOG_ITEMS", "32")),
    )


@dataclass
class EvidenceState:
    claim_key: str
    scope: str
    subject: str
    claim: str
    value: str
    evidence_role: str
    condition: str
    support_ids: list[str] = field(default_factory=list)
    contradiction_ids: list[str] = field(default_factory=list)
    resolved_ids: list[str] = field(default_factory=list)
    explicitly_documented: bool = False
    explicitly_persistent: bool = False
    prior_values: list[dict[str, Any]] = field(default_factory=list)

    @property
    def active(self) -> bool:
        return not self.contradiction_ids and not self.resolved_ids


@dataclass
class EpisodeState:
    actor: str
    scope: str
    condition: str
    fact: str
    resolved: bool
    start_step: int
    end_step: int

    def fingerprint(self) -> tuple[str, str, str, str, bool]:
        return (self.actor, self.scope, self.condition, self.fact, self.resolved)


@dataclass
class ExternalMemoryController:
    persona: str
    config: ExternalControllerConfig = field(default_factory=external_controller_config_from_env)
    step: int = 0
    cumulative_chars: int = 0
    long_gate_active: bool = False
    gate_activated_at: int | None = None
    gate_reason: str = "below_threshold"
    self_state: dict[str, str] = field(default_factory=dict)
    evidence_bank: dict[str, EvidenceState] = field(default_factory=dict)
    consolidated_keys: list[str] = field(default_factory=list)
    hypothesis_keys: list[str] = field(default_factory=list)
    episodes: list[EpisodeState] = field(default_factory=list)
    policy_mode: str = "MAINTAIN"
    policy_text: str = (
        "Follow the current verified equilibrium shown in the latest observation while monitoring. "
        "The last action is an audit record, not a recommendation."
    )
    last_hazard: dict[str, Any] = field(default_factory=dict)
    last_action: dict[str, Any] = field(default_factory=dict)
    last_packet: dict[str, Any] = field(default_factory=dict)

    def update(
        self,
        client: ChatClient,
        scenario: Scenario,
        observation: str,
        action: dict[str, Any],
    ) -> str:
        self.observe(client, scenario, observation)
        self.record_action(action)
        return self.render()

    def observe(self, client: ChatClient, scenario: Scenario, observation: str) -> str:
        packet = extract_event_packet(client, self, scenario, observation)
        self.apply_packet(packet, observation, {})
        return self.render()

    def record_action(self, action: dict[str, Any]) -> str:
        self.last_action = dict(action)
        return self.render()

    def apply_packet(
        self,
        packet: dict[str, Any],
        observation: str,
        action: dict[str, Any],
    ) -> None:
        self.step += 1
        self.cumulative_chars += len(observation)
        event_id = f"E{self.step}"
        self.last_packet = packet
        self._update_context_gate()

        hazard = packet.get("hazard") if isinstance(packet.get("hazard"), dict) else {}
        self.last_hazard = _normalize_hazard(hazard)

        for item in _list_of_dicts(packet.get("self_updates")):
            key = _clean_key(item.get("field", "state"))
            value = str(item.get("value", "unknown")).strip()
            if key and value:
                self.self_state[key] = value

        for item in _list_of_dicts(packet.get("evidence"))[:4]:
            self._apply_evidence(item, event_id)

        for item in _list_of_dicts(packet.get("episodes"))[:4]:
            self._append_episode(item)

        self._refresh_slow_memory()
        self._compile_policy()

    def _update_context_gate(self) -> None:
        if self.long_gate_active:
            return
        by_events = self.step >= self.config.long_event_threshold
        by_chars = self.cumulative_chars >= self.config.long_char_threshold
        if by_events or by_chars:
            self.long_gate_active = True
            self.gate_activated_at = self.step
            if by_events and by_chars:
                self.gate_reason = "event_and_context_threshold"
            elif by_events:
                self.gate_reason = "event_threshold"
            else:
                self.gate_reason = "context_threshold"

    def _apply_evidence(self, item: dict[str, Any], event_id: str) -> None:
        key = _clean_key(item.get("claim_key", ""))
        if not key:
            return
        scope = str(item.get("scope", "world")).strip().lower()
        if scope not in {"self", "other", "world"}:
            scope = "world"
        record = self.evidence_bank.get(key)
        value = str(item.get("value", "unknown")).strip() or "unknown"
        evidence_role = str(item.get("evidence_role", "state")).strip().lower()
        if evidence_role not in {"state", "cause", "behavior"}:
            evidence_role = "state"
        value_changed = False
        if record is None:
            record = EvidenceState(
                claim_key=key,
                scope=scope,
                subject=str(item.get("subject", "world")).strip() or "world",
                claim=str(item.get("claim", key.replace("_", " "))).strip(),
                value=value,
                evidence_role=evidence_role,
                condition=str(item.get("condition", "unconditional")).strip() or "unconditional",
            )
            self.evidence_bank[key] = record
        elif value != "unknown" and record.value != "unknown" and value != record.value:
            value_changed = True
            record.prior_values.append(
                {
                    "value": record.value,
                    "claim": record.claim,
                    "support_ids": list(record.support_ids),
                    "ended_at": event_id,
                }
            )
            record.value = value
            record.claim = str(item.get("claim", record.claim)).strip() or record.claim
            record.evidence_role = evidence_role
            record.condition = str(item.get("condition", record.condition)).strip() or record.condition
            record.support_ids = []
            record.contradiction_ids = []
            record.resolved_ids = []
            record.explicitly_documented = False
            record.explicitly_persistent = False
        stance = str(item.get("stance", "support")).strip().lower()
        # A present-valued variable observation always supports the new current
        # value. "resolve" applies to the previous episode, not to the new state.
        if value != "unknown" or value_changed:
            stance = "support"
        target = (
            record.contradiction_ids
            if stance == "contradict"
            else record.resolved_ids
            if stance == "resolve"
            else record.support_ids
        )
        if event_id not in target:
            target.append(event_id)
        # A parser cannot promote an ordinary stated number by merely calling it
        # "documented". Immediate consolidation is allowed only alongside a
        # verified current hazard/cause packet.
        explicit_allowed = bool(self.last_hazard.get("verified", False)) and evidence_role == "cause"
        record.explicitly_documented = record.explicitly_documented or (
            explicit_allowed and bool(item.get("explicitly_documented", False))
        )
        persistent_allowed = bool(self.last_hazard.get("verified", False)) and (
            self.last_hazard.get("persistence") == "persistent"
        )
        record.explicitly_persistent = record.explicitly_persistent or (
            persistent_allowed and bool(item.get("explicitly_persistent", False))
        )

    def _append_episode(self, item: dict[str, Any]) -> None:
        scope = str(item.get("scope", "episodic")).strip().lower()
        if scope not in {"self", "other", "world", "episodic"}:
            scope = "episodic"
        episode = EpisodeState(
            actor=str(item.get("actor", "world")).strip() or "world",
            scope=scope,
            condition=str(item.get("condition", "unconditional")).strip() or "unconditional",
            fact=str(item.get("fact", "Observed event")).strip() or "Observed event",
            resolved=bool(item.get("resolved", False)),
            start_step=self.step,
            end_step=self.step,
        )
        if self.episodes and self.episodes[0].fingerprint() == episode.fingerprint():
            self.episodes[0].end_step = self.step
        else:
            self.episodes.insert(0, episode)
        self.episodes = self.episodes[: self.config.max_episodes]

    def _refresh_slow_memory(self) -> None:
        if not self.long_gate_active:
            self.consolidated_keys = []
            self.hypothesis_keys = []
            return
        consolidated: list[str] = []
        hypotheses: list[str] = []
        for key, record in self.evidence_bank.items():
            if not record.active:
                continue
            enough = len(record.support_ids) >= self.config.consolidation_threshold
            explicit = record.explicitly_documented or record.explicitly_persistent
            if enough or explicit:
                consolidated.append(key)
            elif record.support_ids:
                hypotheses.append(key)
        self.consolidated_keys = consolidated
        self.hypothesis_keys = hypotheses

    def _compile_policy(self) -> None:
        hazard = self.last_hazard
        status = hazard.get("status", "none")
        verified = bool(hazard.get("verified", False))
        scope = hazard.get("scope", "none")
        persistence = hazard.get("persistence", "unknown")
        if status == "resolved":
            self.policy_mode = "ROLLBACK"
            self.policy_text = (
                "The focal adverse condition has resolved. Roll back temporary precautions now and follow "
                "the current verified normal equilibrium unless another verified hazard remains active. "
                "The last action is an audit record, not a baseline or recommendation."
            )
        elif status == "active" and verified and scope == "other":
            self.policy_mode = "TARGETED_RESPONSE"
            target = hazard.get("target_agent", "the named participant")
            self.policy_text = (
                f"Use a proportional, reversible response targeted only at {target}. Do not generalize "
                "the named participant's conduct to the group or rewrite the world model."
            )
        elif status == "active" and verified:
            persistent_mode = self.long_gate_active and persistence == "persistent"
            self.policy_mode = "PERSISTENT_ADAPT" if persistent_mode else "PRECAUTION"
            qualifier = (
                "The long-horizon gate is active and the persistent condition is documented."
                if persistent_mode
                else "Treat this as a verified current hazard without prematurely creating a long-term rule."
            )
            self.policy_text = (
                f"{qualifier} Override stale baseline advice with the smallest reasonable reversible "
                "adjustment. Do not jump to an action bound unless an immediate survival requirement is explicit."
            )
        else:
            self.policy_mode = "MAINTAIN"
            self.policy_text = (
                "Follow the current verified equilibrium shown in the latest observation while monitoring. "
                "Do not anchor on the last action: it is an audit record, not a recommendation. Do not change "
                "long-term beliefs or take aggressive action without verified evidence."
            )

    def render(self) -> str:
        gate = self._gate_description()
        self_lines = (
            [f"- {key}: {value}" for key, value in sorted(self.self_state.items())]
            or ["- No explicit decision-relevant self-state update."]
        )
        if self.long_gate_active:
            consolidated_lines = [
                _render_belief(self.evidence_bank[key], uncertain=False)
                for key in self.consolidated_keys
            ] or ["- No claim has met the consolidation gate."]
            hypothesis_lines = [
                _render_belief(self.evidence_bank[key], uncertain=True)
                for key in self.hypothesis_keys
            ] or ["- No unresolved open hypothesis."]
        else:
            consolidated_lines = [
                f"- DORMANT under Contextual Phase-Transition Gate ({gate}). Evidence remains episodic."
            ]
            hypothesis_lines = [
                f"- DORMANT under Contextual Phase-Transition Gate ({gate}). No short-horizon hypothesis is promoted."
            ]
        episode_lines = [_render_episode(item) for item in self.episodes] or ["- No observed episode."]
        last_action = self.last_action.get("value", "none")
        return "\n".join(
            [
                "STABLE PERSONA",
                self.persona,
                "",
                "CURRENT SELF STATE",
                *self_lines,
                "",
                "CONSOLIDATED MODELS",
                *consolidated_lines,
                "",
                "OPEN HYPOTHESES",
                *hypothesis_lines,
                "",
                "RECENT OBSERVED EPISODES",
                *episode_lines,
                "",
                "ACTION POLICY",
                f"- Mode: {self.policy_mode}",
                f"- Last action value: {last_action}",
                f"- {self.policy_text}",
            ]
        )

    def audit_snapshot(self) -> dict[str, Any]:
        return {
            "step": self.step,
            "cumulative_chars": self.cumulative_chars,
            "long_gate_active": self.long_gate_active,
            "gate_activated_at": self.gate_activated_at,
            "gate_reason": self.gate_reason,
            "config": self.config.to_dict(),
            "self_state": dict(self.self_state),
            "evidence_bank": {key: asdict(value) for key, value in self.evidence_bank.items()},
            "consolidated_keys": list(self.consolidated_keys),
            "hypothesis_keys": list(self.hypothesis_keys),
            "episodes": [asdict(value) for value in self.episodes],
            "policy_mode": self.policy_mode,
            "last_hazard": dict(self.last_hazard),
            "last_packet": self.last_packet,
        }

    def _gate_description(self) -> str:
        cfg = self.config
        if self.long_gate_active:
            return f"ACTIVE at E{self.gate_activated_at}; reason={self.gate_reason}"
        return (
            f"DORMANT: events={self.step}/{cfg.long_event_threshold}, "
            f"chars={self.cumulative_chars}/{cfg.long_char_threshold}"
        )


def extract_event_packet(
    client: ChatClient,
    controller: ExternalMemoryController,
    scenario: Scenario,
    observation: str,
) -> dict[str, Any]:
    # Keep parser context bounded at long horizons.  Slow-memory keys are kept
    # first and the remaining slots use the most recently introduced variables.
    records = list(controller.evidence_bank.values())
    priority_keys = set(controller.consolidated_keys) | set(controller.hypothesis_keys)
    priority = [item for item in records if item.claim_key in priority_keys]
    recent = [item for item in records if item.claim_key not in priority_keys]
    selected = (priority + recent[-controller.config.max_catalog_items :])[
        -controller.config.max_catalog_items :
    ]
    catalog = [
        {
            "claim_key": item.claim_key,
            "scope": item.scope,
            "subject": item.subject,
            "claim": item.claim,
            "value": item.value,
            "evidence_role": item.evidence_role,
            "condition": item.condition,
        }
        for item in selected
    ]
    user = (
        f"Role:\n{scenario.role}\n\n"
        f"Known claim catalog (reuse keys when applicable):\n{json.dumps(catalog, ensure_ascii=False)}\n\n"
        f"Current observation:\n{observation}"
    )
    raw = client.complete(
        [
            {"role": "system", "content": EVENT_EXTRACTOR_SYSTEM},
            {"role": "user", "content": user},
        ],
        json_mode=True,
    )
    return _normalize_packet(parse_json_object(raw))


def _normalize_packet(packet: dict[str, Any]) -> dict[str, Any]:
    episodes = _list_of_dicts(packet.get("episodes"))
    hazard = _normalize_hazard(
        packet.get("hazard") if isinstance(packet.get("hazard"), dict) else {}
    )
    # "Active" already means the conservative parser found a current adverse
    # condition. Require a same-scope observed episode, then verify it
    # deterministically instead of trusting a second stochastic LLM boolean.
    same_scope_episode = any(
        str(item.get("scope", "episodic")).strip().lower() == hazard["scope"]
        for item in episodes
    )
    if hazard["status"] == "active" and same_scope_episode:
        hazard["verified"] = True
    return {
        "self_updates": _list_of_dicts(packet.get("self_updates")),
        "evidence": _list_of_dicts(packet.get("evidence")),
        "episodes": episodes,
        "hazard": hazard,
    }


def _normalize_hazard(value: dict[str, Any]) -> dict[str, Any]:
    status = str(value.get("status", "none")).lower()
    if status not in {"none", "active", "resolved"}:
        status = "none"
    scope = str(value.get("scope", "none")).lower()
    if scope not in {"self", "other", "world", "episodic", "none"}:
        scope = "none"
    persistence = str(value.get("persistence", "unknown")).lower()
    if persistence not in {"unknown", "temporary", "persistent"}:
        persistence = "unknown"
    return {
        "status": status,
        "scope": scope,
        "target_agent": str(value.get("target_agent", "none")).strip() or "none",
        "description": str(value.get("description", "none")).strip() or "none",
        "verified": bool(value.get("verified", False)),
        "persistence": persistence,
    }


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _clean_key(value: Any) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")
    return key[:96]


def _render_belief(item: EvidenceState, *, uncertain: bool) -> str:
    status = "UNCERTAIN" if uncertain else "CONSOLIDATED"
    supports = ",".join(item.support_ids) or "none"
    return (
        f"- [{status}][{item.scope}][subject={item.subject}][role={item.evidence_role}] "
        f"{item.claim}; value={item.value}; "
        f"condition={item.condition}; support={supports}."
    )


def _render_episode(item: EpisodeState) -> str:
    event_range = f"E{item.start_step}" if item.start_step == item.end_step else f"E{item.start_step}-E{item.end_step}"
    ended = "yes" if item.resolved else "no"
    return (
        f"- [{event_range}][{item.scope}][actor={item.actor}] {item.fact}; "
        f"condition={item.condition}; ended={ended}."
    )
