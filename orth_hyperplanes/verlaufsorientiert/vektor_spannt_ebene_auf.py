import numpy as np
import math
import matplotlib.pyplot as plt
import time
import random as ran
import itertools as iter

#anfang funktionen

#output ist eindeutige identifizierung des verlaufs des fensters
#für 1D reihen funktionen in "1_dim_korrekt" verwenden
def multivar_planes_verlauf(multivar_data,emb_dim,emb_delay):
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



#output ist nur zeichenfolge für den letzten vektor bezüglich vorheriger ebenen
#bis rel_diff gleich
#ergebnismatrix nur ergebnisse von letztem vektor
def multivar_planes(multivar_data,emb_dim,emb_delay):
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


def shannon(haeufigk,log_basis):
    entropy=0
    #bestimmung wahrscheinlichkeiten
    haeufigk=haeufigk/haeufigk.sum()
    #berechnung entropy
    for i in haeufigk:  
        entropy=entropy-i*math.log(i,log_basis) 
    return entropy

#ende funktionen











#anfang random walks

parametercount=2
delay=1
embedding_dim=3
fensterlae=embedding_dim+1
datalae=100000



#zeitreihe aus [0,1)^parametercount
'''
datareihe=np.zeros((parametercount,datalae))
datareihe[:,0]=0
for i in range(1,datalae):
    for j in range(parametercount):
        datareihe[j,i]=ran.random()
start=time.time()
muster2,index2,haeufigkeiten2=multivar_planes_verlauf(datareihe,emb_delay=delay,emb_dim=embedding_dim)
print(time.time()-start," sekunden für ",datalae," punkte in ",parametercount," dimensionen")

#print(datareihe)
print(muster2)
print(haeufigkeiten2)

#plt.plot(datareihe[0,:],datareihe[1,:],'.-')
#plt.show()
'''



#output:
#2D 10^5 Punkte
'''
['+'     '-']
[24052 75946]

['+|++' '+|+-' '+|-+' '+|--' '-|++' '-|+-' '-|-+' '-|--']
[ 2835   7108   1699   12528   863   13374  18773  42817]

['+|++|+++' '+|++|++-' '+|++|+-+' '+|++|+--' '+|++|-++' '+|++|-+-'
 '+|++|--+' '+|++|---' '+|+-|+++' '+|+-|++-' '+|+-|+-+' '+|+-|+--'
 '+|+-|-++' '+|+-|-+-' '+|+-|--+' '+|+-|---' '+|-+|+++' '+|-+|++-'
 '+|-+|+--' '+|-+|-++' '+|-+|-+-' '+|-+|--+' '+|-+|---' '+|--|+++'
 '+|--|++-' '+|--|+-+' '+|--|+--' '+|--|-++' '+|--|-+-' '+|--|--+'
 '+|--|---' '-|++|+++' '-|++|++-' '-|++|+-+' '-|++|+--' '-|++|-++'
 '-|++|-+-' '-|++|---' '-|+-|+++' '-|+-|++-' '-|+-|+-+' '-|+-|+--'
 '-|+-|-++' '-|+-|-+-' '-|+-|--+' '-|+-|---' '-|-+|+++' '-|-+|++-'
 '-|-+|+-+' '-|-+|+--' '-|-+|-++' '-|-+|-+-' '-|-+|--+' '-|-+|---'
 '-|--|+++' '-|--|++-' '-|--|+-+' '-|--|+--' '-|--|-++' '-|--|-+-'
 '-|--|--+' '-|--|---']
[  165   487    82   729    56   157   132  1003    48   775  1022  1917
     8   211  1412  1758    12   220   237   161   205   186   615     6
  1140   129  2971   118   743  2545  4756    42    49    32   190    21
   236   224    26   207  1456  2697    15  2389   364  6262    49   232
   133  2271  2304  5565  1071  7139     6   225  2864  3685   567  7726
  8973 18970]
'''

#3D 10^5 Points
'''
['+'     '-']
[17936 82062]

['+|++' '+|+-' '+|-+' '+|--' '-|++' '-|+-' '-|-+' '-|--']
[ 1253   5138   1334   10469   515   11180  15091  55017]

['+|++|+++' '+|++|++-' '+|++|+-+' '+|++|+--' '+|++|-++' '+|++|-+-'
 '+|++|--+' '+|++|---' '+|+-|+++' '+|+-|++-' '+|+-|+-+' '+|+-|+--'
 '+|+-|-++' '+|+-|-+-' '+|+-|--+' '+|+-|---' '+|-+|+++' '+|-+|++-'
 '+|-+|+-+' '+|-+|+--' '+|-+|-++' '+|-+|-+-' '+|-+|--+' '+|-+|---'
 '+|--|+++' '+|--|++-' '+|--|+-+' '+|--|+--' '+|--|-++' '+|--|-+-'
 '+|--|--+' '+|--|---' '-|++|+++' '-|++|++-' '-|++|+-+' '-|++|+--'
 '-|++|-++' '-|++|-+-' '-|++|--+' '-|++|---' '-|+-|+++' '-|+-|++-'
 '-|+-|+-+' '-|+-|+--' '-|+-|-++' '-|+-|-+-' '-|+-|--+' '-|+-|---'
 '-|-+|+++' '-|-+|++-' '-|-+|+-+' '-|-+|+--' '-|-+|-++' '-|-+|-+-'
 '-|-+|--+' '-|-+|---' '-|--|+++' '-|--|++-' '-|--|+-+' '-|--|+--'
 '-|--|-++' '-|--|-+-' '-|--|--+' '-|--|---']
[   43   176    45   301    21    96    81   484    13   336   478  1629
     6   176   740  1751     3   122     1   183    81   194   137   650
     4   545   116  2435    56   643  1700  4935    22    38    25   109
    11   157     2   187     9   135   803  2186     8  1445   378  6117
    17   147    72  1432  1048  4199  1008  7088     4   197  1861  4650
   451  7604  8935 31470]
'''



