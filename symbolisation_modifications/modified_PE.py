import numpy as np
import math as m
import time as t



def modified_symbols(data):
    #basic implementaion of symbolisation used in "modified Permutation Entropie"

    *_, indexe, counts=np.unique(data,return_index=True,return_counts=True)
    return np.repeat(indexe,counts)



def modified_symbols(data):
    """
    This function performs symbolization on the given data by replacing each unique element 
    with its index and repeating it according to the frequency of that element in the original data.
    
    Parameters:
    data (numpy array or list): The data points that need to be symbolized.
    
    Returns:
    numpy array: An array where each element of `data` is according to "modified Permutation Entropy".
                 An array where each element of `data` is replaced by its index in the unique values 
                 of the input data, repeated according to the frequency of each unique element
    """
    
    # Extract the unique values, their indices in the unique array, and their counts in the original array
    *_, indexe, counts = np.unique(data, return_index=True, return_counts=True)
    
    # Return a new array where the indices of unique values are repeated according to their counts
    return np.repeat(indexe, counts)



def open_pos(array):
    """
    Helperfunction for max_symbols()

    Parameters:
    array (numpy array or list): Array where each element represents the number of positions
                                  filled by a symbol at that step.

    Returns:
    int: The number of remaining open positions after all symbols are processed, or 0 if no positions are open.
    """
    
    # Start with all positions open 
    open_pos = array.shape[0]
    
    # Iterate over each symbol's position count in the array
    for i in range(array.shape[0]):
        
        # If the number of open positions is equal to the number of positions filled by the current symbol return 0
        if open_pos == array[i]:
            return 0
        
        # If the current symbol fills fewer positions than available, reduce the number of open positions
        elif open_pos > array[i]:
            open_pos -= array[i]
        
        # If the current symbol requires more positions than there are available, return the remaining number of open positions
        else:
            return open_pos
    
    # All symbols have been processed
    return open_pos
    


def missing_pos(array):
    #does the same thing as open_pos() but slower
    return (array.shape[0]-np.sum(array))



def read_symbol(array):
    """
    Helperfunction for max_symbols()
    
    Parameters:
    array (numpy array or list): The input array whose non-zero elements are to be counted.
    
    Returns:
    int: The count of non-zero elements in the array.
    """
    
    # Initialize a counter for non-zero elements
    counter = 0
    
    # Iterate over each element in the array
    for i in range(array.shape[0]):  # or use len(array) if it's a list
    
        # If the element is non-zero, increment the counter
        if array[i] != 0:
            counter += 1
    
    # Return the total count of non-zero elements
    return counter


    
def max_symbols(emb_dim):
    symb_count=0
    markers=np.zeros(emb_dim)+1
    while(markers[0]!=emb_dim):
        if(open_pos(markers)==0):
            symb_count+=m.factorial(read_symbol(markers))
            print(markers)
        for i in range(emb_dim-1,-1,-1):
            if(markers[i]==emb_dim-1-i+1):
                if i==0:#prevent markers[0]=0
                    break
                markers[i]=0
                markers[i-1]+=1
                if open_pos(markers)==0:
                    symb_count+=m.factorial(read_symbol(markers))
            elif open_pos(markers)==0:
                if markers[i]==0:
                    continue
                else:
                    markers[i]=0
                    markers[i-1]+=1
                    break
            else:
                open=int(open_pos(markers))
                markers[emb_dim-open:]=1
                break
    if emb_dim==2:
        return symb_count #all valid symbols already have been counted
        
    return symb_count+1 #with emb_dim>=3 while loop terminated before counting symbol (emb__dim,0,0,0,...)



def max_symbols(emb_dim):
    """
    This function calculates the maximum number of valid symbols that can be formed
    using a permutation-based approach where each symbol is represented by a set of 'markers'.
    
    Parameters:
    emb_dim (int): The embedding dimension, which is the number of available positions.
    
    Returns:
    int: The total count of valid symbols that can be formed using numbers 0,1,2,...,'emd_dim'.
    """
    
    # Initialize the symbol count to 0
    symb_count = 0
    
    # Initialize 'markers' array with size emb_dim, all set to 1, corresponding to every number being used once
    markers = np.zeros(emb_dim) + 1
    
    # While loop runs until markers[0] reaches the embedding dimension (emb_dim)
    while markers[0] != emb_dim:
        
        # If no open positions are left, count the number of valid permutations (factorial)
        if open_pos(markers) == 0:
            symb_count += m.factorial(read_symbol(markers))
            
        # Loop through the markers array in reverse order
        for i in range(emb_dim - 1, -1, -1):
            
            # If the current marker reaches its maximum value (emb_dim - i), reset it
            if markers[i] == emb_dim - 1 - i + 1:
                if i == 0:  # Prevent markers[0] from being reset to 0
                    break
                markers[i] = 0  # Reset the current marker
                markers[i - 1] += 1  # Increment the previous marker
                
                # Check if no open positions are left after this change
                if open_pos(markers) == 0:
                    symb_count += m.factorial(read_symbol(markers))
            
            # If there are still open positions, continue checking
            elif open_pos(markers) == 0:
                if markers[i] == 0:
                    continue  # Skip if the marker is already 0
                else:
                    markers[i] = 0
                    markers[i - 1] += 1
                    break  # Exit the loop after adjusting the marker
            else:
                # If there are open positions, fill them from the back with the value 1 
                open = int(open_pos(markers))
                markers[emb_dim - open:] = 1
                break  # Exit the loop after filling open positions
    
    # Special case when embedding dimension is 2, all valid symbols are counted in the loop itself
    if emb_dim == 2:
        return symb_count  
    
    # For emb_dim >= 3, add 1 to the final count since loop doesnt count the symbol 'markers'=[emb_dim,0,0,0,...]
    return symb_count + 1
