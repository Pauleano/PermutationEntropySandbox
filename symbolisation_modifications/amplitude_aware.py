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


a=ordinal_sequence([1,2,3,4,0],dx=3)
print(a,a.shape)

def amplitude_aware_distr(data,weighting_koefficient):
    #weighting_coefficient determines weighting between absolute values and distance of following values

    #get symbols from input
    symbolsequence=data[0:int(data.shape[0]*0.5),:]
    #get unique symbols
    unique_symbols=np.unique(symbolsequence.T,axis=0)
    #initiate weights for each symbol   
    unique_symbol_weights=np.zeros(len(unique_symbols))

    #for each symbol type get specific data corresponding to symbol
    weight_index=0
    for i in unique_symbols:
        #print(i)
        for j in range(data.shape[1]):
            #print(data[0:int(data.shape[0]*0.5),j])
            if all(i==data[0:int(data.shape[0]*0.5),j])==True:
                #print(j)
                #calculate specific weight according to amplitude aware PE
                abs_sum=np.sum(abs(data[int(data.shape[0]*0.5):data.shape[0],j]))
                print(abs_sum)
                difference_array=data[int(data.shape[0]*0.5):data.shape[0]-1,j]-data[int(data.shape[0]*0.5)+1:data.shape[0],j]
                difference_sum=np.sum(abs(difference_array))
                #print(difference_sum)
                unique_symbol_weights[weight_index]+=weighting_koefficient*(abs_sum/(data.shape[0]*0.5))+(1-weighting_koefficient)*(difference_sum/(data.shape[0]*0.5-1))
        weight_index+=1        
    return unique_symbol_weights/np.sum(unique_symbol_weights)

out2=amplitude_aware_distr(a,0)
print(out2)