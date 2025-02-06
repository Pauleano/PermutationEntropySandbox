import numpy as np
import itertools as iter

def orientations_all_sorted_combinations(multivar_data, emb_dim, emb_delay):
    """
    This function computes the symbolic orientation for all combinations of embedded data points
    using determinant-based orientation analysis. Symbols are generated based on the sign of the 
    determinant of the matrix constructed from selected data points.
    
    Args:
    - multivar_data (ndarray): A 2D numpy array where rows represent features, and columns represent time points.
    - emb_dim (int): Embedding dimension, determining the number of points considered for each "symbol."
    - emb_delay (int): Delay between data points used to construct the embedding.
    
    Returns:
    - unique_symbols (ndarray): The unique symbols generated during the orientation computation.
    - symbol_count (ndarray): The count of each unique symbol.
    """
    
    # Create a string consisting of all indices
    zahlen = ''.join(str(m) for m in range(emb_dim))
    
    # Get all valid combinations of indices and convert them to integers
    iter_kombinations = iter.combinations(zahlen, multivar_data.shape[0] + 1)
    int_combinations = np.array([list(kombi) for kombi in iter_kombinations], dtype=int)

    # Initialize matrix for calculating the orientation (determinant)
    matrix = np.concatenate((np.ones((multivar_data.shape[0] + 1, 1)), 
                             np.zeros((multivar_data.shape[0] + 1, multivar_data.shape[0]))), axis=1)
    
    # List to store all generated symbols
    words = []

    # Iterate over the data to generate symbols based on orientations
    for i in range(multivar_data.shape[1] - (emb_dim - 1) * emb_delay):
        word = []

        # Extract the relevant points from the data based on embedding and delay
        relev_points = multivar_data[:, i:i + emb_dim * emb_delay:emb_delay]
        
        # Iterate over all combinations of indices (from int_combinations)
        for k in range(int_combinations.shape[0]):
            for l in range(int_combinations.shape[1]):
                # Update the matrix with relevant data points based on the combination
                matrix[l, 1:] = relev_points[:, int_combinations[k, l]]
            
            # Calculate the orientation by computing the sign of the determinant
            orientation = np.sign(np.linalg.det(matrix))
            
            # Append symbol ('+', '-', or '0') based on orientation
            if orientation == 1:
                word.append('+')
            elif orientation == -1:
                word.append('-')
            else:
                word.append('0')
        
        # Append the generated word (symbol string) for this window to the list of words
        words.append(''.join(word))

    # Return unique symbols and their counts
    unique_symbols, symbol_count = np.unique(words, return_counts=True)
    return unique_symbols, symbol_count
