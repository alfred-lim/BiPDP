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
    
# Define all possible letters
all_letters = 'abcdefghijklmnopqrstuvwxyz'
# Define vowels
orth_vowels = 'aeiou'
# Get number of possible letters
n_letters = len(all_letters) 
# Define maximum positional slots
max_word_length = 10 

# Read word list
data_df = pd.read_excel('word_list_&orthslot.xlsx',na_values='',keep_default_na=False)

# Loop word-by-word
for x in range(data_df.shape[0]):
    # Get orthographic vowel centered pattern
    orth_slot = str(data_df['OrthSlot'][x])
    print(orth_slot)

    # Convert to binary one-hot vector by making use of PyTorch
    orth_tensor = lineToTensor(orth_slot) 
    orth_tensor = orth_tensor.view(1,-1)
    orth_tensor = orth_tensor.squeeze(0)
    orth_tensor = orth_tensor.int()

    # Convert resulted PyTorch tensor object to string
    orth_np = orth_tensor.numpy()
    orth_np = orth_np.astype(int)
    orth_str = np.array2string(orth_np)
    # Remove unwanted symbols due to conversion (e.g., new line char)
    orth_str = re.sub('[^0-9 ]+', '', orth_str) 
    data_df.loc[x, 'OrthVector'] = orth_str  

# Write to Excel file
data_df.to_excel('word_list_&orthslot&orthvector.xlsx')
