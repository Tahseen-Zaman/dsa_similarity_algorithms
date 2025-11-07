# Python
from record_link import jaro_winkler, levenshtein, soundex, metaphone
from record_link import normalize

def test_jw_prefix_bias_can_mislead():
    # Long different tails with same prefix get a bump
    a = "johnathan_something_long"
    b = "johnny_different_tail"
    # # The strings include an underscore; JW treats it as a character, lowering both matches and the prefix bonus.
    # a = normalize(a)
    # b = normalize(b)
    jw = jaro_winkler(a, b)
    # JW is comparatively high despite semantic mismatch, ~0.7929
    assert jw > 0.79

def test_levenshtein_penalizes_transpose_heavily():
    # Single adjacent swap counts as 1 (Damerau) but 2 in plain Levenshtein
    a, b = "ca", "ac"
    assert levenshtein(a, b) == 2

def test_phonetics_collapse_distinct_names():
    # Same code for different names → useful for blocking, not final matching
    assert soundex("Smith") == soundex("Smyth")
    assert metaphone("Steven") == metaphone("Stephen")

def test_phonetics_locale_limitations():
    # English-centric rules; may fail on non-English names
    code1 = metaphone("Xavier")     # could be Z/KS sounds
    code2 = metaphone("Javier")     # /h/ or /x/ Spanish
    assert isinstance(code1, str) and isinstance(code2, str)
