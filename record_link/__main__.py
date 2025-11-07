
"""
uv run python -m recordlink "José López" "Jose Lopez"
"""
import argparse
from . import normalize, levenshtein, jaro_winkler, soundex, metaphone

def main():
    p = argparse.ArgumentParser()
    p.add_argument("a")
    p.add_argument("b")
    args = p.parse_args()
    a = normalize(args.a)
    b = normalize(args.b)
    print("a:", a)
    print("b:", b)
    print("levenshtein:", levenshtein(a, b))
    print("jaro_winkler:", jaro_winkler(a, b))
    print("soundex(a), soundex(b):", soundex(a), soundex(b))
    print("metaphone(a), metaphone(b):", metaphone(a), metaphone(b))

if __name__ == "__main__":
    main()
