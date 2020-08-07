# -*- coding: utf-8 -*-
"""
The program is used for PSS phase parameters tunning in HMF plant. 
Last edited by lili on 21-6-2017
"""
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt


#用于初始化参数
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
    p=0.363
    w0=2*np.pi*np.linspace(0.1,2,num=20)
    x0=np.array([T1,T2,T3,T4,T5,T6,K,K1,K2,a,p])
    
    lb=np.array([0.0199,0.0199,4.219,4.219,4.219,2.149,0.999,6.769,0.49,0.69,0.01])
    ub=np.array([0.0201,0.0201,4.221,4.221,4.221,2.151,1.001,6.771,0.51,1.91,2   ])
    bounds=(lb, ub)
     
    #HMF1
#    Phase_AVR=np.array([-20,-22,-27,-32,-36,-37,-41,-42,-45,-49,\
#                       -54,-60,-73,-80,-93,-101,-79,-76,-70,-63])    
    #HMF2
#    PhaseAVR=np.array([-20,-25,-29,-33,-36,-41,-42,-45,-46,-49,\
#                       -54,-56,-67,-78,-87,-95,-81,-74,-69,-68]) 
    #HMF3
#    PhaseAVR=np.array([-20,-25,-29,-32,-36,-39,-42,-43,-46,-49,\
#                       -55,-59,-66,-74,-89,-95,-85,-73,-68,-71])   
    #HMF4
    PhaseAVR=np.array([-20,-23,-27,-30,-34,-37,-40,-45,-50,-53,\
                       -57,-60,-65,-77,-87,-97,-84,-74,-70,-67])     
    
    return x0,w0,PhaseAVR,bounds



#单纯用于计算PSSAP相位
def Func_Phase_PSSAP(x):
    
    T1,T2,T3,T4,T5,T6,K,K1,K2,a,p=x
    w=2*np.pi*np.linspace(0.1,2,num=20)
    print (p)
   
    if    p>0 and p<1:
        n = a*K2 + a*K1*p - a*K2*p
        m = (a*K2*T6 - a*K2*p*T6)/n   
       
    elif  p>1 and p<2:
        n = 2*a*K1 + a*K2 - a*K1*p - a*K2*p
        m = (a*K2*T6 - a*K2*p*T6)/n           
    
    PhasePSSAP=np.array( 180/(np.pi)*( -np.arctan(T1*w) -np.arctan(T2*w)\
            +np.pi/2.0 -np.arctan(T3*w) + np.pi/2.0-np.arctan(T4*w)\
            +np.pi/2.0 -np.arctan(T5*w) + np.arctan(m*w)-np.arctan(T6*w)  ))          
   
    return  PhasePSSAP 

#用于计算PSSAP函数的拟合角度与需要的补偿的角度的差，值得诟病的是为了契合least_square
#函数计算，Func_delta_angle函数只能接受一个参数，因此导致，AVR相位必须提前传入
#导致参数与功能不能分离
    
def Func_delta_angle(x):
    T1,T2,T3,T4,T5,T6,K,K1,K2,a,p=x
    w=2*np.pi*np.linspace(0.1,2,num=20)
    #HMF1
#    Phase_AVR=np.array([-20,-22,-27,-32,-36,-37,-41,-42,-45,-49,\
#                       -54,-60,-73,-80,-93,-101,-79,-76,-70,-63])    
    #HMF2
#    PhaseAVR=np.array([-20,-25,-29,-33,-36,-41,-42,-45,-46,-49,\
#                       -54,-56,-67,-78,-87,-95,-81,-74,-69,-68]) 
    #HMF3
#    PhaseAVR=np.array([-20,-25,-29,-32,-36,-39,-42,-43,-46,-49,\
#                       -55,-59,-66,-74,-89,-95,-85,-73,-68,-71])     
    #HMF4
    PhaseAVR=np.array([-20,-23,-27,-30,-34,-37,-40,-45,-50,-53,\
                       -57,-60,-65,-77,-87,-97,-84,-74,-70,-67])     
    
    print (p)  #用于跟踪显示p的变化
    
   
    if    p>0 and p<1:
        n = a*K2 + a*K1*p - a*K2*p
        m = (a*K2*T6 - a*K2*p*T6)/n   
       
    elif  p>1 and p<2:
        n = 2*a*K1 + a*K2 - a*K1*p - a*K2*p
        m = (a*K2*T6 - a*K2*p*T6)/n           
    
    PhasePSSAP=np.array( 180/(np.pi)*( -np.arctan(T1*w) -np.arctan(T2*w)\
            +np.pi/2.0 -np.arctan(T3*w) + np.pi/2.0-np.arctan(T4*w)\
            +np.pi/2.0 -np.arctan(T5*w) + np.arctan(m*w)-np.arctan(T6*w)  ))          
   
    return  PhasePSSAP+PhaseAVR+90 
    

#用于画图
def Func_Plot_PSSAP(w,PhasePSSAP,PhaseAVR):

    PhaseSUM=PhasePSSAP+PhaseAVR
    
    plt.plot(np.linspace(0.1,2,num=20),PhaseSUM,linestyle='-.')
    plt.plot(np.linspace(0.1,2,num=20),PhaseAVR,linestyle='-')
    plt.plot(np.linspace(0.1,2,num=20),PhasePSSAP,linestyle=':')
    plt.legend(['AVR+PSS','AVR','PSS'])
    
    plt.grid()
    plt.xlabel("f /Hz")
    plt.ylabel("phase /degree")
    plt.ylim([-150,10])
    
    return PhaseSUM



#####################################################################主体函数
#初始化参数，用于后续计算
x0,w,PhaseAVR,bounds=Func_Initial_PSSAP()                                       
lb, ub=bounds                     

#调用最小二乘函数，使用trf算法，cost function torlerance 是1e-6，因此会导致多次迭代
#那么就没有必要使用for函数来多次调用least_squares
res = least_squares(Func_delta_angle,x0,ftol=1e-4 ,bounds=(lb, ub), method='trf' )
x=res.x
    
#用自定义参数画图
PhasePSSAP_orignal=Func_Phase_PSSAP(x0)
PhaseSUM=Func_Plot_PSSAP(w,PhasePSSAP_orignal,PhaseAVR)

#用算法计算参数画图
#PhasePSSAP=Func_Phase_PSSAP(x)    
#PhaseSUM=Func_Plot_PSSAP(w,PhasePSSAP,PhaseAVR)



