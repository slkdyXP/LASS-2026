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


def config_from_env(project_root: Path, **overrides: object) -> tuple[ExperimentConfig, str]:
    load_dotenv(project_root / ".env")
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    values: dict[str, object] = {
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    }
    values.update({key: value for key, value in overrides.items() if value is not None})
    return ExperimentConfig(**values), api_key

