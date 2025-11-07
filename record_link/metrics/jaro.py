from __future__ import annotations

def jaro(s1: str, s2: str) -> float:
    """Canonical Jaro per Winkler/US Census: correct windowing + transpositions."""
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0

    match_dist = max(len1, len2) // 2 - 1
    if match_dist < 0:
        match_dist = 0

    s1_matches = [False] * len1
    s2_matches = [False] * len2

    # Count matches
    matches = 0
    for i in range(len1):
        start = max(0, i - match_dist)
        end = min(i + match_dist + 1, len2)
        for j in range(start, end):
            if not s2_matches[j] and s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

    if matches == 0:
        return 0.0

    # Count transpositions (out-of-order matches)
    k = 0
    transpositions = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    transpositions /= 2

    return (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0


def jaro_winkler(s1: str, s2: str, *, p: float = 0.1, max_prefix: int = 4) -> float:
    """
    Winkler boost: add l * p * (1 - j), with l = common prefix length (<= max_prefix).
    Applies regardless of punctuation; identical to US Census variant.
    """
    j = jaro(s1, s2)
    if j == 0.0:
        return 0.0

    # Common prefix length
    l = 0
    limit = min(max_prefix, len(s1), len(s2))
    while l < limit and s1[l] == s2[l]:
        l += 1

    return j + l * p * (1.0 - j)
