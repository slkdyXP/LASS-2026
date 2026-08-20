from __future__ import annotations
import random

def round_robin_pairs(agent_ids: list[str], seed: int, rounds: int) -> list[list[tuple[str, str]]]:
    """Seeded circle-method schedule: no repeated pair before round 19."""
    if len(agent_ids) % 2 or len(agent_ids) < 2:
        raise ValueError("An even number of at least two agents is required")
    items = agent_ids[:]
    random.Random(seed).shuffle(items)
    schedules = []
    for _ in range(rounds):
        schedules.append([(items[i], items[-1-i]) for i in range(len(items)//2)])
        items = [items[0], items[-1], *items[1:-1]]
    return schedules

def validate_schedule(schedule: list[list[tuple[str, str]]], agent_ids: list[str]) -> list[str]:
    errors = []
    seen: set[tuple[str, str]] = set()
    expected = set(agent_ids)
    for r, pairs in enumerate(schedule, 1):
        flat = [x for pair in pairs for x in pair]
        if len(pairs) != len(agent_ids)//2 or set(flat) != expected or len(flat) != len(set(flat)):
            errors.append(f"round {r}: not a perfect matching")
        for a, b in pairs:
            key = tuple(sorted((a,b)))
            if a == b: errors.append(f"round {r}: self pair")
            if key in seen: errors.append(f"round {r}: repeated pair {key}")
            seen.add(key)
    return errors
