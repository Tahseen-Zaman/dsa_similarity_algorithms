from __future__ import annotations

def metaphone(word: str) -> str:
    """
    Simplified Metaphone (common rules; good practical accuracy).
    Uses '0' for 'TH' as in classic Metaphone.
    """
    if not word:
        return ""
    w = word.upper()

    # 1) Drop starting silent letters
    for silent in ("KN", "GN", "PN", "AE", "WR"):
        if w.startswith(silent):
            w = w[1:]
            break

    result = []
    i = 0
    prev = ""
    vowels = "AEIOU"
    while i < len(w):
        ch = w[i]

        # Skip duplicate letters (except C)
        if i > 0 and ch == prev and ch != "C":
            i += 1
            continue

        nxt = w[i + 1] if i + 1 < len(w) else ""
        nxt2 = w[i + 2] if i + 2 < len(w) else ""

        if ch in vowels:
            if i == 0:
                result.append(ch)
        elif ch == "B":
            if not (i == len(w) - 1 and prev == "M"):
                result.append("B")
        elif ch == "C":
            if nxt == "H":
                result.append("X"); i += 1
            elif nxt in "IEY":
                result.append("S")
            else:
                result.append("K")
        elif ch == "D":
            if nxt == "G" and nxt2 in "EIY":
                result.append("J"); i += 1
            else:
                result.append("T")
        elif ch == "G":
            if nxt == "H":
                if not (i > 0 and w[i - 1] not in vowels):  # "gh" -> F if after vowel; else drop
                    result.append("F")
                i += 1
            elif nxt == "N":
                # silent 'g' in "gn"
                pass
            elif nxt in "IEY":
                result.append("J")
            else:
                result.append("K")
        elif ch == "H":
            if prev in vowels and nxt in vowels:
                result.append("H")  # pronounced
            # else silent
        elif ch == "K":
            if prev != "C":
                result.append("K")
        elif ch == "P":
            result.append("F" if nxt == "H" else "P")
        elif ch == "Q":
            result.append("K")
        elif ch == "S":
            if nxt == "H":
                result.append("X"); i += 1
            elif w[i:i+3] in ("SIO", "SIA"):
                result.append("X"); i += 2
            else:
                result.append("S")
        elif ch == "T":
            if nxt == "H":
                result.append("0"); i += 1
            elif w[i:i+3] in ("TIO", "TIA"):
                result.append("X"); i += 2
            elif w[i:i+3] == "TCH":
                pass  # silent T
            else:
                result.append("T")
        elif ch == "V":
            result.append("F")
        elif ch == "W":
            if nxt in vowels:
                result.append("W")
        elif ch == "X":
            result.extend(("K", "S"))
        elif ch == "Y":
            if nxt in vowels:
                result.append("Y")
        elif ch == "Z":
            result.append("S")
        elif ch == "R" or ch == "L" or ch == "M" or ch == "N" or ch == "J" or ch == "F":
            result.append(ch)

        prev = ch
        i += 1

    # Drop vowels except first letter (already handled), collapse
    code = "".join(result)
    return code
