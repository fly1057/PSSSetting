# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 22:07:09 2017

@author: ll
"""



# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

def fun_PSS3B(x):
#    TD=5
    w1=2*np.pi*np.linspace(0.1,2,num=20)


# 用于PSS3B   
    phasePSS=np.array(180/(np.pi)*( np.pi/2.0-np.arctan(x[4]*w1) \
                    +2*(  np.arctan(x[0]*w1)-np.arctan(x[1]*w1)\
                         +np.arctan(x[2]*w1)-np.arctan(x[3]*w1)   ) 
                                  ))

    PhaseAVR=np.array([-13,-24,-34,-42,-48,-53,-57,-61,-64,-66,\
                   -68,-70,-71,-72,	-73,-74,-75,-76,-77,	-77])
   

    

    

    phasePSS_need=-90-PhaseAVR
    
    return (phasePSS-phasePSS_need)  

def plot_pss3B(x):
#    TD=5
    w1=2*np.pi*np.linspace(0.1,2,num=20)
    phasePSS=np.array(180/(np.pi)*( np.pi/2.0-np.arctan(x[4]*w1) \
                    +2*(  np.arctan(x[0]*w1)-np.arctan(x[1]*w1)\
                         +np.arctan(x[2]*w1)-np.arctan(x[3]*w1)   ) 
                                  ))

    phaseAVR=np.array([-13,-24,-34,-42,-48,-53,-57,-61,-64,-66,\
                   -68,-70,-71,-72,	-73,-74,-75,-76,-77,	-77])
   

    phaseSUM=phasePSS+phaseAVR
    plt.plot(np.linspace(0.1,2,num=20),phaseSUM,\
             np.linspace(0.1,2,num=20),phaseAVR,\
             np.linspace(0.1,2,num=20),phasePSS )
    plt.grid()
    plt.xlabel("f /Hz")
    plt.ylabel("phase /degree")
    plt.ylim([-120,10])
    
    return phaseSUM

#x0_PSS2B = np.array([0.5,4.6,0.1,0.01 ])
x0_PSS3B = np.array([0.2,0.2,0.2,0.2 ,5])
x_PSS3B=x0_PSS3B

counter=0
lb=np.array([0.01,0.01,0.01,0.01,4.999])
ub=np.array([6   ,100    ,6   ,6  ,5.001 ])
bounds=(lb, ub)

for counter in range(100):
    res_3 = least_squares(fun_PSS3B,x_PSS3B,ftol=0.01 ,bounds=(lb, ub), method='trf' )
# lm方法不行，没有约束条件就会使值变负
#    res_3 = least_squares(fun_PSS2B,x0_PSS2B,ftol=0.01 , method='lm' )
    x_PSS3B=res_3.x
    counter=counter+1
print res_3.x
print res_3.cost

phaseSUM=plot_pss3B(res_3.x)


