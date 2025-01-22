import numpy as np
import scipy.optimize as opt

def hyperplanes_verlauf(multivar_data,emb_dim,emb_delay):
    #for i in range(anzahl der fenster):

    #gaussian sum for array size 
    def gaus(x):
        if x<0:
            out=0
        else:
            out=(x**2+x)*0.5    
        return int(out)
    
    words=[]
    for i in range(multivar_data.shape[1]-emb_dim*emb_delay):
        
        #relevante daten aus reihe lesen |data in ausschnitt|=emb_dim+1
        relev_ausschnitt=np.zeros((multivar_data.shape[0],emb_dim+1))
        for j in range(emb_dim+1):
            relev_ausschnitt[:,j]=multivar_data[:,i+j*emb_delay]
        
        #struktur:[x1-x0<--vor der schleife|x2-x1|x3-x1,x3-x2|x4-x1,x4-x2,x4-x3|....]--> #länge=(emb_dim^2+emb_dim)/2
        #neuer schritt muss mit allen vorherigen ebenen verglichen werden um exakte position zu wissen
        relev_diff=np.zeros((multivar_data.shape[0],gaus(emb_dim)-emb_dim+1))
        #für jeden neuen punkt differenzen zu bisherigen ebenenpunkten berechnen
        relev_diff[:,0]=relev_ausschnitt[:,1]-relev_ausschnitt[:,0]
        counter=1
        for j in range(2,emb_dim+1):
            for k in range(1,j):
                    if counter==gaus(j-1):
                        relev_diff[:,counter]=relev_ausschnitt[:,j]-relev_ausschnitt[:,j-1]
                    else:
                        relev_diff[:,counter]=relev_ausschnitt[:,j]-relev_ausschnitt[:,k]
                    counter+=1
                
        #in for schleife matrizen (bisherige ebenen) erstellen und mit vektor (neue schritt) multiplizieren
        #ergebnis=vektor... soll in ergebnismatrix als zeile übertragen werden
        #plane_matrix=np.zeros((multivar_data.shape[0],emb_dim-1))
        ergebnis_matrix=np.zeros((emb_dim-1,emb_dim-1))

        #formel für indexe der differenzen für vergleich: gaus(k-1)=index ebene in rel_diff
        for j in range(2,emb_dim+1):
            for k in range(1,j):
                ergebnis_matrix[j-2,k-1]=relev_diff[:,gaus(k-1)] @ relev_diff[:,gaus(j-2)+k]
                
         
        #mithilfe ergebnismatrix wort bestimmen und in wörterliste packen
        #zeilenweise die matrix durchgehen
        wordpart=[]
        for j in range(ergebnis_matrix.shape[0]):
            #nur bis inklusive dem eintrag auf der Diagonalen gehen
            if j>0:
                wordpart.append('|')
            for k in range(j+1):
                if ergebnis_matrix[j,k]<0:
                    wordpart.append('-')
                elif ergebnis_matrix[j,k]>0:
                    wordpart.append('+')
                else:
                    wordpart.append('0')
                    
        words.append(''.join(wordpart))
                
    #output mithilf np.unique bekommen (input zwar liste nicht array aber unique macht als erstes array draus)
    [list_of_words,abfolge_words,haeuf_words]=np.unique(words,return_inverse=True, return_counts=True)

    return list_of_words,abfolge_words,haeuf_words


'''
def g1(x):
    return ((x[2]-x[0])*x[4]+(x[3]-x[1])*x[2])-((x[2]-x[0])*x[2]+(x[3]-x[1])*x[3])

def zielfunk(x):
    return np.sum(np.maximum(0,g1(x))**2)

x_0=np.array([0,0,1,0,2,0,])
'''

abstand=0.1

def g1(x):
    return ((x[2]-x[0])*x[4]+(x[3]-x[1])*x[2])-((x[2]-x[0])*x[2]+(x[3]-x[1])*x[3])

def g2(x):
    return -((x[2]-x[0])*x[6]+(x[3]-x[1])*x[7])+((x[2]-x[0])*x[2]+(x[3]-x[1])*x[3])

def g3(x):
    return -((x[4]-x[2])*x[6]+(x[5]-x[3])*x[7])+((x[4]-x[2])*x[4]+(x[5]-x[3])*x[5])

def g4(x):
    return ((x[2]-x[0])*x[8]+(x[3]-x[1])*x[9])-((x[2]-x[0])*x[2]+(x[3]-x[1])*x[3])

def g5(x):
    return ((x[4]-x[2])*x[8]+(x[5]-x[3])*x[9])-((x[4]-x[2])*x[4]+(x[5]-x[3])*x[5])

def g6(x):
    return ((x[6]-x[4])*x[8]+(x[7]-x[5])*x[9])-((x[6]-x[4])*x[6]+(x[7]-x[5])*x[7])

def zielfunk(x):
    return np.sum(np.maximum(0,[g1(x),g2(x),g3(x),g4(x),g5(x),g6(x)])**2)

x_0=np.array([-1,0,3,0,2,1,4,4,4,5])
print(x_0.reshape((5,2)))

result=opt.minimize(zielfunk, x_0, method='trust-constr')
print(result.x.reshape((5,2)).T)
print(zielfunk(result.x))
x,*_=hyperplanes_verlauf(x_0.reshape((5,2)).T,emb_dim=4,emb_delay=1)
a,*_=hyperplanes_verlauf(result.x.reshape((5,2)).T,emb_dim=4,emb_delay=1)
print(x,a)

