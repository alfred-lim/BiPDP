# Author: Alfred Lim
# Location: Singapore
# Date: 2021-11-27
# Task: create binary orthographic vectors for neural networks
# Reference: Lim, O'Brien, & Luca (submitted)

## Import libraries
import re
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim

# Find letter position index, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(max_word_length, 1, n_letters)
    for li, letter in enumerate(line):
        # Check if slot is empty
        if letter != '_': 
            tensor[li][0][letterToIndex(letter)] = 1
    return tensor
    
all_letters = 'abcdefghijklmnopqrstuvwxyz'
orth_vowels = 'aeiou'
phon_vowels = 'eaiERYyoAcuUVCW' #ASCII

n_feature = 28 #number of feature from Moran
max_phon_len = 8 #how many positionals slots for phoneme
n_output = n_feature * max_phon_len
n_letters = len(all_letters) #all possible letters
max_word_length = 10 #how many positionals slots for orth

# Read word list
data_df = pd.read_excel('MALD_monoSyl&Phon&Ascii&Pat.xlsx',na_values='',keep_default_na=False)

# Loop word-by-word
for x in range(data_df.shape[0]):
    # Get orthographic vowel centered pattern
    orth_pat = str(data_df['OrthPat'][x])
    print(orth_pat)

    # Convert to binary one-hot vector by making use of PyTorch
    orth_tensor = lineToTensor(orth_pat) 
    orth_tensor = orth_tensor.view(1,-1)
    orth_tensor = orth_tensor.squeeze(0)
    orth_tensor = orth_tensor.int()

    # Convert resulted PyTorch tensor object to string
    orth_np = orth_tensor.numpy()
    orth_np = orth_np.astype(int)
    orth_str = np.array2string(orth_np)
    # Remove unwanted symbols due to conversion (e.g., new line char)
    orth_str = re.sub('[^0-9 ]+', '', orth_str) 
    data_df.loc[x, 'OrthBin'] = orth_str  

# Write to Excel file
data_df.to_excel('word_list.xlsx')
