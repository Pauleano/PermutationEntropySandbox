import numpy as np

#multiscale PE preprocessing
#in: 1D-zeitreihe
#out: 1D-zeitreihe at specific scale

import math 
import itertools as iter

def ordinal_sequence(data, dx=3, dy=1, taux=1, tauy=1, overlapping=True, tie_precision=None):
    """
    Applies the Bandt and Pompe\\ [#bandt_pompe]_ symbolization approach to obtain 
    a sequence of ordinal patterns (permutations) from data.
    
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

    Examples
    --------
    >>> ordinal_sequence([4,7,9,10,6,11,3], dx=2)
    array([[0, 1],
           [0, 1],
           [0, 1],
           [1, 0],
           [0, 1],
           [1, 0]])
    >>> 
    >>> ordinal_sequence([4,7,9,10,6,11,3], dx=2, taux=2)
    array([[0, 1],
           [0, 1],
           [1, 0],
           [0, 1],
           [1, 0]])
    >>>
    >>> ordinal_sequence([[1,2,1,4],[8,3,4,5],[6,7,5,6]], dx=2, dy=2)
    array([[[0, 1, 3, 2],
            [1, 0, 2, 3],
            [0, 1, 2, 3]], 
           [[1, 2, 3, 0],
            [0, 1, 3, 2],
            [0, 1, 2, 3]]])
    >>>
    >>> ordinal_sequence([1.3, 1.2], dx=2), ordinal_sequence([1.3, 1.2], dx=2, tie_precision=0)
    (array([[1, 0]]), array([[0, 1]]))
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
        symbols = np.apply_along_axis(np.argsort, 1, partitions)
        
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
        symbols = np.apply_along_axis(np.argsort, 2, partitions)
    
    
    symbols2=np.concatenate((symbols.T,partitions.T),axis=0)
    return symbols2

in1=[1,2,3,4,0]
a=ordinal_sequence(in1,dx=2)
print(a,a.shape)

def fine_grained_PE(sequence_data,data_std,alpha):
    #given data_std and difference series, alpha determines how many new symbols are gotten

    #array for additional element
    additional_elements=np.zeros((1,sequence_data.shape[1]))
    #for each symbol type get specific data corresponding to symbol
    weight_index=0
    for i in range(sequence_data.shape[1]):
        #calculate distance inside 
        diff_array=sequence_data[int(sequence_data.shape[0]*0.5):sequence_data.shape[0]-1,i]-sequence_data[int(sequence_data.shape[0]*0.5)+1:sequence_data.shape[0],i]
        max_diff=max(abs(diff_array))
        #calculate additional element
        additional_elements[0,i]=math.floor(max_diff/(data_std*alpha))

    #concatenate additioal symbols with current symbols
    symbol_sequence=np.concatenate((sequence_data[0:int(sequence_data.shape[0]*0.5),:],additional_elements),axis=0)
    symbols,symbol_counts=np.unique(symbol_sequence,return_counts=True,axis=1)
                
    return symbols,symbol_counts

out2_1,out2_2=fine_grained_PE(a,np.std(in1),1)
print(out2_1)