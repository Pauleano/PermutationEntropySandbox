import numpy as np

def hyperplanes_verlauf(multivar_data, emb_dim, emb_delay):
    """
    This function performs symbolic pattern recognition by analyzing the differences between embedding points
    in multivariate data. It generates a set of symbolic sequences representing these patterns and returns the unique
    sequences along with their frequencies.

    Parameters:
    multivar_data : numpy.ndarray
        A 2D array where rows represent different variables, and columns represent time points (or samples).
    emb_dim : int
        The embedding dimension (how many steps to consider for each "window").
    emb_delay : int
        The delay between embedding points (controls the temporal separation of points in the window).

    Returns:
    unique_symbols : numpy.ndarray
        The unique symbolic sequences (patterns) generated from the data.
    symbol_count : numpy.ndarray
        The frequency count of each unique sequence.
    """
    
    # Helper function: calculates the triangular number for x (used for indexing).
    def gaus(x):
        # If x is negative, return 0, else return triangular number
        if x < 0:
            return 0
        else:
            return int(0.5 * (x ** 2 + x))  
            
    # List to store all the generated symbols
    symbol_sequences = []
    
    # Iterate over the dataset in windows based on embedding dimension and delay
    for i in range(multivar_data.shape[1] - emb_dim * emb_delay):
        
        # Extract relevant data slice (embedding window) from multivar_data.
        relev_ausschnitt = multivar_data[:, i:i + emb_dim * emb_delay:emb_delay]
        
        # Create an empty matrix to store relevant differences between points
        relev_diff = np.zeros((multivar_data.shape[0], gaus(emb_dim) - emb_dim + 1))
        
        # For each point calculate the differences(vectors) to previous points
        relev_diff[:, 0] = relev_ausschnitt[:, 1] - relev_ausschnitt[:, 0]
        counter = 1
        for j in range(2, emb_dim + 1):
            for k in range(1, j):
                if counter == gaus(j - 1):
                    relev_diff[:, counter] = relev_ausschnitt[:, j] - relev_ausschnitt[:, j - 1]
                else:
                    relev_diff[:, counter] = relev_ausschnitt[:, j] - relev_ausschnitt[:, k]
                counter += 1
                
        # Initialize an empty result matrix to store the dot products of differences(vectors)
        ergebnis_matrix = np.zeros((emb_dim - 1, emb_dim - 1))

        # For each difference(vector) compute the dot product with previous differences(vectors)
        for j in range(2, emb_dim + 1):
            for k in range(1, j):
                ergebnis_matrix[j - 2, k - 1] = np.dot(relev_diff[:, gaus(k - 1)], relev_diff[:, gaus(j - 2) + k])
        
        # Construct the symbolic sequence (a sequence of +, -, and 0) based on the values in ergebnis_matrix
        symbol = []
        for j in range(ergebnis_matrix.shape[0]):
            # Add a separator '|' between rows
            if j > 0:
                symbol.append('|')
            for k in range(j + 1):
                # If the value is negative, append '-'
                if ergebnis_matrix[j, k] < 0:
                    symbol.append('-')
                # If the value is positive, append '+'
                elif ergebnis_matrix[j, k] > 0:
                    symbol.append('+')
                # If the value is zero, append '0'
                else:
                    symbol.append('0')
        
        # Append the generated symbolic sequence to the list of sequences
        symbol_sequences.append(''.join(symbol))
    
    # Use numpy.unique to get unique sequences, their indices, and their frequencies
    unique_symbols, symbol_count = np.unique(symbol_sequences, return_counts=True)
    
    # Return the unique sequences, the indices of sequences, and their frequencies
    return unique_symbols, symbol_count



#output ist nur zeichenfolge für den letzten vektor bezüglich vorheriger ebenen
#bis rel_diff gleich
#ergebnismatrix nur ergebnisse von letztem vektor
def hyperplanes_last_only(multivar_data,emb_dim,emb_delay):
    #for i in range(anzahl der fenster):
        
    words=[]
    for i in range(multivar_data.shape[1]-emb_dim*emb_delay):
        
        #relevante daten aus reihe lesen |data in ausschnitt|=emb_dim+1
        relev_ausschnitt=np.zeros((multivar_data.shape[0],emb_dim+1))
        for j in range(emb_dim+1):
            relev_ausschnitt[:,j]=multivar_data[:,i+j*emb_delay]
        
        #struktur:[x1-x0,x2-x1,x3-x2,x4-x3|x5-x1,x5-x2,x5-x3,x5-x4]--> beispiel für ausschnitt (x0,...,x5)
        #neuer schritt muss mit allen vorherigen ebenen verglichen werden um exakte position zu wissen
        relev_diff=np.zeros((multivar_data.shape[0],(relev_ausschnitt.shape[1]-2)*2))
        #für jeden neuen punkt differenzen zu bisherigen ebenenpunkten berechnen
        for j in range(1,relev_ausschnitt.shape[1]-1):
            relev_diff[:,j-1]=relev_ausschnitt[:,j]-relev_ausschnitt[:,j-1]
            relev_diff[:,(emb_dim-1)+(j-1)]=relev_ausschnitt[:,emb_dim]-relev_ausschnitt[:,j]
        #in for schleife matrizen (bisherige ebenen) erstellen und mit vektor (neue schritt) multiplizieren
        #ergebnis=vektor... soll in ergebnismatrix als zeile übertragen werden
        #plane_matrix=np.zeros((multivar_data.shape[0],emb_dim-1))
        ergebnis_matrix=np.zeros((1,emb_dim-1))

        #formel für indexe der differenzen für vergleich: gaus(k-1)=index ebene in rel_diff
        for k in range(emb_dim-1):
            #plane=relev_diff[:,k].T
            #vector=relev_diff[:,emb_dim-1+k]
            ergebnis_matrix[0,k]=relev_diff[:,k] @ relev_diff[:,emb_dim-1+k]
            #cos-winkelbestimmung (szenario nullteilung bei differenz=0)
            #ergebnis_matrix[0,k]=ergebnis_matrix[0,k]/((abs(np.dot(relev_diff[:,k],relev_diff[:,k]))**0.5)*(abs(np.dot(relev_diff[:,emb_dim-1+k],relev_diff[:,emb_dim-1+k]))**0.5)) 
        
        #mithilfe ergebnismatrix wort bestimmen und in wörterliste packen
        #bei links rechts entscheidung nur vorzeichen relevant
        #bei fallunterscheidung
        wordpart=[]
        for j in range(ergebnis_matrix.shape[1]):
            #nur bis inklusive dem eintrag auf der Diagonalen gehen
            if ergebnis_matrix[0,j]<0:
                wordpart.append('-')
            elif ergebnis_matrix[0,j]>0:
                wordpart.append('+')
            else:
                wordpart.append('0')    
        words.append(''.join(wordpart))
                
    #output mithilf np.unique bekommen (input zwar liste nicht array aber unique macht als erstes array draus)
    [list_of_words,abfolge_words,haeuf_words]=np.unique(words,return_inverse=True, return_counts=True)

    return list_of_words,abfolge_words,haeuf_words



