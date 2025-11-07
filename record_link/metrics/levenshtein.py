from __future__ import annotations

def levenshtein(a: str, b: str, *, max_distance: int | None = None) -> int:
    """O(min(n,m)) memory DP. Optional early cutoff via max_distance."""
    if a == b:
        return 0
    n, m = len(a), len(b)
    if n == 0: return m
    if m == 0: return n
    # Ensure a is the shorter
    if n > m:
        a, b = b, a
        n, m = m, n
    prev = list(range(n + 1))
    for j in range(1, m + 1):
        curr = [j] + [0] * n
        bj = b[j - 1]
        for i in range(1, n + 1):
            cost = 0 if a[i - 1] == bj else 1
            curr[i] = min(
                prev[i] + 1,       # deletion
                curr[i - 1] + 1,   # insertion
                prev[i - 1] + cost # substitution
            )
        if max_distance is not None and min(curr) > max_distance:
            return max_distance + 1
        prev = curr
    return prev[-1]
