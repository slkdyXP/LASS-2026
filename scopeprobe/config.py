from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import os


def load_dotenv(path: Path) -> None:
    """Load a small KEY=VALUE dotenv file without third-party dependencies."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class ExperimentConfig:
    provider: str = "deepseek"
    model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com"
    temperature: float = 0.2
    max_tokens: int = 700
    timeout_seconds: int = 90
    retries: int = 4
    repeats: int = 5
    seed: int = 20260826

    def to_dict(self) -> dict:
        return asdict(self)


PROVIDER_ENV = {
    "deepseek": ("VIBEBABO_DEEPSEEK_API_KEY", "VIBEBABO_DEEPSEEK_MODEL", "deepseek-v4-flash"),
    "openai": ("VIBEBABO_OPENAI_API_KEY", "VIBEBABO_OPENAI_MODEL", "gpt-5.4-mini"),
    "claude": ("VIBEBABO_CLAUDE_API_KEY", "VIBEBABO_CLAUDE_MODEL", "claude-sonnet-4-6"),
    "qwen": ("DASHSCOPE_API_KEY", "DASHSCOPE_MODEL", "qwen-max"),
}


def config_from_env(
    project_root: Path,
    *,
    provider: str = "deepseek",
    **overrides: object,
) -> tuple[ExperimentConfig, str]:
    load_dotenv(project_root / ".env")
    load_dotenv(project_root / ".env.providers")
    load_dotenv(project_root / ".env.qwen")
    if provider not in PROVIDER_ENV:
        raise ValueError(f"Unknown provider: {provider}")
    key_env, model_env, default_model = PROVIDER_ENV[provider]
    legacy_key = os.getenv("DEEPSEEK_API_KEY", "") if provider == "deepseek" else ""
    use_direct_deepseek = provider == "deepseek" and os.getenv("DEEPSEEK_USE_DIRECT", "").lower() in {
        "1", "true", "yes"
    }
    api_key = (
        legacy_key if use_direct_deepseek else os.getenv(key_env, legacy_key)
    ).strip()
    base_url = (
        os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        if use_direct_deepseek
        else
        os.getenv(
            "DASHSCOPE_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        if provider == "qwen"
        else os.getenv(
            "VIBEBABO_BASE_URL",
            os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        )
    )
    values: dict[str, object] = {
        "provider": provider,
        "model": os.getenv(model_env, os.getenv("DEEPSEEK_MODEL", default_model) if provider == "deepseek" else default_model),
        "base_url": base_url,
    }
    values.update({key: value for key, value in overrides.items() if value is not None})
    return ExperimentConfig(**values), api_key
