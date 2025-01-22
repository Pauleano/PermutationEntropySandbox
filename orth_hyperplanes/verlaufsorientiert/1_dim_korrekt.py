import numpy as np
import matplotlib.pyplot as plt

def gaus(x):
        if x<0:
            out=0
        else:
            out=(x**2+x)*0.5    
        return int(out)



#same as PE just different symbolisation
def verlauf_orth_1D(datareihe):
    #input ist keine ganze reihe sondern nur der zu betrachtende ausschnitt
    #output ist symbol _|__|___|...

    #relev_diff nicht zwanghaft array, könnte auch nur eine variable sein aber somit kann anschließend kontrolliert werden ob werte richtig waren
    relev_diff=np.zeros((1,gaus(datareihe.shape[1])-1))

    word=[]
    counter=0
    for i in range(1,datareihe.shape[1]):
        if i>1:
            word.append('|')
        for j in range(0,i):
            
            relev_diff[:,counter]=datareihe[:,i]-datareihe[:,j]
            if relev_diff[0,counter]>0:
                word.append('+')
            elif relev_diff[0,counter]<0:
                word.append('-')
            else:
                 word.append('0')
            counter+=1
    symbol=''.join(word)
    
    return symbol




def multivar_planes_verlauf_1D(multivar_data,emb_dim,emb_delay):
    #raussuchen relevante ausschnitte dann verwendung funktion verlauf_orth_1D für relevanter ausschnitt

    #for i in range(anzahl der fenster):
    
    words=[]
    for i in range(multivar_data.shape[1]-emb_dim*emb_delay):
        
        #relevante daten aus reihe lesen |data in ausschnitt|=emb_dim+1
        relev_ausschnitt=np.zeros((multivar_data.shape[0],emb_dim+1))
        for j in range(emb_dim+1):
            relev_ausschnitt[:,j]=multivar_data[:,i+j*emb_delay]
        
        wort=verlauf_orth_1D(relev_ausschnitt)
        words.append(wort)
                
    #output mithilf np.unique bekommen (input zwar liste nicht array aber unique macht als erstes array draus)
    [list_of_words,abfolge_words,haeuf_words]=np.unique(words,return_inverse=True, return_counts=True)

    return list_of_words,abfolge_words,haeuf_words



import itertools as iter
#outputs all possible arrangements of 0,1,2,3,...,number
def all_combinations(number):
    laenge=number 
    zahlen=[]
    for i in range(laenge):
        zahlen.append(str(i))
    zahlen=''.join(zahlen)

    kombis=iter.permutations(zahlen,laenge)
    return list(kombis)





print(all_combinations(5))


