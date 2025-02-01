import numpy as np
import random as ran
import time



def twodim_sorting(x_values,y_values):
    LAMBDA_matrix=np.zeros((len(x_values),len(x_values)),dtype=int)
    #mit e statt klein_omega

    
    for i in range(len(x_values)):
        rays_left=[]
        ray_up=[]
        rays_right=[]
        ray_down=[]

        #number of true/original points on ray_up
        n_k_up=0    

        u_values=x_values-x_values[i]
        v_values=y_values-y_values[i]

        for j in range(len(x_values)):
            if (u_values[j]==0):
                if (v_values[j]==0):
                    LAMBDA_matrix[i,j]=-1
                elif (v_values[j]<0):
                    ray_down.append(j)
                    ray_up.append(j+len(x_values))
                else:
                    ray_up.append(j)
                    n_k_up+=1
                    ray_down.append(j+len(x_values))
            elif (u_values[j]>0):
                rays_right.append(j)
                rays_left.append(j+len(x_values))
            else:
                rays_left.append(j)
                rays_right.append(j+len(x_values))
        
            

#matrizen von rays_right und rays_left
#erste und letzte zeile sind immer ganzzahlig (aber als float in der matrix)
        if (len(rays_right)>=1):
            matrix_right=np.zeros((3,len(rays_right)))
            matrix_right[0,:]=rays_right
            for k in range(len(rays_right)):
                if (matrix_right[0,k]>=len(x_values)):
                    matrix_right[1,k]=v_values[int(matrix_right[0,k]-len(x_values))]/u_values[int(matrix_right[0,k]-len(x_values))]
                else:
                    matrix_right[1,k]=v_values[int(matrix_right[0,k])]/u_values[int(matrix_right[0,k])]
            #uniq_sequence wird immer mit ausgegeben
            uniq_seq,verlauf=np.unique(matrix_right[1,:],return_inverse=True)
            matrix_right[2,:]=verlauf

        if (len(rays_left)>=1):
            matrix_left=np.zeros((3,len(rays_left)))
            matrix_left[0,:]=rays_left
            for k in range(len(rays_left)):
                if (matrix_left[0,k]>=len(x_values)):
                    matrix_left[1,k]=v_values[int(matrix_left[0,k]-len(x_values))]/u_values[int(matrix_left[0,k]-len(x_values))]
                else:
                    matrix_left[1,k]=v_values[int(matrix_left[0,k])]/u_values[int(matrix_left[0,k])]
            #uniq_sequence wird immer mit ausgegeben
            uniq_seq,verlauf=np.unique(matrix_left[1,:],return_inverse=True)
            #anzahl der vorherigen rays wird aufaddiert
            if (len(ray_up)>0):
                matrix_left[2,:]=verlauf+len(rays_right)+1

            else:
                matrix_left[2,:]=verlauf+len(rays_right)    
        
        #erstellen von k_matrix... 1.zeile sind alle punkte....2.zeile ist nummer des rays des punktes
        if len(ray_up)>0:
            k_matrix=np.zeros((2,len(rays_right)+len(ray_up)+len(rays_left)+len(ray_down)))
            k_matrix[0,:]=np.concatenate((matrix_right[0,:],np.array(ray_up),matrix_left[0,:],np.array(ray_down)))
            k_matrix[1,:]=np.concatenate((matrix_right[2,:],np.zeros(len(ray_up))+len(rays_right),matrix_left[2,:],np.zeros(len(ray_down))+k_matrix.shape[1]-1))
        else:
            k_matrix=np.zeros((2,len(rays_right)+len(rays_left)))
            k_matrix[0,:]=np.concatenate((matrix_right[0,:],matrix_left[0,:]))
            k_matrix[1,:]=np.concatenate((matrix_right[2,:],matrix_left[2,:]))
        
        #n_k bestimmen für alle rays   
        
        if len(ray_up)>0:
            n_k_array=np.zeros(len(rays_right)+len(rays_left)+2)
        else:
            n_k_array=np.zeros(len(rays_right)+len(rays_left))

        for k in range(n_k_array.shape[0]):
                if k_matrix[0,k]<len(x_values):
                    n_k_array[int(k_matrix[1,k])]+=1
                
        

        #berechnung LAMBDA_matrix Zeileneinträge
        for j in range(len(x_values)):
            if (LAMBDA_matrix[i,j]!=-1):
                lauf1=0
                lauf2=0
                while (k_matrix[0,lauf1]!=j):
                    lauf1+=1
                while k_matrix[0,lauf2]!=j+len(x_values):
                    lauf2+=1

                #summierung n_k von 1 danach bis 1 davor (nach hinten wieder vorne anfangen)
                if k_matrix[1,lauf2]>k_matrix[1,lauf1]:
                    LAMBDA_matrix[i,j]=np.sum(n_k_array[int(k_matrix[1,lauf1])+1:int(k_matrix[1,lauf2])])
                else:
                    LAMBDA_matrix[i,j]=np.sum(n_k_array[int(k_matrix[1,lauf1])+1:])+np.sum(n_k_array[0:int(k_matrix[1,lauf2])])

    #print(k_matrix)
    #print(n_k_array)
    
    return LAMBDA_matrix



def twodim_sorting_verlauf(twodim_data,emb_dim,emb_delay):
        
    LAMBDA_matrizen=[]
    for i in range(twodim_data.shape[1]-emb_dim*emb_delay):
        
        #relevante daten aus reihe lesen |data in ausschnitt|=emb_dim+1
        relev_ausschnitt=np.zeros((twodim_data.shape[0],emb_dim))
        for j in range(emb_dim):
            relev_ausschnitt[:,j]=twodim_data[:,i+j*emb_delay]
        laufmatrix=twodim_sorting(relev_ausschnitt[0,:],relev_ausschnitt[1,:])
        LAMBDA_matrizen.append(np.array2string(laufmatrix))
    #print(LAMBDA_matrizen)
    return np.unique(LAMBDA_matrizen,return_counts=True,return_inverse=True) 



datalae=100000

datareihe=np.zeros((2,datalae))
datareihe[:,0]=0
for i in range(1,datalae):
    for j in range(2):
        datareihe[j,i]=ran.random()*10

print(datareihe)
matrizen,indexe,freq=twodim_sorting_verlauf(datareihe,emb_delay=1,emb_dim=5)
print(matrizen)
print(indexe)
print(freq)


#x_werte=np.array([0,1,1])
#y_werte=np.array([0,0,1])
#now=time.time()
#raya,rayb,rayc,rayd,matrixa,matrixb,lambdamatrix=twodim_sorting(x_werte,y_werte)
#print(time.time()-now)

#print(raya)
#print(rayb)
#print(rayc)
#print(rayd)
#print(matrixa)
#print(matrixb)
#print(np.array2string(lambdamatrix.flatten()))