#gaussian spaziergang 

mü=0
spaziergang2=np.zeros((parametercount,datalae))
for i in range(1,datalae):
    for j in range(parametercount):
        spaziergang2[j,i]=spaziergang2[j,i-1]+ran.gauss(0,10000000) #normal distribution

start=time.time()
[muster2,index2,haeufigkeiten2]=multivar_planes_verlauf(spaziergang2,emb_delay=delay,emb_dim=embedding_dim)
print(time.time()-start," sekunden für ",datalae," punkte in ",parametercount," dimensionen")
print(muster2)
print(haeufigkeiten2)
plt.plot(spaziergang2[0,:],spaziergang2[1,:])
plt.show()


#output:

#2D 10^5 Points

#sd=1
'''
['+' '-']
[49815 50183]

['+|++' '+|+-' '+|-+' '+|--' '-|++' '-|+-' '-|-+' '-|--']
[21742   15517  3201   9401   3090   9338   21829  15879]

['+|++|+++' '+|++|++-' '+|++|+-+' '+|++|+--' '+|++|-++' '+|++|-+-'
 '+|++|--+' '+|++|---' '+|+-|+++' '+|+-|++-' '+|+-|+-+' '+|+-|+--'
 '+|+-|-++' '+|+-|-+-' '+|+-|--+' '+|+-|---' '+|-+|+++' '+|-+|++-'
 '+|-+|+--' '+|-+|-++' '+|-+|-+-' '+|-+|--+' '+|-+|---' '+|--|+++'
 '+|--|++-' '+|--|+-+' '+|--|+--' '+|--|-++' '+|--|-+-' '+|--|--+'
 '+|--|---' '-|++|+++' '-|++|++-' '-|++|+-+' '-|++|+--' '-|++|-++'
 '-|++|-+-' '-|++|---' '-|+-|+++' '-|+-|++-' '-|+-|+-+' '-|+-|+--'
 '-|+-|-++' '-|+-|-+-' '-|+-|--+' '-|+-|---' '-|-+|+++' '-|-+|++-'
 '-|-+|+-+' '-|-+|+--' '-|-+|-++' '-|-+|-+-' '-|-+|--+' '-|-+|---'
 '-|--|+++' '-|--|++-' '-|--|+-+' '-|--|+--' '-|--|-++' '-|--|-+-'
 '-|--|--+' '-|--|---']
[8875       6349        928         2902        564         532  
352        1221        1141        3049        4460        3398   
 60         225         2339        1085        233         566  
 165        1056        428         302         429         48  
 963        320         1318        355         409         3957 
 2047       1065        410         299         479         224  
 566        181         351         395         3892        1991
 61         911         325         1309        615         527
334         1210        9090        6379        964         2831   
50          191         2394        1036        1158        3092 
4263        3327]
'''

#sd=100
'''
['+' '-']
[50060 49938]

['+|++' '+|+-' '+|-+' '+|--' '-|++' '-|+-' '-|-+' '-|--']
[22116   15467  3167   9474   3140   9235   21801  15597]

['+|++|+++' '+|++|++-' '+|++|+-+' '+|++|+--' '+|++|-++' '+|++|-+-'
 '+|++|--+' '+|++|---' '+|+-|+++' '+|+-|++-' '+|+-|+-+' '+|+-|+--'
 '+|+-|-++' '+|+-|-+-' '+|+-|--+' '+|+-|---' '+|-+|+++' '+|-+|++-'
 '+|-+|+--' '+|-+|-++' '+|-+|-+-' '+|-+|--+' '+|-+|---' '+|--|+++'
 '+|--|++-' '+|--|+-+' '+|--|+--' '+|--|-++' '+|--|-+-' '+|--|--+'
 '+|--|---' '-|++|+++' '-|++|++-' '-|++|+-+' '-|++|+--' '-|++|-++'
 '-|++|-+-' '-|++|---' '-|+-|+++' '-|+-|++-' '-|+-|+-+' '-|+-|+--'
 '-|+-|-++' '-|+-|-+-' '-|+-|--+' '-|+-|---' '-|-+|+++' '-|-+|++-'
 '-|-+|+-+' '-|-+|+--' '-|-+|-++' '-|-+|-+-' '-|-+|--+' '-|-+|---'
 '-|--|+++' '-|--|++-' '-|--|+-+' '-|--|+--' '-|--|-++' '-|--|-+-'
 '-|--|--+' '-|--|---']
[9121 6336  917 2937  579  508  320 1182 1144 3106 4305 3439   66  204
 2311 1097  213  550  163 1066  422  313  418   53  923  299 1302  357
  430 3944 2011 1044  455  285  417  238  549  172  337  400 3953 2021
   44  908  333 1331  608  499  359 1168 9031 6352  951 2863   56  220
 2311 1064 1103 3136 4375 3377]
'''

#sd=10^7
'''
['+' '-']
[49746 50252]

['+|++' '+|+-' '+|-+' '+|--' '-|++' '-|+-' '-|-+' '-|--']
[21675 15725  3109  9458  3008  9298 22175 15549] 
'''
