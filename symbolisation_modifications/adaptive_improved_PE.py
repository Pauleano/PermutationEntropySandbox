import numpy as np
import math as m

def partitions_copied(data, dx=3, dy=1, taux=1, tauy=1, overlapping=True, tie_precision=None):
    """
    Copied from ordpy package function ordinal_sequence()
    
    Parameters
    ----------
    data : array 
           Array object in the format :math:`[x_{1}, x_{2}, x_{3}, \\ldots ,x_{n}]`
           or  :math:`[[x_{11}, x_{12}, x_{13}, \\ldots, x_{1m}],
           \\ldots, [x_{n1}, x_{n2}, x_{n3}, \\ldots, x_{nm}]]` 
           (:math:`n \\times m`).
    dx : int
         Embedding dimension (horizontal axis) (default: 3).
    dy : int
         Embedding dimension (vertical axis); it must be 1 for time series 
         (default: 1).
    taux : int
           Embedding delay (horizontal axis) (default: 1).
    tauy : int
           Embedding delay (vertical axis) (default: 1).
    overlapping : boolean
                  If `True`, **data** is partitioned into overlapping sliding 
                  windows (default: `True`). If `False`, adjacent partitions are
                  non-overlapping.
    tie_precision : None, int
                    If not `None`, **data** is rounded with `tie_precision`
                    number of decimals (default: `None`).

    Returns
    -------
     : array
       Array containing the sequence of ordinal patterns.
    """
    
    try:
        ny, nx = np.shape(data)
        data   = np.array(data)
    except:
        nx     = np.shape(data)[0]
        ny     = 1
        data   = np.array([data])

    if tie_precision is not None: 
        data = np.round(data, tie_precision)
    
    if ny==1: #time series
        if overlapping == True:
            partitions = np.apply_along_axis(func1d       = np.lib.stride_tricks.sliding_window_view, 
                                             axis         = 1, 
                                             arr          = data, 
                                             window_shape = (dx+(dx-1)*(taux-1),)
                                            )
            partitions = partitions[::, ::, ::taux].reshape(-1, dx) 
                                                                    
        else: #non overlapping
            partitions = np.concatenate(
                [
                    [np.concatenate(data[j:j+dy*tauy:tauy, i:i+dx*taux:taux]) for i in range(0, nx-(dx-1)*taux, dx+(dx-1)*(taux-1))] 
                    for j in range(ny-(dy-1)*tauy)
                ]
            )
        
    else: #image
        if overlapping == True:
            partitions        = np.lib.stride_tricks.sliding_window_view(x            = data, 
                                                                         window_shape = (dy+(dy-1)*(tauy-1), dx+(dx-1)*(taux-1))
                                                                        )
            rows, columns, *_ = np.shape(partitions)
            partitions        = partitions[::,::,::tauy,::taux].reshape(rows, columns, dx*dy)

        else: #non overlapping
            partitions = np.concatenate(
                [
                    [[np.concatenate(data[j:j+dy*tauy:tauy, i:i+dx*taux:taux]) for i in range(0, nx-(dx-1)*taux, dx+(dx-1)*(taux-1))]] 
                    for j in range(0, ny-(dy-1)*tauy, dy+(dy-1)*(tauy-1))
                ]
            )            
    return partitions



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
