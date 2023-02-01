# Author: Alfred Lim
# Location: Singapore
# Date: 2021-11-27
# Task: apply vowel-centered slot-based coding scheme to orthography
# Reference: Lim, O'Brien, & Luca (submitted)

import re
import numpy as np
import pandas as pd
import sys

# Define function that finds the position of the first vowel
def first_orth_vowel(word, consecutive=False):
    # arg consecutive: indicate if we're looking for a 2nd vowel
    # return -1 if there's no vowel found
    i = 0   
    while i < len(word):
        # Look for vowel from left to right
        if word[i] in orth_vowels or (i != 0 and word[i] == 'y') or (len(word) == 1 and word[i] == 'y' and consecutive == False):
            return i
        i += 1
    return -1

orth_vowels = 'aeiou'

# Read in corpus data
data_df = pd.read_excel('corpus.xlsx',na_values='',keep_default_na=False)

# Loop through word list 
for x in range(data_df.shape[0]):
    # Rearrange orth to be vowel-centred '_ p l a _ n e _ _ _' (CCCVVCCCCC)
    word = str(data_df['Word'][x]) #get word
    vow_ind = first_orth_vowel(word) #get position of first vowel
    new_word = '' #init variable to store pattern

    # If vowel was found
    if vow_ind != -1:
        new_word = word[:vow_ind] 
        new_word = '_' * (3 - len(new_word)) + new_word + word[vow_ind] 

        # Check the next character after the vowel
        if vow_ind+1 == len(word): 
            # End of word
            new_word = new_word + '_' * 6
        elif first_orth_vowel(word[vow_ind+1], consecutive=True) == -1:
            # Next char is not an vowel
            new_word = new_word + '_'
            remaining = word[vow_ind+1:] + '_' * (5 - len(word[vow_ind+1:]))
            new_word = new_word + remaining
        else:
            # Next char is also an vowel
            new_word = new_word + word[vow_ind+1]
            remaining = word[vow_ind+2:] + '_' * (5 - len(word[vow_ind+2:]))
            new_word = new_word + remaining
    else:
        # No orth vowel
        new_word = ('_' * 3) + ('_' * 2) + word[0:] + '_' * (5 - len(word[0:]))
        
    # Write orth slot-based encoded pattern
    data_df.loc[x, 'OrthSlot'] = new_word  

# Write new Excel file
data_df.to_excel('corpus_&orthslot.xlsx')
