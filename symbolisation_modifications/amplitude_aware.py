import numpy as np

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
