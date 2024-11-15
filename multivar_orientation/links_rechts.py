import numpy as np
import math
import itertools as iter









#start funktionen



def verlauf_2d(multivar_data,emb_dim,emb_delay):
    #for i in range(anzahl der fenster):
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
                plane=relev_diff[:,gaus(k-1)]
                vektor=relev_diff[:,gaus(j-2)+k]
            #mithilfe mult ergebnismatrix bestimmen :
            #ergebnismatrix=untere dreickecksmatrix
                ergebnis_matrix[j-2,k-1]=plane[0]*vektor[1]-plane[1]*vektor[0]
                
         
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






#speicherung alle 3 punkte rotation
#wie verlauf_2D aber mehr vergleiche 
def rotationen_3_punkte(multivar_data,emb_dim,emb_delay):
    
    #alle 3punkte komb ...einschränkung max fensterlänge=10 (0,1,2,3,4,5,6,7,8,9)
    zahlen=[]
    for m in range(emb_dim+1):
        zahlen.append(str(m))
    zahlen=''.join(zahlen)
    
    indexe=np.zeros((1,3))

    #for i in range(anzahl der fenster):
    words=[]
    for i in range(multivar_data.shape[1]-emb_dim*emb_delay):
        
        #relevante daten aus reihe lesen |data in ausschnitt|=emb_dim+1
        relev_ausschnitt=np.zeros((multivar_data.shape[0],emb_dim+1))
        #print(relev_ausschnitt)
        for j in range(relev_ausschnitt.shape[1]):
            relev_ausschnitt[:,j]=multivar_data[:,i+j*emb_delay]
        
        ergebnis_matrix=np.zeros((1,math.comb(emb_dim+1,3)))
        counter=0
        kombis=iter.combinations(zahlen,3)
        #für jeden neuen punkt differenzen zu bisherigen ebenenpunkten berechnen
        for z in kombis:
            indexe[0,:]=z
            #print(indexe)
            eins=int(indexe[0,0])
            zwei=int(indexe[0,1])
            drei=int(indexe[0,2])

            diff1=relev_ausschnitt[:,eins]-relev_ausschnitt[:,zwei]
            diff2=relev_ausschnitt[:,zwei]-relev_ausschnitt[:,drei]

            ergebnis_matrix[0,counter]=diff1[0]*diff2[1]-diff1[1]*diff2[0]
            counter+=1
        #mithilfe ergebnismatrix wort bestimmen und in wörterliste packen
        #zeilenweise die matrix durchgehen
        #print(ergebnis_matrix)
        wordpart=[]
        for k in range(ergebnis_matrix.shape[1]):
                if ergebnis_matrix[0,k]<0:
                    wordpart.append('-')
                elif ergebnis_matrix[0,k]>0:
                    wordpart.append('+')
                else:
                    wordpart.append('0')

        words.append(''.join(wordpart))
                
    #output mithilf np.unique bekommen (input zwar liste nicht array aber unique macht als erstes array draus)
    [list_of_words,abfolge_words,haeuf_words]=np.unique(words,return_inverse=True, return_counts=True)

    return list_of_words,abfolge_words,haeuf_words










#gaussian spaziergang (random walk with gaussian increments)
import time
import random as ran
import matplotlib.pyplot as plt


parametercount=2
delay=1
embedding_dim=3
datalae=100000

'''
mü=0
standev=1
spaziergang2=np.zeros((parametercount,datalae))
start=time.time()
for i in range(1,datalae):
    for j in range(parametercount):
        spaziergang2[j,i]=spaziergang2[j,i-1]+ran.gauss(mü,standev) #normal distribution
print('spaziergang took %s sec.' %(time.time()-start))
[muster3,index3,haeufigkeiten3]=rotationen_3_punkte(spaziergang2,emb_delay=delay,emb_dim=embedding_dim)
print(muster3)
print(haeufigkeiten3)

plt.plot(spaziergang2[0,:],spaziergang2[1,:])
plt.show()

#plt.stairs(haeufigkeiten3)
'''


