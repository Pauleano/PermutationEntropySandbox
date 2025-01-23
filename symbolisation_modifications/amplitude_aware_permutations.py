import numpy as np

def amplitude_aware_permutations(data, weighting_koefficient):
    """
    Calculate the permutation weights based on the amplitude and the difference between consecutive values.
    
    Parameters:
    data (np.ndarray): The sequence data (n x m), where [0:n/2] is the data and [(n/2)+1:n] is the permutation and m is the number of observed permutations.
    weighting_koefficient (float): A coefficient that balances the contribution of the absolute sum and the difference sum.
    
    Returns:
    np.ndarray: The probabilities for each unique permutation.
    """

    # Extract the second half of the data (permutation sequence)
    permutation_sequence = data[int(data.shape[0]*0.5):,:]  # Taking the second half of the dataset
    # Get unique permutations from the permutation sequence
    unique_symbols = np.unique(permutation_sequence.T, axis=0)  # Doesnt work properly if not transposed
    # Initialize an array to hold the weights for each unique permutation
    unique_symbol_weights = np.zeros(len(unique_symbols))

    # Iterate over each unique permutation to calculate its specific weight
    weight_index = 0
    for i in unique_symbols:
        # For each permutation, loop through all the columns in the data
        for j in range(data.shape[1]):
            # Check if the current permutation matches the unique permutation using array_equal
            if np.array_equal(i, permutation_sequence[:, j]): 
                # Calculate the absolute sum of values for the current symbol
                abs_sum = np.sum(abs(data[:int(data.shape[0]*0.5), j]))  
                
                # Calculate the sum of absolute differences between consecutive values 
                difference_array = data[1:int(data.shape[0]*0.5), j] - data[:int(data.shape[0]*0.5)-1, j]
                difference_sum = np.sum(abs(difference_array)) 
                
                # Calculate the weight for the current symbol based on average amplitude and average difference
                unique_symbol_weights[weight_index] += weighting_koefficient * (abs_sum / (data.shape[0]*0.5)) + (1 - weighting_koefficient) * (difference_sum / (data.shape[0]*0.5 - 1))
        # Move to the next symbol in the unique symbols list
        weight_index += 1
    
    # Convert weights to probabilities
    return unique_symbol_weights / np.sum(unique_symbol_weights) 
