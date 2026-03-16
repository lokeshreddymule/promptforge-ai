import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional


# Simple file-based memory (no vector DB required to run)
MEMORY_FILE = Path(__file__).parent.parent / "memory" / "prompt_store.json"


def _load_store() -> list:
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def _save_store(data: list):
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_prompt(
    original_prompt: str,
    optimized_prompt: str,
    prompt_type: str,
    original_score: float,
    optimized_score: float,
):
    """Save a prompt pair to memory."""
    store = _load_store()
    entry = {
        "id": len(store) + 1,
        "timestamp": datetime.now().isoformat(),
        "prompt_type": prompt_type,
        "original_prompt": original_prompt,
        "optimized_prompt": optimized_prompt,
        "original_score": original_score,
        "optimized_score": optimized_score,
        "improvement": round(optimized_score - original_score, 1),
    }
    store.append(entry)
    _save_store(store)
    return entry


def get_all_prompts() -> list:
    """Get all stored prompts."""
    return _load_store()


def get_best_prompts(limit: int = 5) -> list:
    """Get top prompts by optimized score."""
    store = _load_store()
    sorted_store = sorted(store, key=lambda x: x.get("optimized_score", 0), reverse=True)
    return sorted_store[:limit]


def get_prompts_by_type(prompt_type: str) -> list:
    """Get prompts filtered by type."""
    store = _load_store()
    return [p for p in store if p.get("prompt_type", "").lower() == prompt_type.lower()]


def get_stats() -> dict:
    """Get overall statistics."""
    store = _load_store()
    if not store:
        return {"total": 0, "avg_improvement": 0, "best_score": 0}

    improvements = [p.get("improvement", 0) for p in store]
    scores = [p.get("optimized_score", 0) for p in store]

    return {
        "total": len(store),
        "avg_improvement": round(sum(improvements) / len(improvements), 1),
        "best_score": max(scores),
        "avg_score": round(sum(scores) / len(scores), 1),
    }


def clear_memory():
    """Clear all stored prompts."""
    _save_store([])
