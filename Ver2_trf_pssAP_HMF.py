# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

def Func_Initial_PSSAP():
    T1=0.02
    T2=0.02
    T3=4.22
    T4=4.22
    T5=4.22
    T6=2.15
    K=1
    K1=6.77
    K2=0.5
    a=1
    p=0.5
    w0=2*np.pi*np.linspace(0.1,2,num=20)
    x0=np.array([T1,T2,T3,T4,T5,T6,K,K1,K2,a,p])
    
    lb=np.array([0.0199,0.0199,4.219,4.219,4.219,2.149,0.999,6.769,0.49,0.69,0.01])
    ub=np.array([0.0201,0.0201,4.221,4.221,4.221,2.151,1.001,6.771,0.51,1.91,2   ])
    bounds=(lb, ub)
     
    #HMF1
#    Phase_AVR=np.array([-20,-22,-27,-32,-36,-37,-41,-42,-45,-49,\
#                       -54,-60,-73,-80,-93,-101,-79,-76,-70,-63])    
     #HMF2
    Phase_AVR=np.array([-20,-25,-29,-33,-36,-41,-42,-45,-46,-49,\
                       -54,-56,-67,-78,-87,-95,-81,-74,-69,-68]) 
    
    
    return x0,w0,Phase_AVR,bounds




def Func_Parameter_Calculate(x,w,Phase_AVR,bounds):

    def Func_Phase_PSSAP(x):
        
        T1,T2,T3,T4,T5,T6,K,K1,K2,a,p=x
        w=2*np.pi*np.linspace(0.1,2,num=20)
        print p
       
        if    p>0 and p<1:
            n = a*K2 + a*K1*p - a*K2*p
            m = (a*K2*T6 - a*K2*p*T6)/n   
           
        elif  p>1 and p<2:
            n = 2*a*K1 + a*K2 - a*K1*p - a*K2*p
            m = (a*K2*T6 - a*K2*p*T6)/n           
        
        Phase_PSSAP=np.array( 180/(np.pi)*( -np.arctan(T1*w) -np.arctan(T2*w)\
                +np.pi/2.0 -np.arctan(T3*w) + np.pi/2.0-np.arctan(T4*w)\
                +np.pi/2.0 -np.arctan(T5*w) + np.arctan(m*w)-np.arctan(T6*w)  ))          
    
        Phase_PSSAP_need=-90-Phase_AVR
        
        return  (Phase_PSSAP-Phase_PSSAP_need)  
    
    lb, ub=bounds
    counter=0
                          
    for counter in range(100):
        res = least_squares(Func_Phase_PSSAP,x,ftol=0.0001 ,bounds=(lb, ub), method='trf' )
        x=res.x
        counter=counter+1
        print counter,x
    
    return res.x,w,Phase_AVR,res


def Func_Plot_PSSAP(x,w,PhaseAVR):
    T1,T2,T3,T4,T5,T6,K,K1,K2,a,p=x;
    w=w;
    PhaseAVR=PhaseAVR;
    
    if    p>0 and p<1:
       n = a*K2 + a*K1*p - a*K2*p
       m = (a*K2*T6 - a*K2*p*T6)/n
    
           
    elif  p>1 and p<2:
       n = 2*a*K1 + a*K2 - a*K1*p - a*K2*p
       m = (a*K2*T6 - a*K2*p*T6)/n     

    PhasePSS=np.array(180/(np.pi)*( -np.arctan(T1*w) -np.arctan(T2*w)\
                +np.pi/2.0 -np.arctan(T3*w) + np.pi/2.0-np.arctan(T4*w)\
                +np.pi/2.0 -np.arctan(T5*w) + np.arctan(m*w)-np.arctan(T6*w)  ))  

    PhaseSUM=PhasePSS+PhaseAVR
    
    plt.plot(np.linspace(0.1,2,num=20),PhaseSUM,linestyle='-.')
    plt.plot(np.linspace(0.1,2,num=20),PhaseAVR,linestyle='-')
    plt.plot(np.linspace(0.1,2,num=20),PhasePSS,linestyle=':')
    plt.legend(['AVR+PSS','AVR','PSS'])
    
    plt.grid()
    plt.xlabel("f /Hz")
    plt.ylabel("phase /degree")
    plt.ylim([-150,10])
    
    return PhaseSUM,n





x0,w0,Phase_AVR,bounds=Func_Initial_PSSAP();
x,w,Phase_AVR,res=Func_Parameter_Calculate(x0,w0,Phase_AVR,bounds);
PhaseSUM,n=Func_Plot_PSSAP(x,w,Phase_AVR);



