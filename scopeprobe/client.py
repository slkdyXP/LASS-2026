from __future__ import annotations

import json
from datetime import datetime, timezone
import os
from pathlib import Path
import random
import time
from http.client import RemoteDisconnected
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ChatClient(Protocol):
    def complete(self, messages: list[dict[str, str]], *, json_mode: bool = False) -> str: ...


class ModelResponseError(Exception):
    """A billed model response was empty or violated the requested JSON contract."""


class DeepSeekClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        temperature: float,
        max_tokens: int,
        timeout_seconds: int,
        retries: int,
        provider: str = "deepseek",
        usage_log_path: Path | None = None,
        usage_metadata: dict[str, Any] | None = None,
    ) -> None:
        self.api_key = api_key
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.provider = provider
        self.usage_log_path = usage_log_path
        self.usage_metadata = dict(usage_metadata or {})

    def complete(self, messages: list[dict[str, str]], *, json_mode: bool = False) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        if self.provider == "deepseek":
            # V4 defaults to high-effort thinking, which can exhaust max_tokens
            # before producing final JSON. The registered experiments use the
            # non-thinking decision model, matching the earlier DeepSeek runs.
            payload["thinking"] = {"type": "disabled"}
        request = Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        last_error: Exception | None = None
        for attempt in range(self.retries):
            try:
                with urlopen(request, timeout=self.timeout_seconds) as response:
                    data = json.loads(response.read().decode("utf-8"))
                content = data["choices"][0]["message"].get("content") or ""
                valid_content = bool(content.strip())
                if valid_content and json_mode:
                    try:
                        parse_json_object(content)
                    except (json.JSONDecodeError, ValueError):
                        valid_content = False
                self._log_usage(
                    data,
                    messages,
                    attempt=attempt + 1,
                    valid_content=valid_content,
                )
                if not valid_content:
                    raise ModelResponseError("empty or malformed JSON model response")
                return content
            except (
                HTTPError,
                URLError,
                ConnectionError,
                RemoteDisconnected,
                TimeoutError,
                KeyError,
                json.JSONDecodeError,
                ModelResponseError,
            ) as exc:
                last_error = exc
                if attempt + 1 < self.retries:
                    time.sleep(min(8.0, (2**attempt) + random.random()))
        raise RuntimeError(f"DeepSeek request failed after {self.retries} attempts: {last_error}")

    def _log_usage(
        self,
        data: dict[str, Any],
        messages: list[dict[str, str]],
        *,
        attempt: int,
        valid_content: bool,
    ) -> None:
        if self.usage_log_path is None:
            return
        usage = data.get("usage") if isinstance(data.get("usage"), dict) else {}
        system = messages[0].get("content", "") if messages else ""
        if "structured event parser" in system:
            call_kind = "event_parser"
        elif "reporting the participant's current beliefs" in system:
            call_kind = "belief_probe"
        elif "conservative evaluator" in system:
            call_kind = "external_evaluator"
        elif "conservative forensic annotator" in system:
            call_kind = "claim_audit"
        elif "autonomous participant" in system:
            call_kind = "action"
        else:
            call_kind = "memory_update_or_other"
        record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "provider": self.provider,
            "requested_model": self.model,
            "resolved_model": data.get("model"),
            "call_kind": call_kind,
            "attempt": attempt,
            "valid_content": valid_content,
            "finish_reason": (data.get("choices") or [{}])[0].get("finish_reason"),
            "content_chars": len(
                ((data.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
            ),
            "prompt_tokens": int(usage.get("prompt_tokens", 0) or 0),
            "completion_tokens": int(usage.get("completion_tokens", 0) or 0),
            "total_tokens": int(usage.get("total_tokens", 0) or 0),
            "cache_hit_tokens": int(
                usage.get(
                    "prompt_cache_hit_tokens",
                    (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0),
                )
                or 0
            ),
            "reasoning_tokens": int(
                (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0
            ),
            "response_id": data.get("id"),
            **self.usage_metadata,
        }
        payload = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
        self.usage_log_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.usage_log_path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            os.write(fd, payload)
        finally:
            os.close(fd)


def parse_json_object(text: str) -> dict[str, Any]:
    """Parse a JSON response, tolerating fenced output and surrounding prose."""
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        stripped = "\n".join(lines[1:-1]).strip()
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        start, end = stripped.find("{"), stripped.rfind("}")
        if start < 0 or end <= start:
            raise
        value = json.loads(stripped[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value
