import numpy as np
import math

def fine_grained_permutations(sequence_data, data_std, alpha):
    """
    This function generates additional symbols based on the maximum difference of   
    The new symbol is added to the permutation to form a new symbol sequence.
    
    Parameters:
    sequence_data (np.ndarray): A 2D array of sequence data (n x m), where [:(n/2)-1] are data points and [(n/2):] is the corresponding permutation and m is the number of symbols.
    data_std (float): Standard deviation of the data, used to scale the maximum difference for generating new symbols.
    alpha (float): A scaling factor that determines how many new symbols are generated based on the maximum difference.
    
    Returns:
    symbols (np.ndarray): The unique symbols in the new sequence after adding the additional symbols.
    symbol_counts (np.ndarray): The counts of each unique symbol in the new sequence.
    """

    # Initialize an array to store the new symbols (one row, same number of columns as the original sequence)
    additional_elements = np.zeros((1, sequence_data.shape[1]))  # Shape: (1, m), where m is the number of observed permutations
    
    # Iterate through each permutation
    for i in range(sequence_data.shape[1]):
        # Calculate the difference between adjacent data points
        diff_array = sequence_data[1:int(sequence_data.shape[0] * 0.5), i] - sequence_data[0:int(sequence_data.shape[0] * 0.5) - 1, i]
        
        # Find the maximum absolute difference in the data points
        max_diff = max(abs(diff_array))
        
        # Calculate the new symbol based on the maximum difference, scaled by data_std * alpha
        additional_elements[0, i] = math.floor(max_diff / (data_std * alpha))

    # Concatenate the additional symbols with the permutations, creating new symbols
        symbol_sequence = np.concatenate((sequence_data[int(sequence_data.shape[0] * 0.5):, :], additional_elements), axis=0)
    
    # Find the unique symbols and their counts in the new symbol sequence (across colums)
    symbols, symbol_counts = np.unique(symbol_sequence, return_counts=True, axis=1)
                
    return symbols, symbol_counts/np.sum(symbol_counts)
