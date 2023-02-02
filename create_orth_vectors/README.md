# Create orthographic vectors

This file documents use of create_orth_vectors.py for the purpose of creating binary orthographic vectors of words to be used in neural networks. 

# Coding scheme
We used a position sensitive slot-based vowel-centered format for orthographic representation (e.g., Harm & Seidenberg, 1999, 2004).

The orthographic layer comprises of 260 units, corresponding to 10 letter position slots × 26 possible letters. Words are coded as vowel-centred, such that the fourth slot was filled with the left-most vowel of a word (e.g., yap → _ _ y a p _ _ _ _ _ )

<img src="orth_coding_scheme.png" width="500">

# Usage
First, use the Python script [create_orth_slots.py](create_orth_slots.py) create_orth_slots.py to convert words to slot-based orthographic representations. This will add a new _OrthSlot_ column to the corpus Excel file.

Then, use the Python script [create_orth_vectors.py](create_orth_vectors.py) create_orth_vectors.py to convert slot-based orthograhic representations to binary vectors. This will add a new _OrthVector_ column to the corpus Excel file.

## Required files
* Python files (create_orth_slots.py, create_orth_vector.py)
* Corpus file (corpus.xlsx)

If you need a sample corpus file, you may use the one published in our [OSF repository](https://osf.io/wdzqc/?view_only=d6ef4592811441779ce7e8801dec805d).
