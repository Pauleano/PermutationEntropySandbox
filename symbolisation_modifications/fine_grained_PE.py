import numpy as np

#uses output from modified_ordinal_sequence
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
