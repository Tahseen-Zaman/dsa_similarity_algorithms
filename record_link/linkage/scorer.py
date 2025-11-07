from __future__ import annotations
from dataclasses import dataclass
from ..metrics.levenshtein import levenshtein
from ..metrics.jaro import jaro_winkler

def _lev_sim(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    d = levenshtein(a, b)
    m = max(len(a), len(b))
    return 1.0 - (d / m) if m else 1.0

@dataclass(frozen=True)
class Scorer:
    """Weighted similarity: jw (Jaro–Winkler), lev (Levenshtein-normalized)."""
    weights: dict[str, float] = None

    def __post_init__(self):
        if self.weights is None:
            object.__setattr__(self, "weights", {"jw": 1.0})

    def score(self, a: str, b: str) -> float:
        w = self.weights
        parts = []
        if "jw" in w:
            parts.append(w["jw"] * jaro_winkler(a, b))
        if "lev" in w:
            parts.append(w["lev"] * _lev_sim(a, b))
        denom = sum(w.get(k, 0.0) for k in ("jw", "lev"))
        return (sum(parts) / denom) if denom else 0.0
