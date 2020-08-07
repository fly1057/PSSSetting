# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 21:47:04 2017

@author: ll
"""
from os import path
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

###############################################################################
#初始化
#路径名处理
path_str=u"C:/Users/ll/Desktop/ddj1_PSS2B.csv"
dir_filename,filetype=path.splitext(path_str) 

df=pd.read_csv(path_str,encoding="gb2312")
AVR_phase=df.AVR
PSS_phase=df.PSS
M=df.M.dropna().max()
N=df.N.dropna().max()
T1,T2,T3,T4,T5,T6,T7,T8,T9=df.Ts.dropna()
Ks1,Ks2,Ks3=df.Ks.dropna()
Tw1,Tw2,Tw3,Tw4=df.Tw.dropna()
Tj=df.Tj.dropna().max()
ws=2*np.pi*np.linspace(0.1,2,num=20)
T7=5.0
Ks2=T7/Tj

###############################################################################
#计算相频参数

#相频函数残差
def  residuals_PSS_T(p):
    T1,T2,T3,T4=p
    PSS_phase=np.array(180/(np.pi)*(( np.pi/2.0-np.arctan(Tw3*ws) )-np.arctan(T7*ws)\
                    +np.arctan(T1*ws)-np.arctan(T2*ws)\
                    +np.arctan(T3*ws)-np.arctan(T4*ws) ))

    return  -90.0-AVR_phase-PSS_phase  #标幺化后进行的计算，否则误差会很大

#进行计算前的初始化条件
lb=np.array([0.01,0.01,0.01,0.01])
ub=np.array([2.0,2.0,2.0,2.0])
x0=[0.1,0.1,0.1,0.1]
counter=0

for counter in range(5):
    res=least_squares(residuals_PSS_T ,x0,ftol=0.001 ,bounds=(lb, ub), method='trf' )
    x0=res.x
    counter=counter+1

T1,T2,T3,T4=res.x
print "cost=",res.cost

###############################################################################
#回存到CSV里面

PSS_phase=np.array(180/(np.pi)*(( np.pi/2.0-np.arctan(Tw3*ws) )-np.arctan(T7*ws)\
                    +np.arctan(T1*ws)-np.arctan(T2*ws)\
                    +np.arctan(T3*ws)-np.arctan(T4*ws) ))
AVR_PSS_phase=AVR_phase+PSS_phase

#幅值算的有点不对，不知道原因是什么
PSS_amplify1=np.exp(\
    np.log(Tw3*ws)-np.log(1+Tw3*ws) \
    +np.log(Ks2)-np.log(1+T7*ws)\
    +np.log(1+T1*ws)-np.log(1+T2*ws)\
    +np.log(1+T3*ws)-np.log(1+T4*ws))

#PSS_amplify2=np.abs(Tw3*ws)/np.abs(1+Tw3*ws) \
#    *np.abs(Ks2)/np.abs(1+T7*ws)\
#    *np.abs(1+T1*ws)/np.abs(1+T2*ws)\
#    *np.abs(1+T3*ws)/np.abs(1+T4*ws)


df.PSS_Gain=PSS_amplify1
df.Ks[0:3]=Ks1,Ks2,Ks3
df.Ts[0:9]= T1,T2,T3,T4,T5,T6,T7,T8,T9
df.PSS=PSS_phase
df.AVR_PSS=AVR_PSS_phase
df.to_csv(path_str,index=None)#保存时去掉索引，否则csv会越来越大

###############################################################################
#画图，保存图片

#设定图像大小，像素，去除边框
plt.figure(figsize=(7,4), dpi=80)
ax = plt.gca()
ax.spines['top'].set_visible(False)  #去掉上边框
ax.spines['right'].set_visible(False) #去掉右边框

plt.plot(np.linspace(0.1,2,num=20),AVR_PSS_phase,\
         np.linspace(0.1,2,num=20),AVR_phase,\
         np.linspace(0.1,2,num=20),PSS_phase )

#legend
plt.legend(['AVR_PSS_phase','AVR_phase','PSS_phase'])

#plt.grid()
plt.xlabel("f /Hz")
plt.ylabel("phase /degree")
plt.ylim([-150,40])
plt.savefig(dir_filename+u'_相频图.jpg',format='jpg') 





