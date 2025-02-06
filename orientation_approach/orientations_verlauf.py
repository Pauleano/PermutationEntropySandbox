import numpy as np

def orientations_verlauf(data, emb_dim, emb_delay):
    """
    This function computes the orientation-based symbolization of the data.
    The output represents symbolic states of the data based on determinant calculations.
    
    Args:
    - data (ndarray): A 2D numpy array where rows represent features, and columns represent time points.
    - emb_dim (int): Embedding dimension, determining the number of points considered for each "symbol."
    - emb_delay (int): Delay between data points used to construct the embedding.
    
    Returns:
    - unique_symbols (ndarray): The unique symbols generated during the orientation computation.
    - symbol_count (ndarray): The count of each unique symbol.
    """
    
    def gaus(x):
        """
        A helper function to calculate a 'gaussian-like' value for symbolization.
        
        Args:
        - x (int): Input value for which the function computes a value.
        
        Returns:
        - int: Computed value based on a parabolic-like function.
        """
        if x < 0:
            return 0
        else:
            return int((x**2 + x) * 0.5)
    
    # Initialize an empty list to hold the resulting symbols
    words = []
    # Construct the matrix that will be used to calculate orientation
    matrix = np.concatenate((np.ones((data.shape[0] + 1, 1)), np.zeros((data.shape[0] + 1, data.shape[0]))), axis=1)
                

    # Loop over the data to compute symbolic representations
    for i in range(data.shape[1] - (emb_dim - 1) * emb_delay):
        # Create an empty symbol array, and a corresponding array for string-based symbols
        symbol = np.zeros(gaus(emb_dim - data.shape[0]))
        symbol_str = np.zeros(gaus(emb_dim), dtype=str)

        # Get relevant points from the data based on embedding dimension and delay
        relev_points = data[:, i:i + emb_dim * emb_delay:emb_delay]
        # print(f"Relevant points (data slice): {relev_points}")
        
        # For each new data point in the embedding dimension
        counter = 0
        for k in range(data.shape[0], emb_dim):
            # Calculate the orientation by comparing with previous data points
            for l in range(k - data.shape[0] + 1):
                # Set values in the matrix for orientation calculation
                matrix[-1, 1:] = relev_points[:, k]  # Last row is the current data point
                matrix[0:-1, 1:] = relev_points[:, l:l + data.shape[0]].T  # Previous points up to current
            
                # print(f"Matrix for determinant calculation: {matrix}")
                
                # Calculate determinant and store the result
                symbol[counter] = np.linalg.det(matrix)
                counter += 1
        
        # print(f"Symbol for current slice: {symbol}")
        
        # Create string representation of the symbol based on the determinant sign
        symbol_str = np.where(symbol > 0, '+', np.where(symbol < 0, '-', '0'))
        # print(f"Symbol string: {''.join(symbol_str)}")
        
        # Append the generated symbol string to the words list
        words.append(''.join(symbol_str))

    # print(f"All generated symbols: {words}")

    # Find unique symbols and count their occurrences
    unique_symbols, symbol_count = np.unique(words, return_counts=True)
    # print(f"Unique symbols: {unique_symbols}")
    # print(f"Symbol counts: {symbol_count}")
    
    # Return the unique symbols and their counts
    return unique_symbols, symbol_count
