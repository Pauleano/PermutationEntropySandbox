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