# Author: Alfred Lim
# Location: Singapore
# Date: 2021-11-27
# Task: build example files for Lens
# Reference: Lim, O'Brien, & Luca (submitted)

## Import libraries
import numpy as np
import pandas as pd
import random
import math
import time

## Define function that write example files for Lens
def write_examples(data, out_op, out_po):
    # data: word list dataframe
    # out_op: OP file object
    # out_po: PO file object

    ## Add header to set input/output event time to default
    # OP file
    np.savetxt(out_op, np.array(['defI:- actI:- defT:- actT:-']), fmt="%s")
    np.savetxt(out_op, np.array([';']), fmt="%s", newline='\n\n')
    # PO file
    np.savetxt(out_po, np.array(['defI:- actI:- defT:- actT:-']), fmt="%s")
    np.savetxt(out_po, np.array([';']), fmt="%s", newline='\n\n')
    
    ## Loop through word list
    for x in range(filtered_df.shape[0]):
        # Get word
        word = str(filtered_df['Word'][x])

        ## Write word to OP example file
        # Write word
        np.savetxt(out_op, np.array(['name: '+'{'+word+'}']), fmt="%s")
        np.savetxt(out_op, np.array(['freq: ']), fmt="%s", newline='')
        np.savetxt(out_op, np.array([filtered_df['Model_Frequency'][x]]), fmt="%s")
        np.savetxt(out_op, np.array(['1']), fmt="%s") #3 events
        # Write orthography representation
        np.savetxt(out_op, np.array(['I: (Orth)']), fmt="%s", newline='')
        np.savetxt(out_op, np.array([filtered_df['OrthBin'][x]]), delimiter=' ', fmt="%s")
        # Write phonological representation
        np.savetxt(out_op, np.array(['[*] T: (Phon)']), fmt="%s", newline='')
        np.savetxt(out_op, np.array([filtered_df['ASCIIBin'][x]]), delimiter=' ', fmt="%s")
        np.savetxt(out_op, np.array([';']), delimiter=' ', fmt="%s", newline='\n\n')

        ## Write word to PO example file
        # Write word
        np.savetxt(out_po, np.array(['name: '+'{'+word+'}']), fmt="%s")
        np.savetxt(out_po, np.array(['freq: ']), fmt="%s", newline='')
        np.savetxt(out_po, np.array([filtered_df['Model_Frequency'][x]]), fmt="%s")
        np.savetxt(out_po, np.array(['1']), fmt="%s") #3 events
        # Write phonological representation
        np.savetxt(out_po, np.array(['I: (Phon)']), fmt="%s", newline='')
        np.savetxt(out_po, np.array([filtered_df['ASCIIBin'][x]]), delimiter=' ', fmt="%s")
        # Write orthography representation
        np.savetxt(out_po, np.array(['[*] T: (Orth)']), fmt="%s", newline='')
        np.savetxt(out_po, np.array([filtered_df['OrthBin'][x]]), delimiter=' ', fmt="%s")
        np.savetxt(out_po, np.array([';']), delimiter=' ', fmt="%s", newline='\n\n')
