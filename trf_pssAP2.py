# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 15:04:14 2017

@author: ll
"""

import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
#import wx

#定义用于最优化的函数，由于最优化是针对标量进行最优化，因此这个函数的输入变量
#就是需要优化的参数，因此只能有一个参数，输出参数是标量
def Func_PSSAP(x):

#    T1,T2,T3,T4,T5,T6,K,K1,K2,a,p=x
    T5,T6,K1,K2,a,p=x;

    if    p>0 and p<1:
            n = a*K2 + a*K1*p - a*K2*p
            m = (a*K2*T6 - a*K2*p*T6)/n   
           
    elif  p>1 and p<2:
            n = 2*a*K1 + a*K2 - a*K1*p - a*K2*p
            m = (a*K2*T6 - a*K2*p*T6)/n           
        
    Phase_PSSAP=np.array(180/(np.pi)*( -np.arctan2(T1*w,1) -np.arctan2(T2*w,1)\
                +np.pi/2.0 -np.arctan2(T3*w,1) + np.pi/2.0-np.arctan2(T4*w,1)\
                +np.pi/2.0 -np.arctan2(T5*w,1) + np.arctan2(m*w,1)-np.arctan2(T6*w,1)  ))  

    Phase_PSSAP_need=-90-PhaseAVR
        
#    return  np.sqrt((Phase_PSSAP-Phase_PSSAP_need)*(Phase_PSSAP-Phase_PSSAP_need))  
    return  (Phase_PSSAP-Phase_PSSAP_need)


def Func_Plot_PSSAP(x,w,PhaseAVR):
#    T1,T2,T3,T4,T5,T6,K,K1,K2,a,p=x;
    T5,T6,K1,K2,a,p=x;
    
    if    p>0 and p<1:
       n = a*K2 + a*K1*p - a*K2*p
       m = (a*K2*T6 - a*K2*p*T6)/n
    
           
    elif  p>1 and p<2:
       n = 2*a*K1 + a*K2 - a*K1*p - a*K2*p
       m = (a*K2*T6 - a*K2*p*T6)/n     

    PhasePSSAP=np.array(180/(np.pi)*( -np.arctan2(T1*w,1) -np.arctan2(T2*w,1)\
                +np.pi/2.0 -np.arctan2(T3*w,1) + np.pi/2.0-np.arctan2(T4*w,1)\
                +np.pi/2.0 -np.arctan2(T5*w,1) + np.arctan2(m*w,1)-np.arctan2(T6*w,1)  ))  

    PhaseSUM=PhasePSSAP+PhaseAVR
    
    
    fig=plt.figure()
    
    ax=fig.add_axes([0,0,1.1,1.3]) #[左，下，宽，高]
    
    f=np.linspace(0.1,2,num=20) #用f来做横坐标
    line1,line2,line3=ax.plot(f,PhaseSUM,f,PhaseAVR,f,PhasePSSAP)
    fig.legend((line1,line2,line3),('PhaseSUM','PhaseAVR','PhasePSSAP'),5)

    plt.xlabel("f /Hz")
    plt.ylabel("phase /degree")
    plt.ylim([-160,160])
    plt.show()
    
    return PhasePSSAP,PhaseSUM,m,n

#主函数部分用于初始化参数，形成全局变量
T1=0.02
T2=0.02
T3=999
T4=999
T5=4.22
T6=2.15
K=1
K1=6.77
K2=0.5
a=0.5
p=0.1
PhaseAVR=np.array([-8,-15,-22,-32,-41,-48,-52,-57,-62,-66,\
                      -68,-72,-73,-75,-78,-80,-83,-84,-86,-89])
    
#x包含T1、T2、T3、T4； 并考察T5,T6,K1,K2,a,p      
#lb=np.array([0.0199,0.0199,4.2199,4.2199,4.2199,2.1499,0.999,6.76,0.499,0.49,0.05])
#ub=np.array([0.0201,0.0201,4.2201,4.2201,4.2201,2.1501,1.001,6.78,5.001,0.51,2.0001])
#不含T1、T2、T3、T4； 仅考察T5,T6,K1,K2,a,p  
lb=np.array([3,2,0.1,0.1,0.499,0.01])
ub=np.array([8,5,10 ,5  ,0.501   ,2   ])

#lb=np.array([0       ,0       ,1,998,998,1 ,0.999,0.1,0.1,0.01,0.01])
#ub=np.array([0.0002  ,0.0002  ,8,1000,1000,10,1    ,10 ,5  ,5   ,2   ])

#x=np.array([T1,T2,T3,T4,T5,T6,K,K1,K2,a,p])
x=np.array([T5,T6,K1,K2,a,p])
w=2*np.pi*np.linspace(0.1,2,num=20)

counter=0
for counter in range(100):
    res = least_squares(Func_PSSAP,x,ftol=0.01 ,bounds=(lb, ub), method='trf' )
# lm方法不行，没有约束条件就会使值变负
#    res_3 = least_squares(fun_PSS2B,x0_PSS2B,ftol=0.01 , method='lm' )
    x=res.x
    counter=counter+1

PhasePSS,PhaseSUM,m,n=Func_Plot_PSSAP(x,w,PhaseAVR)

