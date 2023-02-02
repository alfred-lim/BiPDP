# Author: Alfred Lim
# Location: Singapore
# Date: 2021-11-27
# Task: create binary phonological vectors for neural networks
# Reference: Lim, O'Brien, & Luca (submitted)

import re
import numpy as np
import pandas as pd
#pytorch
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim

# Get features of a phoneme
def phonemeToFeature(phoneme):
    #find matched row's phoneme, and convert row to list
    feature = feature_df[feature_df['ASCII'] == phoneme].iloc[0].tolist()
    print(feature)
    return feature[3:] #remove front headers

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def phonemeToTensor(pline):
    tensor = torch.zeros(max_phon_len, 1, n_feature)
    for li, phoneme in enumerate(pline):
        tensor[li][0][:] = torch.FloatTensor(phonemeToFeature(phoneme))
    return tensor
    
all_letters = 'abcdefghijklmnopqrstuvwxyz'
orth_vowels = 'aeiou'
phon_vowels = 'eaiERYyoAcuUVCW' #ASCII

n_feature = 28 #number of feature from Moran
max_phon_len = 8 #how many positionals slots for phoneme
n_output = n_feature * max_phon_len
n_letters = len(all_letters) #all possible letters
max_word_length = 10 #how many positionals slots for orth

#read in data with alignment included (tested with phonetisaurus-align)
data_df = pd.read_excel('corpus_&phonslot.xlsx',na_values='',keep_default_na=False)
feature_df = pd.read_excel('phonemes_features.xlsx')

data_df['ASCIIBin'] = ''

#loop through data 
for x in range(data_df.shape[0]):
    ascii_pat = str(data_df['PhonSlot'][x]) #get ASCII pattern
    print(ascii_pat)
    #convert phoneme (must be in list) to one-hot vector
    ascii_tensor = phonemeToTensor(list(ascii_pat))

    ascii_tensor = ascii_tensor.squeeze(1)
    ascii_tensor = ascii_tensor.view(1,-1)
    ascii_tensor = ascii_tensor.squeeze(0)
    ascii_np = ascii_tensor.numpy()   #to numpy for conversion from tensor to str
    ascii_np = ascii_np.astype(int)
    ascii_str = np.array2string(ascii_np)
    ascii_str = re.sub('[^0-9 ]+', '', ascii_str) #remove unwanted symbols due to conversion
    
    data_df.loc[x, 'PhonVector'] = ascii_str  #write ascii binaries

data_df.to_excel('corpus_&phonslot&phonvector.xlsx')
