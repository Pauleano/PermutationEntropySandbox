import numpy as np

def coded_PE(seq_data):
    #get symbols from input
    symbolsequence=seq_data[0:int(seq_data.shape[0]*0.5),:]
    #get unique symbols
    unique_symbols=np.unique(symbolsequence.T,axis=0)
    #2D array for average calculation   
    #last row is for counts of symbols
    symbol_averages=np.zeros((int(seq_data.shape[0]*0.5)+1,len(unique_symbols)))
    sum_counts=np.zeros((1,len(unique_symbols)))

    #for each symbol type get specific data corresponding to symbol and add all up
    symbolcount=0
    for i in unique_symbols:
        #print(i)
        for j in range(seq_data.shape[1]):
            #print(data[0:int(data.shape[0]*0.5),j])
            if all(i==seq_data[0:int(seq_data.shape[0]*0.5),j])==True:
                #print(j)
                symbol_averages[:,symbolcount]+=seq_data[0:int(seq_data.shape[0]*0.5),j]
                sum_counts[0,symbolcount]+=1
        symbolcount+=1
    
    #get averages of each position for every permutation
    for i in range(symbolcount):
        symbol_averages[:,i]=symbol_averages[:,i]/sum_counts[i]

    coded_array=np.zeros((int(seq_data.shape[0]*0.5),seq_data[1]))

    #for each datapoint of window compare with symbol_specific_average differentiating between -1,0,1 coresponding to <,=,> respectively 
    symbolcount=0
    for i in unique_symbols:
        #print(i)
        for j in range(seq_data.shape[1]):
            #print(data[0:int(data.shape[0]*0.5),j])
            if all(i==seq_data[0:int(seq_data.shape[0]*0.5),j])==True:
                #print(j)
                coded_array[:,j]=seq_data[0:int(seq_data.shape[0]*0.5),j]-symbol_averages[:,symbolcount]
        symbolcount+=1

    #codierung der Einträge
    for i in range(seq_data.shape[0]):
        for j in range(seq_data.shape[1]):
            if coded_array[i,j]<0:
                coded_array[i,j]='-'
            elif coded_array[i,j]>0:
                coded_array[i,j]='+'
            else:
                coded_array[i,j]='0'

    #concatenate coded_matrix to symbol sequence
    new_symbol_sequence=np.concatenate((symbolsequence,coded_array),axis=0) 
    
     
    #aufbau matrix:
    #[symbol1;symbol2;...]
    #[coded1 ;coded2 ;...]

    #wende unique auf matrix an along axis 0(verticaler scan) analog zu
    symbols,symbol_counts=np.unique(new_symbol_sequence,axis=1,return_counts=True)

    return symbols,symbol_counts