#testing 
'''
laenge=3
vektor=np.zeros((1,laenge))
musterliste=[]

for i in kombis:
    vektor[0,:]=i
    symb=verlauf_orth_1D(vektor)
    musterliste.append(symb)
[muster,index,haeufigkeiten]=np.unique(musterliste,return_inverse=True, return_counts=True)
print(muster)
print(index)
print(haeufigkeiten)


#anfang ergebnisse für alle anordnungen  x Punkte|emb_dim= x-1| x-1 Ebenen:
2 Punkte|emb_dim=1|1 Ebene                                                
['+' '-']
[0 1]
[1 1]


3 Punkte|2 Ebenen
['+|++' '+|+-' '+|--' '-|++' '-|-+' '-|--']
[0 1 3 2 4 5]
[1 1 1 1 1 1]


4 Punkte|3 Ebenen
['+|++|+++' '+|++|++-' '+|++|+--' '+|++|---' '+|+-|+++' '+|+-|+-+'
 '+|+-|+--' '+|+-|---' '+|--|+++' '+|--|+-+' '+|--|--+' '+|--|---'
 '-|++|+++' '-|++|++-' '-|++|-+-' '-|++|---' '-|-+|+++' '-|-+|-++'
 '-|-+|-+-' '-|-+|---' '-|--|+++' '-|--|-++' '-|--|--+' '-|--|---']
[ 0  1  4  2  5  6 12 13  8  3  9  7 16 14 20 15 10 11 17 18 21 19 22 23]
[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]


5 Punkte|4 Ebenen
['+|++|+++|++++' '+|++|+++|+++-' '+|++|+++|++--' '+|++|+++|+---'
 '+|++|+++|----' '+|++|++-|++++' '+|++|++-|++-+' '+|++|++-|++--'
 '+|++|++-|+---' '+|++|++-|----' '+|++|+--|++++' '+|++|+--|++-+'
 '+|++|+--|+--+' '+|++|+--|+---' '+|++|+--|----' '+|++|---|++++'
 '+|++|---|++-+' '+|++|---|+--+' '+|++|---|---+' '+|++|---|----'
 '+|+-|+++|++++' '+|+-|+++|+++-' '+|+-|+++|+-+-' '+|+-|+++|+---'
 '+|+-|+++|----' '+|+-|+-+|++++' '+|+-|+-+|+-++' '+|+-|+-+|+-+-'
 '+|+-|+-+|+---' '+|+-|+-+|----' '+|+-|+--|++++' '+|+-|+--|+-++'
 '+|+-|+--|+--+' '+|+-|+--|+---' '+|+-|+--|----' '+|+-|---|++++'
 '+|+-|---|+-++' '+|+-|---|+--+' '+|+-|---|---+' '+|+-|---|----'
 '+|--|+++|++++' '+|--|+++|+++-' '+|--|+++|+-+-' '+|--|+++|--+-'
 '+|--|+++|----' '+|--|+-+|++++' '+|--|+-+|+-++' '+|--|+-+|+-+-'
 '+|--|+-+|--+-' '+|--|+-+|----' '+|--|--+|++++' '+|--|--+|+-++'
 '+|--|--+|--++' '+|--|--+|--+-' '+|--|--+|----' '+|--|---|++++'
 '+|--|---|+-++' '+|--|---|--++' '+|--|---|---+' '+|--|---|----'
 '-|++|+++|++++' '-|++|+++|+++-' '-|++|+++|++--' '-|++|+++|-+--'
 '-|++|+++|----' '-|++|++-|++++' '-|++|++-|++-+' '-|++|++-|++--'
 '-|++|++-|-+--' '-|++|++-|----' '-|++|-+-|++++' '-|++|-+-|++-+'
 '-|++|-+-|-+-+' '-|++|-+-|-+--' '-|++|-+-|----' '-|++|---|++++'
 '-|++|---|++-+' '-|++|---|-+-+' '-|++|---|---+' '-|++|---|----'
 '-|-+|+++|++++' '-|-+|+++|+++-' '-|-+|+++|-++-' '-|-+|+++|-+--'
 '-|-+|+++|----' '-|-+|-++|++++' '-|-+|-++|-+++' '-|-+|-++|-++-'
 '-|-+|-++|-+--' '-|-+|-++|----' '-|-+|-+-|++++' '-|-+|-+-|-+++'
 '-|-+|-+-|-+-+' '-|-+|-+-|-+--' '-|-+|-+-|----' '-|-+|---|++++'
 '-|-+|---|-+++' '-|-+|---|-+-+' '-|-+|---|---+' '-|-+|---|----'
 '-|--|+++|++++' '-|--|+++|+++-' '-|--|+++|-++-' '-|--|+++|--+-'
 '-|--|+++|----' '-|--|-++|++++' '-|--|-++|-+++' '-|--|-++|-++-'
 '-|--|-++|--+-' '-|--|-++|----' '-|--|--+|++++' '-|--|--+|-+++'
 '-|--|--+|--++' '-|--|--+|--+-' '-|--|--+|----' '-|--|---|++++'
 '-|--|---|-+++' '-|--|---|--++' '-|--|---|---+' '-|--|---|----']
[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1]
'''
#ende ergebnisse kombis




#logistic map
'''
def logi_map(alpha,laeng,x_null): 
    #alpha in [0,4];x_null in [0,1]  
    out=np.zeros((1,laeng))
    out[0,0]=x_null
    for i in range(1,laeng):
        out[0,i]=alpha*out[0,i-1]*(1-out[0,i-1])
    return out




import time

r=2.8
lang=100000
startpunkt=0.5
gotime=time.time()
reihe=logi_map(r,lang,startpunkt)
print("genrating took %s sekonds"%(time.time()-gotime))
emb_dimen=1
emb_dela=1


start=time.time()

[muster,index,haeufigkeiten]=multivar_planes_verlauf_1D(reihe,emb_dimen,emb_dela)
print(muster)
print(haeufigkeiten)
print('2zones took %s sekonds' %(time.time()-start))


#import matplotlib.pyplot as plt
#x=np.arange(lang).reshape(1,lang)
#plt.plot(x,reihe,'.-')
#plt.show()

logistic_alpha=[2.8,3.2,3.5,3.6,3.83,3.9]

for i in range(len(logistic_alpha)):
    reihe=logi_map(logistic_alpha[i],lang,startpunkt)
    for embed in range(2,7):
        [muster,index,haeufigkeiten]=multivar_planes_verlauf_1D(reihe,embed,emb_dela)
        print(muster)
        print(haeufigkeiten)
'''

