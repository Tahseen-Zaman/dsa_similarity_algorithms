from __future__ import annotations
from math import floor

def jaro(s1: str, s2: str) -> float:
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0
    match_dist = max(len1, len2) // 2 - 1
    s1_match = [False] * len1
    s2_match = [False] * len2

    matches = 0
    for i, ch in enumerate(s1):
        start = max(0, i - match_dist)
        end = min(i + match_dist + 1, len2)
        for j in range(start, end):
            if not s2_match[j] and s2[j] == ch:
                s1_match[i] = s2_match[j] = True
                matches += 1
                break
    if matches == 0:
        return 0.0

    t = 0
    k = 0
    for i in range(len1):
        if s1_match[i]:
            while not s2_match[k]:
                k += 1
            if s1[i] != s2[k]:
                t += 1
            k += 1
    transpositions = t / 2
    return (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0

def jaro_winkler(s1: str, s2: str, *, p: float = 0.1, max_prefix: int = 4) -> float:
    j = jaro(s1, s2)
    if j <= 0:
        return 0.0
    l = 0
    for a, b in zip(s1, s2):
        if a == b and l < max_prefix:
            l += 1
        else:
            break
    return j + l * p * (1.0 - j)
