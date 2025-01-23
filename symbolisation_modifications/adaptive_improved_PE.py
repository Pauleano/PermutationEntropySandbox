import numpy as np
import math as m

def impr_symbols_without_abs(emb_window, quantisation_para, min_val, max_val):
    """
    Improved Permutation Entropy without using the absolute difference. Overly sensitive to negative differences

    Parameters:
    emb_window (np.ndarray): A 1D or 2D array representing the embedded window of data.
    quantisation_para (int): The number of quantization levels.
    min_val (float): The minimum value of the data range.
    max_val (float): The maximum value of the data range.

    Returns:
    np.ndarray: The calculated symbol sequence.
    """
    
    # Compute the delta (quantization step)
    delta = (max_val - min_val) / quantisation_para
    
    # Initialize the symbol array to store the quantized values
    symbol = np.zeros(emb_window.shape[0])

    #Quantize first element
    symbol[0]=m.floor((emb_window[0] - min_val) / delta)

    # Loop through each element in the embedded window
    for i in range(emb_window.shape[0]):
        
        # Quantize current element
        symbol[i] = symbol[0] + m.floor((emb_window[i] - emb_window[0]) / delta)
        
    return symbol



def impr_symbols_with_abs(emb_window, quantisation_para, min_val, max_val):
    """
    Applies 'Improved Permutation Entropy" approach to data points in the probably intented way.
    This function applies quantization to an embedding window, transforming continuous values
    into discrete symbols based on the quantization parameters and the provided range.
    
    Parameters:
    emb_window (numpy array): The embedding window (data points to be quantized).
    quantisation_para (int): The number of quantization levels or symbols.
    min_val (float): The minimum value in the quantization range.
    max_val (float): The maximum value in the quantization range.
    
    Returns:
    numpy array: An array of quantized symbols corresponding to the embedding window values.
    """
    
    # Calculate the delta (step size) based on the quantization parameters
    delta = (max_val - min_val) / quantisation_para
    
    # Calculate the base quantization symbol for each value (based on emb_window[0] and the min_val)
    base_symbol = np.floor((emb_window[0] - min_val) / delta)
    
    # Calculate the differences between each value and emb_window[0]
    diff = emb_window - emb_window[0]
    
    # Vectorized calculation of quantized symbols
    symbol = base_symbol + np.sign(diff) * np.floor(np.abs(diff) / delta)
    
    # Handle case where value is exactly max_val (map to the maximum quantized symbol)
    symbol[emb_window == max_val] = quantisation_para - 1
    
    return symbol



def adaptive_impr_symbols(emb_window, quant_para, min_val, max_val, slope_para):
    """
    This function applies adaptive quantization to an embedding window, transforming continuous values
    into discrete symbols. The quantization is adjusted based on the relative slope between consecutive values.

    Parameters:
    emb_window (numpy array): The embedding window (data points to be quantized).
    quant_para (int): The number of quantization levels or symbols.
    min_val (float): The minimum value in the quantization range.
    max_val (float): The maximum value in the quantization range.
    slope_para (float): The parameter that controls the sensitivity to slope changes between consecutive values.
    
    Returns:
    numpy array: An array of quantized symbols corresponding to the embedding window values.
    """
    
    # Calculate the step size (delta) for quantization based on the provided range and quantization levels
    delta = (max_val - min_val) / quant_para
    
    # Initialize the symbol array with zeros
    symbol = np.zeros(emb_window.shape[0])

    # Set the first symbol based on the initial value in the embedding window
    symbol[0] = m.floor((emb_window[0] - min_val) / delta)

    # Loop through the embedding window starting from the second element
    for i in range(1, emb_window.shape[0]):
        # Calculate the symbol for each element based on the previous symbol and the slope
        symbol[i] = symbol[i - 1] + np.sign(emb_window[i] - emb_window[i - 1]) * m.floor(abs(emb_window[i] - emb_window[i - 1]) / slope_para)

    return symbol
