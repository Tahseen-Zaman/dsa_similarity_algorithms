# **RecordLink**

### *A lightweight Python toolkit for string similarity and phonetic algorithms in record linkage*

---

## **1. Goal and Vision**

Data from multiple sources rarely align perfectly—names are misspelled, addresses differ, formats vary. *RecordLink* aims to make linking such data transparent and reproducible by implementing core string similarity and phonetic algorithms from scratch in Python.
The goal is twofold:

1. Provide an educational, open, and well-documented reference implementation.
2. Serve as a foundation for scalable entity-resolution systems in research and industry domains such as healthcare, census, and customer analytics.

This project focuses on clarity, correctness, and extensibility rather than raw speed—each algorithm is implemented in readable Python to illustrate the underlying logic.

---

## **2. Theoretical Background**

### **2.1 Record Linkage & String Matching**

**Record Linkage** (or *Entity Resolution*) is the process of identifying records across datasets that refer to the same real-world entity (e.g., the same patient or customer), even when text fields differ slightly.
It combines **string matching** and **blocking**:

* *String Matching* quantifies similarity between individual fields (like names).
* *Blocking* groups potentially similar records to avoid O(n²) comparisons.

### **2.2 Algorithms Implemented**

**Levenshtein Distance**
Measures the minimal number of insertions, deletions, or substitutions needed to transform one string into another.
Example: `kitten → sitting` = 3 edits.
Used to capture *typo-level differences.*

**Jaro–Winkler Similarity**
Considers matching characters and transpositions within a variable window; Winkler extension rewards common prefixes.
Effective for *short names and transposed letters.*

**Soundex**
Encodes words into a 4-character alphanumeric code based on how they *sound* in English.
Example: `Smith → S530`, `Smyth → S530`.
Used for *phonetic blocking.*

**Metaphone**
Improved phonetic algorithm capturing more modern pronunciation patterns (e.g., `Knight` and `Night` → same code).
Better linguistic coverage than Soundex.

Together, these algorithms measure **edit distance**, **character similarity**, and **phonetic resemblance**—the core pillars of record linkage.

---

## **3. Project Structure**

```
recordlink/
  core/         # Normalization and text preprocessing
  metrics/      # Levenshtein and Jaro–Winkler similarity
  phonetic/     # Soundex and Metaphone encoders
  blocking/     # Blocking keys using phonetic codes
  linkage/      # Combined scorer for similarity weighting
  tests/        # Unit tests and examples
```


---
# How we developed our code in accordance with the theory:


## Levenshtein distance (edit distance)

**Idea**
Minimum number of single-character edits (insert, delete, substitute) to turn string A into B.

**Pseudocode (plain English)**

1. Make a 2D table `dp` of size `(len(A)+1) x (len(B)+1)`.
2. Initialize first row with `0..len(B)` (cost to insert B’s prefix), first column with `0..len(A)` (cost to delete A’s prefix).
3. For each `i=1..len(A)` and `j=1..len(B)`:

   * If `A[i-1] == B[j-1]`, set `cost = 0`, else `cost = 1`.
   * Set `dp[i][j] = min( dp[i-1][j] + 1 (delete), dp[i][j-1] + 1 (insert), dp[i-1][j-1] + cost (substitute) )`.
4. Answer is `dp[len(A)][len(B)]`.

**Complexity**: O(n·m) time, O(n·m) space (or O(min(n,m)) with row-rolling).
**Edge cases**: empty vs non-empty (distance = length of other); identical strings (0).
**Failure mode vs Damerau**: adjacent swaps count as 2 edits (not 1).

---

## Jaro and Jaro–Winkler similarity

**Idea**
Compare characters within a match window and penalize out-of-order matches (transpositions). Winkler adds a bonus for common prefixes. Returns a similarity in [0,1].

**Pseudocode (plain English)**

1. If A == B → return 1. If either empty → 0.
2. Match window = `floor(max(len(A), len(B)) / 2) - 1`, floored at 0.
3. Find matches:

   * For each char in A at index `i`, search in B from `i - window` to `i + window` for the same char that isn’t already matched.
   * Mark both positions matched and increment `matches`.
4. If `matches == 0` → return 0.
5. Count transpositions:

   * Iterate matched chars in order in A and B; count positions where the matched characters differ; `transpositions = count / 2`.
6. Jaro score = average of:

   * `matches / len(A)`, `matches / len(B)`, and `(matches - transpositions) / matches`.
7. Winkler bonus:

   * `l = length of common prefix of A and B up to 4`.
   * `JW = Jaro + l * p * (1 - Jaro)` with `p = 0.1` typically.

**Complexity**: O(n + m) with the sliding window; worst-case O(n·window).
**Edge cases**: works well for short names and transpositions; identical prefix increases score.
**Failure mode**: prefix bonus can make long, diverging strings look slightly too similar.

---

## Soundex (phonetic hash)

