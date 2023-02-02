# Author: Alfred Lim
# Location: Singapore
# Date: 2021-11-27
# Task: create binary phonological vectors for neural networks
# Reference: Lim, O'Brien, & Luca (submitted)

# Import libraries
import re
import numpy as np
import pandas as pd
# Make use of PyTorch for binary encoding
import torch

# Define function to get the features of a phoneme
def phonemeToFeature(phoneme):
    #find matched row's phoneme, and convert row to list
    feature = feature_df[feature_df['Phoneme_ASCII'] == phoneme].iloc[0].tolist()
    print(feature)
    return feature[1:] #remove front headers

# Define function that convert list of features to a binary vector
def phonemeToTensor(pline):
    tensor = torch.zeros(max_phon_len, 1, n_feature)
    for li, phoneme in enumerate(pline):
        tensor[li][0][:] = torch.FloatTensor(phonemeToFeature(phoneme))
    return tensor

# Define constants
phon_vowels = 'eaiERYyoAcuUVCW' #ASCII vowel phonemes
n_feature = 28                  #max number of phonological features
max_phon_len = 8                #max positional slots for phonemes
n_output = n_feature * max_phon_len #compute max size of binary vector

# Read word list
data_df = pd.read_excel('corpus_&phonslot.xlsx',na_values='',keep_default_na=False)
# Read list of phonological features
feature_df = pd.read_excel('phonological_features.xlsx')

# Init column to store vector
data_df['PhonVector'] = ''

# Loop word-by-word
for x in range(data_df.shape[0]):
    # Get phonological vowel centered pattern
    ascii_pat = str(data_df['PhonSlot'][x]) 
    print(ascii_pat)
    
    # Get phonological features of the phonemes
    ascii_tensor = phonemeToTensor(list(ascii_pat))
    # Convert to binary one-hot vector by making use of PyTorch
    ascii_tensor = ascii_tensor.squeeze(1)
    ascii_tensor = ascii_tensor.view(1,-1)
    ascii_tensor = ascii_tensor.squeeze(0)
    
    # Convert resulted PyTorch tensor object to string
    ascii_np = ascii_tensor.numpy()   
    ascii_np = ascii_np.astype(int)
    ascii_str = np.array2string(ascii_np)
    
    # Remove unwanted symbols due to conversion (e.g., new line char)
    ascii_str = re.sub('[^0-9 ]+', '', ascii_str) 
    data_df.loc[x, 'PhonVector'] = ascii_str  #write ascii binaries

# Write to Excel file
data_df.to_excel('corpus_&phonslot&phonvector.xlsx')
