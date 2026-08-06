import json
from pathlib import Path

PATH = Path("data/seen_jobs.json")

def load_seen() -> set[str]:
    try:
        return set(json.loads(PATH.read_text(encoding="utf-8")).get("seen_jobs", []))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen(items: set[str]) -> None:
    PATH.parent.mkdir(parents=True, exist_ok=True)
    PATH.write_text(json.dumps({"seen_jobs": sorted(items)}, indent=2), encoding="utf-8")
