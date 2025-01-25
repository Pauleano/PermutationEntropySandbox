import numpy as np

import numpy as np

def coded_permutations(seq_data):
    """
    Implements symbolization according to coded permutation entropy.

    Input:
    - seq_data (numpy.ndarray): A 2D NumPy array (nxm) where rows[0:(n/2)-1] correspond to data points and rows[n/2:n-1] corresponds to permutation at each instance 
                            
    Output:
    - symbols (numpy.ndarray): A 1D array of unique symbols found in the concatenated sequence of permutations and coded values.
    - symbol_counts (numpy.ndarray): A 1D array with counts of how many times each unique symbol appears in the concatenated sequence.
    """
    
    
    
    #Extract permutations
    permutation_sequence = seq_data[int(seq_data.shape[0] * 0.5):, :]
    
    #Identify unique permutations, their indexes and counts 
    unique_permutation, permutation_indices, permutation_counts = np.unique(permutation_sequence.T, axis=0, return_inverse=True, return_counts=True)
    
    #Initialize a matrix to store the averages for each permutation
    symbol_averages = np.zeros((int(seq_data.shape[0] * 0.5), len(unique_permutation)))
    
    #Calculate the average for each permutation at each position
    for i in range(seq_data.shape[1]):
        symbol_index = permutation_indices[i]
        symbol_averages[:, symbol_index] += seq_data[:int(seq_data.shape[0] * 0.5), i]

    #Calculate the average by dividing by the counts of each symbol
    symbol_averages = symbol_averages / permutation_counts

    #Initialize the coded_array which will store the coded values ('+', '-', or '0')
    coded_array = np.zeros((int(seq_data.shape[0] * 0.5), seq_data.shape[1]), dtype=str)
    
    #Compare datapoints with the corresponding permutation averages
    #Assign '+', '-', or '0' depending on whether the value is greater than, less than, or equal to the average
    for i in range(seq_data.shape[1]):
        symbol_index = permutation_indices[i]
        diff = seq_data[:int(seq_data.shape[0] * 0.5), i] - symbol_averages[:, symbol_index]
        coded_array[:, i] = np.where(diff > 0, '+', np.where(diff < 0, '-', '0'))

    #Concatenate the coded_array to the permutation_sequence
    symbol_sequence = np.concatenate((permutation_sequence, coded_array), axis=0)
    
    #Identify the unique symbols in the concatenated sequence along axis 1 (horizontal scan)
    symbols, symbol_counts = np.unique(symbol_sequence, axis=1, return_counts=True)
    
    return symbols, symbol_counts
