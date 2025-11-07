from __future__ import annotations
from ..phonetic.soundex import soundex
from ..phonetic.metaphone import metaphone

def soundex_block_key(name: str) -> str:
    return soundex(name)

def metaphone_block_key(name: str) -> str:
    return metaphone(name)
