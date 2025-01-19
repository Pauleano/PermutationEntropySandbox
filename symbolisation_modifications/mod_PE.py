import numpy as np
import math as m
import time as t



#given array outputs number of 'open' positions in context of max_symbols-function of modified_PE-approach
def open_pos(array):
    
    #all positions open
    open_pos=array.shape[0]
    
    #starting from first 'symbol', subtract how often it occurs from open positions
    for i in range(array.shape[0]):
        
        if(open_pos==array[i]):#all positions full after current symbol->no open positions
            return 0
        
        elif(open_pos>array[i]):#still positions open after current symbol
            open_pos-=array[i]
            #print(open_pos)
        
        else:#symbol is used more than there are positions left->cant use symbol 
            return open_pos
    #there are still open positions after using following array    
    return open_pos    

def missing_pos(array):
    #does the same thing as open_pos() only slower
    return (array.shape[0]-np.sum(array))

def read_symbol(array):
    #=np.sum(np.sign(array)) gives same result but slower
    counter=0
    for i in range(array.shape[0]):
         if (array[i]!=0):
            counter+=1
    return counter
    
def max_symbols(emb_dim):
    symb_count=0
    markers=np.zeros(emb_dim)+1
    while(markers[0]!=emb_dim):
        if(open_pos(markers)==0):
            symb_count+=m.factorial(read_symbol(markers))
            print(markers)
        for i in range(emb_dim-1,-1,-1):
            if(markers[i]==emb_dim-1-i+1):
                if i==0:#prevent markers[0]=0
                    break
                markers[i]=0
                markers[i-1]+=1
                if open_pos(markers)==0:
                    symb_count+=m.factorial(read_symbol(markers))
            elif open_pos(markers)==0:
                if markers[i]==0:
                    continue
                else:
                    markers[i]=0
                    markers[i-1]+=1
                    break
            else:
                open=int(open_pos(markers))
                markers[emb_dim-open:]=1
                break
    if emb_dim==2:
        return symb_count #all valid symbols already have been counted
        
    return symb_count+1 #with emb_dim>=3 while loop terminated before counting symbol (emb__dim,0,0,0,...)


x=np.zeros(5)
print(x)
x[0:]=[5,0,0,0,0]
print(x)
#max_symbols-function endless loop with emb_dim=2
print(max_symbols(2))

ranges=100000

times=t.time()
for i in range(ranges):
    missing_pos(x)
print(t.time()-times)

times=t.time()
for i in range(ranges):
    open_pos(x)
print(t.time()-times)
