from copy import deepcopy
import numpy as np

Id = np.zeros((100,2))
passo = 0.1
Vg = 0.1
array = []
for Vds in [2,3,6]:
    for j in range(100):
        Id[j,0]=(Vg)*(Vds)     
        Id[j,1]=Vg
        Vg=Vg+(passo)

    Vg=0.1
   
    x=deepcopy(Id[:,1])
    y=deepcopy(Id[:,0])
    
    array.append(x)
    array.append(y)

print("AQUI", array)