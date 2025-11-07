import random
import string
from record_link import levenshtein, jaro_winkler, soundex, metaphone

RNG = random.Random(1337)

def _words(n=1000, size=12):
    for _ in range(n):
        yield "".join(RNG.choice(string.ascii_lowercase) for _ in range(size))

def test_perf_levenshtein(benchmark):
    pairs = [(w, w[::-1]) for w in _words(200, 20)]
    def run():
        s = 0
        for a, b in pairs:
            s += levenshtein(a, b)
        return s
    benchmark(run)

def test_perf_jw(benchmark):
    pairs = [(w, w[::-1]) for w in _words(400, 12)]
    benchmark(lambda: sum(jaro_winkler(a, b) for a, b in pairs))

def test_perf_soundex(benchmark):
    words = list(_words(10_000, 10))
    benchmark(lambda: [soundex(w) for w in words])

def test_perf_metaphone(benchmark):
    words = list(_words(5_000, 10))
    benchmark(lambda: [metaphone(w) for w in words])
