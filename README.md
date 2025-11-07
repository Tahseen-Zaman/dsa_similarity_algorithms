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