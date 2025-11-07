from record_link import normalize, levenshtein, jaro_winkler, soundex, metaphone, Scorer


def main():
    a, b = normalize("A. K. Rahman"), normalize("Abdul Karim Rahman")
    print("lev:", levenshtein(a, b))
    print("jw :", jaro_winkler(a, b))
    print("sx :", soundex("Rahman"), soundex("Rohman"))
    print("mp :", metaphone("Knight"), metaphone("Night"))
    print("score:", Scorer(weights={"jw": 0.7, "lev": 0.3}).score(a, b))


if __name__ == "__main__":
    main()
