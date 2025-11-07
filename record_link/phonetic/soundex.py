from __future__ import annotations

_MAP = {
    **{c: "1" for c in "BFPV"},
    **{c: "2" for c in "CGJKQSXZ"},
    **{c: "3" for c in "DT"},
    "L": "4",
    **{c: "5" for c in "MN"},
    "R": "6",
}
_VOWELish = set("AEIOUYHW")

def soundex(name: str) -> str:
    """US Soundex (4 chars). Non A–Z dropped; returns '' for empty."""
    if not name:
        return ""
    # Keep first letter from raw ASCII-ish input
    letters = [ch for ch in name.upper() if "A" <= ch <= "Z"]
    if not letters:
        return ""
    first = letters[0]
    digits = []
    prev = _MAP.get(first, "")
    for ch in letters[1:]:
        code = _MAP.get(ch, "0" if ch in _VOWELish else "")
        if code and code != "0" and code != prev:
            digits.append(code)
        prev = code
    code = (first + "".join(digits))[:4]
    return code.ljust(4, "0")
