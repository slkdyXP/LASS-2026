from __future__ import annotations
import json, os, time, urllib.error, urllib.request

def complete(config: dict, messages: list[dict[str,str]]) -> str:
    key = os.environ.get(config["api_key_env"], "")
    if not key: raise RuntimeError(f"Missing API key env: {config['api_key_env']}")
    payload = {"model":config["model"], "messages":messages, "temperature":config.get("temperature",.7), "max_tokens":config.get("max_tokens",500)}
    if config.get("disable_thinking"): payload["thinking"]={"type":"disabled"}
    last = None
    for attempt in range(config.get("request_retries",8)):
        req=urllib.request.Request(config["base_url"].rstrip("/")+"/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=config.get("request_timeout_seconds",60)) as response: body=json.loads(response.read().decode())
            text=body["choices"][0]["message"].get("content","")
            if isinstance(text,str) and text.strip(): return text
            raise RuntimeError("empty model content")
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, TypeError, ValueError, RuntimeError) as exc:
            last=exc
            if attempt+1 < config.get("request_retries",8): time.sleep(min(30, 2*(attempt+1)))
    raise RuntimeError(f"model request failed: {last}")
