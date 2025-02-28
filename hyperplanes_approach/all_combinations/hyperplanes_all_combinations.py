import numpy as np
import itertools as iter

def hyperplanes_all_combinations(multivar_data,emb_dim,emb_delay):
    #
    emb_dim+=1
    # einschränkung: max fensterlänge=10 (0,1,2,3,4,5,6,7,8,9)
    zahlen=[]
    for m in range(emb_dim):
        zahlen.append(str(m))
    zahlen=''.join(zahlen)
    #print(zahlen)
    
    kombinations=np.array(list(iter.combinations(zahlen,3)))
    print(kombinations)

    words=[] 
    #for i in range(anzahl der fenster):
    for i in range(multivar_data.shape[1]-((emb_dim-1)*emb_delay)):
        
        #relevante daten aus reihe lesen |data in ausschnitt|=emb_dim+1
        word=[]
        relev_ausschnitt=multivar_data[::,i:i+(emb_dim)*emb_delay:emb_delay]#'stop'-index wird nicht erreicht
        #print(relev_ausschnitt)
        
        #für jede punktkombi differenzen und winkel berechnen
        
        for j in range(kombinations.shape[0]):
            point_one=int(kombinations[j,0])
            point_two=int(kombinations[j,1])
            point_three=int(kombinations[j,2])

            vect_one=relev_ausschnitt[:,point_two]-relev_ausschnitt[:,point_one]
            #print(vect_one)
            vect_two=relev_ausschnitt[:,point_three]-relev_ausschnitt[:,point_two]
            #print(vect_two)
            position=vect_one @ vect_two

            if np.sign(position)==1:    
                word.append("+")
            elif np.sign(position)==-1:    
                word.append("-")
            else:    
                word.append("0")
        #print(word)
        words.append(''.join(word))

    [list_of_words,abfolge_words,haeuf_words]=np.unique(words,return_inverse=True, return_counts=True)

    return list_of_words,abfolge_words,haeuf_words 
