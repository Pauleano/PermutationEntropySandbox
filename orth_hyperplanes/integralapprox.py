def flaeche(x_0,y_0,x_1,y_1):
    #print('x0'+' '+str(x_0))
    #print('y0'+' '+str(y_0))
    #print('x1'+' '+str(x_1))
    #print('y1'+' '+str(y_1))
    
    #wenn keine bewegung dann fläche=0 
    if(x_0==x_1)and(y_0==y_1):
        flaech=0
        return(flaech)
    
    #horizontale hyperebene
    if(x_1==x_0):

        if(y_0<y_1):
            flaech=1-y_1
        else:
            flaech=y_1
        return flaech

    #vertikale hyperebene
    elif(y_1==y_0):

        if(x_0<x_1):
            flaech=1-x_1
        else:
            flaech=y_1
        return flaech

    #keine der z_* wird zu +-inf
    else:
        z_L=y_1+(x_1-x_0)*((x_1)/(y_1-y_0))
        z_L=round(z_L,10)
        z_U=x_1+(y_1-y_0)*((y_1)/(x_1-x_0))
        z_U=round(z_U,10)
        z_R=y_1+(-x_1+x_0)*((1-x_1)/(y_1-y_0))
        z_R=round(z_R,10)
        z_O=x_1+(y_1-y_0)*((1-y_1)/(-x_1+x_0))
        z_O=round(z_O,10)

    #4 z_* innerhalb [0,1]
    if (z_O==0)and(z_L==1)and (z_R==0)and(z_U==1):
        flaech=0.5
        return flaech
    elif (z_O==1)and(z_L==0)and (z_R==1)and(z_U==0):
        flaech=0.5
        return flaech
             
    #3 z_* innerhalb [0,1]
    else:
    #ecke unten links
        #unten links rechts--> unten rechts
        if (z_U==0)and(z_L==0):
            if (z_R<=1)and(z_R>=0):
                z_L=-5001
            #unten links oben -->links oben
            if (z_O<=1)and(z_O>=0):
                z_U=-5002
    #ecke unten rechts
        #unten rechts links--> unten rechts
        if (z_U==1)and(z_R==0):
            if (z_L<=1)and(z_L>=0):
                z_R=-5003
        #unten rechts oben -->rechts oben
            if (z_O<=1)and(z_O>=0):
                z_U=-5004
    #ecke oben rechts
        #oben rechts links--> oben links
        if (z_O==1)and(z_R==1):
            if (z_L<=1)and(z_L>=0):
                z_R=-5005
        #oben rechts unten -->rechts unten
            if (z_U<=1)and(z_U>=0):
                z_O=-5006
    #ecke oben links
        #oben links rechts--> oben rechts
        if (z_O==0)and(z_L==1):
            if (z_R<=1)and(z_R>=0):
                z_L=-5007
        #oben links unten -->links unten
            if (z_U<=1)and(z_U>=0):
                z_O=-5008
            
    #2 z_* innerhalb [0,1]
    #gerade durch benachbarte ränder
    #oben_rechts
        if (z_O<=1)and(z_O>=0) and (z_R<=1)and(z_R>=0):     #re_ob
                if (x_0<x_1)and(y_0<y_1):#! positiv=eingeschlossenes 3eck
                    flaech=0.5*(1-z_R)*(1-z_O)
                else:
                    flaech=1-(0.5*(1-z_R)*(1-z_O))

    #oben_links
        if (z_O<=1)and(z_O>=0) and (z_L<=1)and(z_L>=0):   #li_ob
                if (x_0>x_1)and(y_0<y_1):#! positiv=eingeschlossenes 3eck
                    flaech=0.5*(z_O)*(1-z_L)
                else:
                    flaech=1-(0.5*(z_O)*(1-z_L))

    #unten_links
        if (z_L<=1)and(z_L>=0) and (z_U<=1)and(z_U>=0):   #li_un
                if (x_0>x_1)and(y_0>y_1):#! positiv=eingeschlossenes 3eck
                    flaech=0.5*(z_L)*(z_U)
                else:
                    flaech=1-(0.5*(z_L)*(z_U))

    #unten_rechts
        if (z_R<=1)and(z_R>=0) and (z_U<=1)and(z_U>=0):   #re_un
                if (x_0<x_1)and(y_0>y_1):#! positiv=eingeschlossenes 3eck
                    flaech=0.5*(1-z_U)*(z_R)
                else:
                    flaech=1-(0.5*(1-z_U)*(z_R))


    #gerade durch ggüberlieg ränder
        if (z_O<=1)and(z_O>=0) and (z_U<=1)and(z_U>=0):   #un_ob
        #vektor nach rechts
                if (x_0<x_1)and(z_O>z_U):
                    flaech=(0.5*(z_O-z_U)*1)+((1-z_O)*1)    #trapez=3eck+(rest)rechteck
                if (x_0<x_1)and(z_O<z_U):
                    flaech=(0.5*(z_U-z_O)*1)+((1-z_U)*1)    #trapez=3eck+(rest)rechteck
        #vektor nach links
                if (x_0>x_1)and(z_O>z_U):#
                    flaech=(0.5*(z_O-z_U)*1)+(z_U*1)        #trapez=3eck+rechteck
                if (x_0>x_1)and(z_O<z_U):
                    flaech=(0.5*(z_U-z_O)*1)+(z_O*1)        #trapez=3eck+rechteck


        if (z_R<=1)and(z_R>=0) and (z_L<=1)and(z_L>=0):   #li_re
        #vektor nach oben
                if (y_0<y_1)and(z_L>z_R):
                    flaech=(0.5*(z_L-z_R)*1)+((1-z_L)*1)    #trapez=3eck+(rest)rechteck
                if (y_0<y_1)and(z_L<z_R):
                    flaech=(0.5*(z_R-z_L)*1)+((1-z_R)*1)    #trapez=3eck+(rest)rechteck
        #vektor nach unten
                if (y_0>y_1)and(z_L>z_R):
                    flaech=(0.5*(z_L-z_R)*1)+(z_R*1)        #trapez=3eck+rechteck
                if (y_0>y_1)and(z_L<z_R):
                    flaech=(0.5*(z_R-z_L)*1)+(z_L*1)        #trapez=3eck+rechteck

    return flaech




summe=0
points=0
steps=81

for i in range(steps):
    a=i/steps
    print(a)
    #print(t.time())
    for j in range(steps):
        b=j/steps
        #print(b)
        for k in range(steps):
            c=k/steps
            
            for l in range(steps):
                d=l/steps
                #if(a==0.01)and(b==0.41):
                    #print(d)
                wert=flaeche(a,b,c,d)
                if(a!=c) and (b!=d): 
                    points+=1
                summe=summe+wert
print(summe/(points))




'''
#fixierung erter punkt
for k in range(steps+1):
            c=k/steps
            #print(c)
            for l in range(steps+1):
                d=l/steps
                print(d)
                wert=flaeche(0.01,0.41,c,d)
                summe=summe+wert
print(summe/(steps+1)**2)
'''
#print(flaeche(0.2,0.4,0.4,0.6))