#output rotationen_3_punkte
'''
['+' '-']
[50080 49918]

['++++' '+++-' '++-+' '++--' '+-++' '+--+' '+---' '-+++' '-++-' '-+--'
 '--++' '--+-' '---+' '----']
[16669  6364  2041 12406  2147  4224  6262  6304  4087  2035 12464  2003
  6264 16727]

['++++++++++' '+++++++++-' '++++++++--' '+++++++---' '++++++-+++'
 '++++++--++' '++++++---+' '++++++----' '+++++-++++' '+++++-++-+'
 '+++++-++--' '+++++-+---' '+++++--+++' '+++++---++' '+++++---+-'
 '+++++-----' '++++--++++' '++++--++-+' '++++--+--+' '++++--+---'
 '++++---+++' '++++---++-' '++++----+-' '++++------' '+++-+++++-'
 '+++-++++--' '+++-+++--+' '+++-+++---' '+++-++-+++' '+++-++-++-'
 '+++-++--++' '+++-++---+' '+++--++++-' '+++--+++-+' '+++--+++--'
 '+++--++--+' '+++--+-++-' '+++--+--++' '+++--+--+-' '+++--+---+'
 '+++---++++' '+++---+++-' '+++---++-+' '+++---+--+' '+++----++-'
 '+++-----+-' '+++------+' '+++-------' '++-+++++++' '++-++++++-'
 '++-+++-+++' '++-+-+++++' '++-+-++-++' '++-+-+-+++' '++-+--++++'
 '++-+--+-++' '++-+--+--+' '++-+--+---' '++-+---+++' '++-+---++-'
 '++-+---+--' '++-+------' '++--+++++-' '++--++-+++' '++--++-++-'
 '++--+-+++-' '++--+--++-' '++--+--+--' '++----++++' '++----+++-'
 '++----+-++' '++----+--+' '++-----++-' '++-----+--' '++-------+'
 '++--------' '+-+++-++-+' '+-+++-++--' '+-+++-+---' '+-++-+++-+'
 '+-++-++-++' '+-++-++--+' '+-++--++-+' '+-++--+--+' '+-++--+---'
 '+-+-++++--' '+-+-+++-++' '+-+-+++--+' '+-+-+++---' '+-+-++-+++'
 '+-+-++-++-' '+-+-++-+--' '+-+-++--++' '+-+-+-++--' '+-+-+-+---'
 '+-+-+--+--' '+-+--+++-+' '+-+--+++--' '+-+--++-++' '+-+--++--+'
 '+-+--+-++-' '+-+--+-+--' '+-+--+--++' '+-+--+--+-' '+--+++++++'
 '+--++++++-' '+--+++++-+' '+--++-+++-' '+--++-++-+' '+--++-++--'
 '+--+-+++++' '+--+-+++-+' '+--+-++-++' '+---+-+++-' '+---+-++--'
 '+---+--+--' '+----+++++' '+----+++-+' '+----+++--' '+----++-++'
 '+----+-+--' '+----+--++' '+----+--+-' '+----+----' '+-----++++'
 '+-----+++-' '+-----++--' '+-----+-++' '+------+--' '+-------++'
 '+--------+' '+---------' '-+++++++++' '-++++++++-' '-+++++++--'
 '-++++++-++' '-+++++-+--' '-+++++--++' '-+++++---+' '-+++++----'
 '-++++-++++' '-++++-++-+' '-++++-++--' '-++++-+-++' '-++++--+--'
 '-++++---++' '-++++---+-' '-++++-----' '-+++-++-++' '-+++-+--++'
 '-+++-+---+' '-++-+--+--' '-++-+---+-' '-++-+-----' '-++--+--++'
 '-++--+--+-' '-++--+---+' '-++-----+-' '-++------+' '-++-------'
 '-+-++-++-+' '-+-++-++--' '-+-++-+-++' '-+-++-+--+' '-+-++--++-'
 '-+-++--+--' '-+-++---++' '-+-++---+-' '-+-+-++-++' '-+-+-+-+++'
 '-+-+-+--++' '-+-+--++--' '-+-+--+-++' '-+-+--+--+' '-+-+--+---'
 '-+-+---+++' '-+-+---++-' '-+-+---+--' '-+-+----++' '-+--++-+++'
 '-+--++-++-' '-+--++--+-' '-+--+--++-' '-+--+--+--' '-+--+---+-'
 '-+---+-+++' '-+---+--++' '-+---+--+-' '--++++++++' '--+++++++-'
 '--+++++-++' '--+++++--+' '--++++-++-' '--++++-+--' '--++++---+'
 '--++++----' '--++-++-++' '--++-++--+' '--++-+---+' '--++--+--+'
 '--++--+---' '--++-----+' '--+-++++++' '--+-+++-++' '--+-+++--+'
 '--+-+++---' '--+-++-+++' '--+-++-++-' '--+-++-+--' '--+-++----'
 '--+-+-+---' '--+-+--+--' '--+-+-----' '--+---+---' '--+------+'
 '--+-------' '---+++++++' '---++++++-' '---+++++-+' '---++++--+'
 '---+++-++-' '---+++--+-' '---+++---+' '---+++----' '---++-+++-'
 '---++-++-+' '---++-++--' '---++-+--+' '---++--++-' '---++---++'
 '---++---+-' '---++----+' '---+--+++-' '---+--++--' '---+--+--+'
 '---+--+---' '---+---+++' '---+---++-' '---+----++' '---+-----+'
 '----++++++' '----++++-+' '----+++--+' '----+++---' '----++-+++'
 '----++-++-' '----++--+-' '----++----' '-----+++++' '-----+++-+'
 '-----+++--' '-----++---' '-----+-+++' '-----+--++' '-----+--+-'
 '-----+----' '------++++' '------+++-' '------++--' '------+---'
 '-------+++' '--------++' '---------+' '----------']
[4157 1689 1294  206 1203 1135  271  368  562  537 2547 1102   74   90
   63 1087  245  206  634 1099   50   35   67 1113  357  231   78   63
 1163  695 1032  180   32   39   43  171  209 1775  339  609   50   44
   21  264  193  246 1030 2567  563  118   98  263   36   48  444  216
  431  365  112  101   74  219   44  108  133   34   67   23  227  174
   97  147  281  242  361 1261   29  261   60   15   19   41   22   78
   85  270   62  105   97  271  281  175  135  171   44   41   60   69
  141  162   52   37  575   95  541  182   23   80   40  385  207   14
   44   48  188   36  630   86  127  292   43 1066  162  129  447  306
  773  146  352  387  639 1687 1657  583  398  386  135  788  272  428
  121  176 1058   40  218  116   74  637   51  192   51   33   16  209
  398   52   88   27  155  491   96  560   38   58  140  160   66   63
   45   60  158  158  172  318  308  107  110   80  261   77   82   11
   38   26   14   50  244   30 1238  379  243  244  132  110  169  195
   30   64   26  127   76   72  229   68  113  135  348  453  214  425
   55   42  250   79  145  609 2566 1059  256  174  261   25   44   42
  628  363 1758  212  153   26   24   50  152 1020  761 1089   61   61
  234  343 1095   54   42   59 1099  639  201  251 1102   79   84   93
 1069 2511  519  598  370  299 1119 1147  226 1250 1717 4296]
'''



mü=0
standev=1000000
spaziergang2=np.zeros((parametercount,datalae))
start=time.time()
for i in range(1,datalae):
    for j in range(parametercount):
        spaziergang2[j,i]=spaziergang2[j,i-1]+ran.gauss(mü,standev) #normal distribution
print('spaziergang took %s sec.' %(time.time()-start))
[muster3,index3,haeufigkeiten3]=verlauf_2d(spaziergang2,emb_delay=delay,emb_dim=embedding_dim)
print(muster3)
print(haeufigkeiten3)

plt.plot(spaziergang2[0,:],spaziergang2[1,:])
plt.show()

#outputs:
'''
['+' '-']
[49831 50167]

['+|++' '+|+-' '+|-+' '+|--' '-|++' '-|+-' '-|-+' '-|--']
[18995 18857  6312  6190  6239  6137 18809 18458]


'''