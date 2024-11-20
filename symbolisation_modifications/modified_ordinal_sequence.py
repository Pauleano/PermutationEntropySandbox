#slightly modified method, copied from ordpy package
#outputs symbols and coresponding data not just symbol sequence

import itertools
import math
import warnings

import numpy as np

def modified_ordinal_sequence(data, dx=3, dy=1, taux=1, tauy=1, overlapping=True, tie_precision=None):
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


a=modified_ordinal_sequence([1,2,3,4,0],dx=3)
print(a,a.shape)
