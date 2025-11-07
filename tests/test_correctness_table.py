# Python
from math import isclose
from record_link import levenshtein, jaro_winkler

cases = [
    ("martha", "marhta", 0.961, 2),   # JW≈0.961, Lev=2
    ("dwayne", "duane",  0.84,  2),
    ("dixon",  "dicksonx", 0.81, 4),
    ("kitten", "sitting", None, 3),
]

def test_table_values():
    for a, b, jw_exp, lev_exp in cases:
        if jw_exp is not None:
            assert isclose(round(jaro_winkler(a, b), 3), jw_exp, rel_tol=0, abs_tol=0.005)
        assert levenshtein(a, b) == lev_exp
