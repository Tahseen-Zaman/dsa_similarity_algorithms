from record_link import normalize

def test_normalize_basic():
    assert normalize("  José  López  ") == "jose lopez"
    assert normalize("") == ""
