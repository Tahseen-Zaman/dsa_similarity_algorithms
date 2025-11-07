from record_link import soundex, metaphone

def test_soundex():
    assert soundex("Robert") == "R163"
    assert soundex("Rupert") == "R163"
    assert soundex("Rubin")  == "R150"

def test_metaphone_common():
    assert metaphone("Smith").startswith("SM")  # typically "SM0"
    assert metaphone("Smyth").startswith("SM")
    assert "KS" in metaphone("Alex")           # X -> KS
