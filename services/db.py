from typing import Dict, List

# Simple in-memory stores
users: List[dict] = []
courses: List[dict] = []
enrollments: List[dict] = []

# Auto-increment counters
_counters: Dict[str, int] = {"user": 0, "course": 0, "enrollment": 0}


def next_id(key: str) -> int:
    _counters[key] += 1
    return _counters[key]
