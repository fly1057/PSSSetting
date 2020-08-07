# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 09:51:58 2018
Tj的计算
1磅=0.45kg
1英寸=0.0254m
1磅*英寸^2=0.45*0.0254^2=2.90322*10^-4

@author: ll
"""
import numpy as np
#数据初始化  J_high,   J_midlle,   J_low,   J_gen,   Sn,   nr
yiyang4=[1.30368*10**7,0,(8.92001+8.96572)*10**7,3.25765*10**7,722*10**6,3000] #益阳4号机8.908s
yongxin1=[4007 ,17783.5 ,17951.6 ,0,729*10**6,3000]#永新1号机6.808s

#yongxin1=[0 ,0 ,0 ,38000/4 ,729*10**6,3000]#永新1号机5.38+1.428
#解包
J_high,J_midlle,J_low,J_gen,Sn,nr=np.array(yongxin1)
#系数
w=2*np.pi*nr/60
lb_in2_to_kg_m2=2.90322*10**(-4)
#计算
J_all=(J_high+J_midlle+J_low+J_gen)
Tj=J_all*w**2/Sn 

print(Tj)