**Idea**
Encode an English name into a 4-character code: first letter + three digits representing consonant groups; collapses similar-sounding names.

**Pseudocode (plain English)**

1. Uppercase the input; keep only A–Z; if empty → return empty.
2. Keep the first letter as is.
3. For remaining letters, map each to a digit using groups:

   * BFPV→1, CGJKQSXZ→2, DT→3, L→4, MN→5, R→6; vowels and H/W/Y are “no digit”.
4. Drop consecutive duplicate digits (e.g., “BB” should not double-count “1”).
5. Remove all “no digit” markers.
6. Construct `first_letter + digits`, then:

   * Truncate to 4 chars, or pad with zeros to reach 4.
7. Return the 4-char code.

**Complexity**: O(n).
**Edge cases**: non-ASCII letters should be normalized first; empty → empty string.
**Failure mode**: very coarse—many different names share the same code (great for blocking, not for final matching).

---

## Metaphone (phonetic hash, richer than Soundex)

**Idea**
Encode a word into a consonant-like skeleton that approximates English pronunciation (handles silent letters, digraphs, and common patterns). Output length varies.

**Pseudocode (plain English)**

1. Uppercase word; optionally drop leading silent combos (KN, GN, PN, AE, WR).
2. Scan left→right with look-ahead (next 1–2 chars) and apply ordered rules:

   * Vowels: keep only if at start.
   * `PH → F`; `GH` → often `F` (depending on context) or silent; `KN/GN/PN` → drop leading consonant.
   * `CH → X` (like “sh”); `TIO/TIA → X`; `SH → X`.
   * `TH → 0` (special token).
   * `C` before `E/I/Y → S`, else `K`.
   * `DG` before `E/I/Y → J`; else `T`.
   * `Q → K`, `X → KS`, `V → F`, `Z → S`.
   * Drop repeated letters (except special cases like “CC”).
   * Keep sonorants `L, R, M, N, J` as themselves when pronounced.
3. Concatenate emitted symbols to form the code (no fixed length).
4. Return the code.

**Complexity**: O(n).
**Edge cases**: rules are English-centric; ambiguous cases (“Xavier”, “Javier”) vary by accent.
**Failure mode**: still collapses distinct names; not robust for non-English phonology. Double Metaphone (not implemented here) handles more cases by producing primary/alternate codes.

---

## How they fit together in record linkage

1. **Normalize** text first (Unicode normalize, case-fold, strip accents/punct, collapse spaces).
2. **Block** candidate pairs using phonetic keys (Soundex/Metaphone) to reduce comparisons.
3. **Compare** within blocks using Jaro–Winkler and/or Levenshtein.
4. **Score** (e.g., weighted average) and **threshold** to decide matches.
5. **Evaluate** with precision/recall; adjust normalization, weights, and thresholds.

---

## **4. Running Instructions**

### **Installation**

```bash
git clone https://github.com/yourusername/recordlink.git
cd recordlink
pip install -e .
pytest -q  # run tests
```

### **Usage**

```python
from recordlink import normalize, levenshtein, jaro_winkler, soundex, metaphone, Scorer

a, b = normalize("José López"), normalize("Jose Lopez")

print("Levenshtein:", levenshtein(a, b))
print("Jaro–Winkler:", jaro_winkler(a, b))
print("Soundex:", soundex("Robert"), soundex("Rupert"))
print("Metaphone:", metaphone("Knight"), metaphone("Night"))

scorer = Scorer(weights={"jw": 0.7, "lev": 0.3})
print("Combined score:", scorer.score(a, b))
```

---
## CLI Tool:

```
uv run python -m recordlink "José López" "Jose Lopez"
```
---

## **5. Expected Results and Interpretation**

| Function             | Output       | Meaning                                  |
| -------------------- | ------------ | ---------------------------------------- |
| `levenshtein(a, b)`  | Integer (≥0) | Number of edits required                 |
| `jaro_winkler(a, b)` | 0–1 float    | Similarity (1 = identical)               |
| `soundex(name)`      | 4-char code  | Phonetic code (for blocking)             |
| `metaphone(name)`    | String       | Pronunciation-based key                  |
| `Scorer.score(a,b)`  | 0–1 float    | Weighted similarity combining algorithms |

A *high Jaro–Winkler score* with *identical Soundex/Metaphone codes* strongly suggests two strings represent the same entity.

---

## **6. Unexplored Areas and Future Extensions**

The current release focuses on algorithmic clarity rather than full-scale linkage pipelines. Future extensions may include:

* **Double Metaphone** for multilingual phonetic encoding.
* **Damerau–Levenshtein** (handling transpositions).
* **Probabilistic linkage models** (Fellegi–Sunter framework).
* **Parallelized and vectorized computation** for large datasets.
* **Machine-learned similarity weighting** for adaptive scoring.

**RecordLink** is meant to bridge *theory and practice*—a toolkit for learning, experimenting, and eventually scaling real-world record.

---