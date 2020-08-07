# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 08:22:56 2018
1、完成了双Y轴画图
2、实现了map函数的利用，即同一函数形式作用于一个list
3、实现了map到list，list到array的强制转化，可以方便的使用各种数据结构的优势
4、构造了求复数幅值和相位的函数，配合map使用
@author: ll
"""
import numpy as np
import matplotlib.pyplot as plt

global  Tr,T1,T2,Td0p,Kfd,Voo,Tw3,Ks2,T7,Ks1,Ts1,Ts2,Ts3,Ts4,f,s
#函数定义
def PSS_init():
    #初始化
    global  Tr,T1,T2,Td0p,Kfd,Voo,Tw3,Ks2,T7,Ks1,Ts1,Ts2,Ts3,Ts4,f,s
    Tr=0.02
    T1=1
    T2=10
    Td0p=6.5
    Kfd=0.91/3.3
    Voo=500
    Tw3=5
    Ks2=0.5
    T7=5
    Ks1=1
    Ts1=0.2
    Ts2=0.05
    Ts3=0.2
    Ts4=0.05
    f=np.arange(0.1,100,0.001)
    s=1j*2*np.pi*f
    
def complex_phase(complex):
    comlex_real=np.real(complex)
    comlex_imag=np.imag(complex)
    complex_phase=180/np.pi*np.arctan2(comlex_imag,comlex_real)
    return complex_phase

def complex_Magnitude(complex):
    return np.abs(complex)    

PSS_init()

#传递函数关系
AVR_OPEN=500*(1+s*T1)/(1+s*T2)*Kfd/(1 +Td0p*s)
AVR_CLOSE=2.5/(1+Tr*s)*1/(1+Tr*s)*1/(1+Tr*s)*AVR_OPEN/(1+AVR_OPEN*1/(1+Tr*s))

AVR_OPEN_phase=map(complex_phase,AVR_OPEN.tolist())
AVR_OPEN_phase=list(AVR_OPEN_phase)#map到list的强制转换
AVR_OPEN_phase=list(np.array(AVR_OPEN_phase))

AVR_OPEN_Magnitude=map(complex_Magnitude,AVR_OPEN.tolist())
AVR_OPEN_Magnitude=list(AVR_OPEN_Magnitude)#map到list的强制转换
AVR_OPEN_Magnitude=20*np.log10(AVR_OPEN_Magnitude)

AVR_CLOSE_phase=map(complex_phase,AVR_CLOSE.tolist())
AVR_CLOSE_phase=list(AVR_CLOSE_phase)#map到list的强制转换


                  

for index_num in np.arange(len(AVR_CLOSE_phase)):
     if np.abs(AVR_CLOSE_phase[index_num]-AVR_CLOSE_phase[index_num+1])>3.14:
         phase_reverse_num=index_num 
         break
     else :
            continue

temp_AVR_Phase=AVR_CLOSE_phase[phase_reverse_num+1:]
temp_AVR_Phase=np.array(temp_AVR_Phase)-360  
AVR_CLOSE_phase[phase_reverse_num+1:]=temp_AVR_Phase

AVR_CLOSE_phase=list(np.array(AVR_CLOSE_phase)+0)

AVR_CLOSE_Magnitude=map(complex_Magnitude,AVR_CLOSE.tolist())
AVR_CLOSE_Magnitude=list(AVR_CLOSE_Magnitude)#map到list的强制转换
AVR_CLOSE_Magnitude=20*np.log10(AVR_CLOSE_Magnitude)



#由于第二个叠加点处有一个负号，在算PSS相位的时候需要再减去180°
PSS=Tw3*s/(1+Tw3*s)*Ks2/(1+T7*s)*(-Ks1)*(1+Ts1*s)/(1+Ts2*s)*(1+Ts3*s)/(1+Ts4*s)

PSS_phase=map(complex_phase,PSS.tolist())
PSS_phase=list(PSS_phase)#map到list的强制转换
PSS_phase=list(np.array(PSS_phase)-180)

PSS_Magnitude=map(complex_Magnitude,PSS.tolist())
PSS_Magnitude=list(PSS_Magnitude)#map到list的强制转换
PSS_Magnitude=20*np.log10(PSS_Magnitude)

#画图
#AVR画图
fig1 = plt.figure()
ax11 = fig1.add_subplot(111)
ax11.plot(f, AVR_CLOSE_Magnitude)
#ax11.plot(f, AVR_OPEN_Magnitude)
ax11.set_title("AVR Frequency Response")
ax11.legend(labels=["AVR Magnitude"],loc='lower center')
ax11.set_xscale('log')
ax11.set_xlim(0.25,40)
ax11.set_xlabel('Frequency (Hz)') #xlabel 写在ax2里面不起作用
ax11.set_ylim(-63,13)
ax11.set_ylabel(' AVR Magnitude(dB)')

ax12 = ax11.twinx()  # this is the important function
ax12.plot(f, AVR_CLOSE_phase, 'r')
ax12.legend(labels=["AVR Phase"],loc='lower left')
ax12.set_xscale('log')
ax12.set_xlim(0.25,40)
ax12.set_ylim(-360,0)
ax12.set_ylabel('AVR phase(Degree)')

#PSS画图
fig2 = plt.figure()

ax21 = fig2.add_subplot(111)
ax21.plot(f, PSS_Magnitude)
ax21.set_title("PSS Frequency Response")
ax21.legend(labels=["PSS Magnitude"],loc='upper center')
ax21.set_xscale('log')
ax21.set_xlim(0.01,1)
ax21.set_xlabel('Frequency (Hz)') #xlabel 写在ax2里面不起作用 ,因为ax21时主轴，ax22是附属轴，显示要在主轴上进行
ax21.set_ylim(-25,5)
ax21.set_ylabel(' PSS Magnitude(dB)')

ax22 = ax21.twinx()  # this is the important function
ax22.plot(f, PSS_phase, 'r')
ax22.legend(labels=["PSS Phase"],loc='upper right')
ax22.set_xscale('log')
ax22.set_ylim(-360,0)
ax22.set_ylabel('PSS phase(Degree)')

plt.show()




