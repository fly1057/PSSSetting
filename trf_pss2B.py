# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

def fun_PSS2B(x):
    Tw3=5
    T7=5
    w1=2*np.pi*np.linspace(0.1,2,num=20)


    phasePSS=np.array(180/(np.pi)*(( np.pi/2.0-np.arctan(Tw3*w1) )-np.arctan(T7*w1)\
                    +np.arctan(x[0]*w1)-np.arctan(x[1]*w1)\
                    +np.arctan(x[2]*w1)-np.arctan(x[3]*w1) ))
 
    
#    phaseAVR=np.array([-8,-15,-22,-32,-41,-48,-52,-57,-62,-66,\
#                   -68,-72,-73,-75,	-78,-80,-83,-84,-86,	-89])
   
    
#广科项目单机 xl=0.4//0.4
#    phaseAVR=np.array([-14,-39,-55,-64,-68,-72,-74,-76,-77,-79,\
#                   -81,-83,-87,-93,-98,-97,-94,-92,-91,-91])

#广科项目三机 xl=0.14//0.14
    phaseAVR=np.array([-16,-41,-56,-63,-68,-71,-73,-75,-77,-79,\
                   -82,-88,-94,92,-92,-93,-93,-92,-92,-91])
    

    

    phasePSS_need=-90-phaseAVR
    
    return (phasePSS-phasePSS_need)  

def plot_pss2B(x):
    Tw3=5
    T7=5
    w1=2*np.pi*np.linspace(0.1,2,num=20)
    phasePSS=np.array(180/(np.pi)*(( np.pi/2.0-np.arctan(Tw3*w1) )-np.arctan(T7*w1)\
                    +np.arctan(x[0]*w1)-np.arctan(x[1]*w1)\
                    +np.arctan(x[2]*w1)-np.arctan(x[3]*w1) ))

#    phaseAVR=np.array([-8,-15,-22,-32,-41,-48,-52,-57,-62,-66,\
#                   -68,-72,-73,-75,	-78,-80,-83,-84,-86,	-89
#                   ])
#    phaseAVR=np.array([-8,-15,-22,-32,-41,-48,-52,-57,-62,-66,\
#                   -68,-72,-73,-75,	-78,-80,-83,-84,-86,	-89])
 
#广科项目单机 xl=0.4//0.4
    phaseAVR=np.array([-14,-39,-55,-64,-68,-72,-74,-76,-77,-79,\
                   -81,-83,-87,-93,-98,-97,-94,-92,-91,-91])

#广科项目三机 xl=0.14//0.14
    phaseAVR=np.array([-16,-41,-56,-63,-68,-71,-73,-75,-77,-79,\
                   -82,-88,-94,92,-92,-93,-93,-92,-92,-91])
    
    phaseSUM=phasePSS+phaseAVR
    plt.plot(np.linspace(0.1,2,num=20),phaseSUM,\
             np.linspace(0.1,2,num=20),phaseAVR,\
             np.linspace(0.1,2,num=20),phasePSS )
    plt.grid()
    plt.xlabel("f /Hz")
    plt.ylabel("phase /degree")
    plt.ylim([-120,10])
    
    return phaseSUM

x0_PSS2B = np.array([0.2,0.01,0.2,0.01 ])

counter=0
lb=np.array([0.01,0.01,0.01,0.01])
ub=np.array([0.5,0.5 ,0.5,0.5])
bounds=(lb, ub)

for counter in range(100):
    res_3 = least_squares(fun_PSS2B,x0_PSS2B,ftol=0.01 ,bounds=(lb, ub), method='trf' )
# lm方法不行，没有约束条件就会使值变负
#    res_3 = least_squares(fun_PSS2B,x0_PSS2B,ftol=0.01 , method='lm' )
    x0_PSS2B=res_3.x
    counter=counter+1
print res_3.x
print res_3.cost

phaseSUM=plot_pss2B(res_3.x)


