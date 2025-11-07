from __future__ import annotations
import unicodedata
from dataclasses import dataclass
import re

def _strip_accents(s: str) -> str:
    nkfd = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in nkfd if not unicodedata.combining(ch))

def normalize(s: str) -> str:
    """Unicode NFKC → casefold → accent-strip → keep alnum/space → collapse spaces."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s).casefold()
    s = _strip_accents(s)
    s = re.sub(r"[^0-9a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

@dataclass(frozen=True)
class Normalizer:
    keep_chars: str = ""  # e.g., "-'" if you wish
    def apply(self, s: str) -> str:
        pat = rf"[^0-9a-z\s{re.escape(self.keep_chars)}]"
        t = unicodedata.normalize("NFKC", s).casefold()
        t = _strip_accents(t)
        t = re.sub(pat, " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t
