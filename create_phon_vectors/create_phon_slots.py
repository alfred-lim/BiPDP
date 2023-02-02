# Author: Alfred Lim
# Location: Singapore
# Date: 2021-11-27
# Task: apply vowel-centered slot-based coding scheme to phonology
# Reference: Lim, O'Brien, & Luca (submitted)

import re
import numpy as np
import pandas as pd
import sys

# Find the position of the first vowel
def first_phon_vowel(phon):
    i = 0   
    while i < len(phon):
        if phon[i] in phon_vowels:
            return i
        i += 1
    return -1
    
all_phonemes = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH',
                'ER','EY','F','G','HH','IH','IY','JH','K','L','M','N',
                'NG','OW','OY','P','R','S','SH','T','TH','UH','UW','V',
                'W','Y','Z','ZH']

phon_vowels = 'eaiERYyoAcuUVCW' #ASCII

n_phonemes = len(all_phonemes)
max_phoneme_length = 14
n_output = n_phonemes * max_phoneme_length

#read in data with alignment included (tested with phonetisaurus-align)
data_df = pd.read_excel('corpus.xlsx',na_values='',keep_default_na=False)
data_df['PhonSlot'] = ''

#loop through data 
for x in range(data_df.shape[0]):
    ascii_str = str(data_df['PhonASCII'][x]) #get ASCII phonemes

    #rearrange phonemes according to pattern encoding (e.g., _ _ m y n s _ _)
    vowel_ind = first_phon_vowel(ascii_str) #determine vowel for vowel-centre encoding
    n_pad_end = 4-len(ascii_str[vowel_ind+1:]) #determine how many spaces should be padded at the end (must have 4 chars after vowel)
    n_pad_front = 3-len(ascii_str[:vowel_ind]) #number of front spaces (must have 3 chars before vowel)
    ascii_pat = n_pad_front*'_' + ascii_str + n_pad_end*'_'
    data_df.loc[x, 'PhonSlot'] = ascii_pat  #write ascii slot-based encoded pattern

data_df.to_excel('corpus_&phonslot.xlsx')
