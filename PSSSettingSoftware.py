# -*- coding: utf-8 -*-
# 20191117 edit by lili
#
import sys
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from PyQt5 import QtWidgets
from Ui_PSSSettingSoftware import Ui_Dialog




class MyForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()  # 利用类Ui_Dialog的构造函数，新建立一个实例。新建的实例又是当前类的成员变量。
        self.ui.setupUi(self)  # 新建立的实例继承了Ui_Dialog唯一的成员函数，该成员函数的作用是形成一系列控件，
        # 然后将这些控件放在一个dialog中，但是这个函数并没有指定这个dialog，因此成员函数有一个形式参数，需要外部来指定。
        # 在这里，指定当前类的实例作为输入的形式参数dialog，因为当前类的直接父类是QDialog。总体而言，就是说利用外部函数生成的
        # 界面控件将放在当前类的实例上，因此完成了初始化，剩下需要做的就是引用控件，连接函数。
        self.ui.pushButton_AutoCalculateAndPlot.clicked.connect(
            self.AutoCalculateAndPlot)
        self.ui.pushButton_ManualCalculateAndPlot.clicked.connect(
            self.ManualCalculateAndPlot)
        self.ui.pushButton_SaveCSV.clicked.connect(self.SaveCSV)
        self.ui.pushButton_ReadCSV.clicked.connect(self.ReadCSV)
        self.ui.pushButton_Reset.clicked.connect(self.Reset)
        self.ui.Slider_PSSSettingValue.valueChanged.connect(
            self.PSSSettingValueChangedBySlider)
        self.ui.lineEdit_PSSSettingValue.editingFinished.connect(
            self.PSSSettingValueChangedByLineEdit)
        self.ui.pushButton_TjCalculate.clicked.connect(self.TjCalculate)

        # 在这里引入matplotlib的代码结构，首先建立figure，然后建立canvas，其中canvas是子类
        # 然后将canvas加入到之前在Qt designer中建立的layout中去，关键是要在设计时留一个空出来
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ui.verticalLayout.addWidget(self.canvas)

        self.Reset()
        self.show()

    def TjCalculate(self):
        try:
            print("begin TjCalculate")  # 在一个group内的radiobutton是互斥的
            self.GD2_TurbineHighPressureMass = float(
                self.ui.LineEdit_GD2_TurbineHighPressureMass.text())
            self.GD2_TurbineMiddlePressureMass = float(
                self.ui.LineEdit_GD2_TurbineMiddlePressureMass.text())
            self.GD2_TurbineLowPressureMass = float(
                self.ui.LineEdit_GD2_TurbineLowPressureMass.text())
            self.GD2_GeneratorMass = float(
                self.ui.LineEdit_GD2_GeneratorMass.text())

            self.GR2_TurbineHighPressureMass = float(
                self.ui.LineEdit_GR2_TurbineHighPressureMass.text())
            self.GR2_TurbineMiddlePressureMass = float(
                self.ui.LineEdit_GR2_TurbineMiddlePressureMass.text())
            self.GR2_TurbineLowPressureMass = float(
                self.ui.LineEdit_GR2_TurbineLowPressureMass.text())
            self.GR2_GeneratorMass = float(
                self.ui.LineEdit_GR2_GeneratorMass.text())
            self.Sn = float(self.ui.LineEdit_Sn.text())
            self.GD2 = float(self.ui.LineEdit_GD2.text())
            self.RotorSpeed = float(self.ui.LineEdit_RotorSpeed.text())

            if self.ui.radioButton_GD2.isChecked():
                self.GD2 = self.GD2_TurbineHighPressureMass + self.GD2_TurbineMiddlePressureMass + \
                    self.GD2_TurbineLowPressureMass + self.GD2_GeneratorMass
                self.Tj = self.GD2*1000/4*(2*np.pi*self.RotorSpeed/60)**2/(self.Sn*10**6)

            elif self.ui.radioButton_GR2.isChecked():
                self.GD2 = 4*(self.GR2_TurbineHighPressureMass + self.GR2_TurbineMiddlePressureMass +
                              self.GR2_TurbineLowPressureMass + self.GR2_GeneratorMass)
                self.Tj = self.GD2*1000/4*(2*np.pi*self.RotorSpeed/60)**2/(self.Sn*10**6)

            self.ui.LineEdit_GD2.setText(str(self.GD2))
            self.ui.LineEdit_Sn.setText(str(self.Sn))
            self.ui.LineEdit_Tj.setText(str(self.Tj))
            print("end TjCalculate")
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数

    def AutoCalculateAndPlot(self):
        try:
            print("hello world! AutoCalculateAndPlot")

            self.ManualCalculateAndPlot()  # 需要及时更新LineEdit的变化，可以通过手动计算先进行更新
            if self.ui.radioButton_PSS1.isChecked():
                pass
            elif self.ui.radioButton_PSS2A.isChecked():
                # 进行计算前的初始化条件
                lb = np.array([0.01, 0.01, 0.01, 0.01])
                ub = np.array([2.0, 2.0, 2.0, 2.0])
                x0 = [0.1, 0.1, 0.1, 0.1]
                for counter in range(10):
                    self.res = least_squares(self.residuals_PSS2A, x0, ftol=0.001,
                                             bounds=(lb, ub), method='trf')
                    x0 = self.res.x
                    counter = counter + 1
                self.T1, self.T2, self.T3, self.T4 = self.res.x
                self.T5 = 0
                self.T6 = 0
                print("PSS2A cost=", self.res.cost)
                print(self.res.x)

            elif self.ui.radioButton_PSS2B.isChecked():
                lb = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
                ub = np.array([2.0, 2.0, 2.0, 2.0, 2.0, 2.0])
                x0 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
                for counter in range(10):
                    self.res = least_squares(
                        self.residuals_PSS2B, x0, ftol=0.001, bounds=(lb, ub), method='trf')
                    x0 = self.res.x
                    counter = counter + 1
                self.T1, self.T2, self.T3, self.T4, self.T5, self.T6 = self.res.x
                print("PSS2B cost=", self.res.cost)
                print(self.res.x)
            self.SUM = self.AVR_phase + self.PSS_phase  # 调用残差函数计算时并没有计算SUM，在这里要加上
            self.Ks2 = self.T7/self.Tj
            self.AMP = self.Ks1 * np.abs(1j*self.TW3*self.ws)/np.abs(1+1j*self.TW3*self.ws) \
                * np.abs(self.Ks2)/np.abs(1+1j*self.T7*self.ws)\
                * np.abs(1+1j*self.T1*self.ws)/np.abs(1+1j*self.T2*self.ws)\
                * np.abs(1+1j*self.T3*self.ws)/np.abs(1+1j*self.T4*self.ws)\
                * np.abs(1+1j*self.T5*self.ws)/np.abs(1+1j*self.T6*self.ws)

            self.UpdateDataFrameFromSelf()
            self.UpdateTableWidgetFromDataFrame()
            self.UpdateLineEditFromDataFrame()
            self.Plot()

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数

    def ManualCalculateAndPlot(self):
        try:
            print("hello world! ManualCalculateAndPlot")
            self.UpdateDataFrameFromTableWidget()  # 先从tableWidget更新相位。
            self.UpdateDataFrameFromLineEdit()  # 然后从lineedit更新参数。  两者不要搞反了。
            self.UpdateSelfFromDataFrame()
            if self.ui.radioButton_PSS1.isChecked():
                pass
            elif self.ui.radioButton_PSS2A.isChecked():
                self.PSS_phase = np.array(
                    180 / np.pi * ((np.pi / 2.0 - np.arctan(self.TW3 * self.ws)) - np.arctan(self.T7 * self.ws)
                                   + np.arctan(self.T1 * self.ws) -
                                   np.arctan(self.T2 * self.ws)
                                   + np.arctan(self.T3 * self.ws) -
                                   np.arctan(self.T4 * self.ws)
                                   ))
            elif self.ui.radioButton_PSS2B.isChecked():
                self.PSS_phase = np.array(
                    180 / np.pi * ((np.pi / 2.0 - np.arctan(self.TW3 * self.ws)) - np.arctan(self.T7 * self.ws)
                                   + np.arctan(self.T1 * self.ws) -
                                   np.arctan(self.T2 * self.ws)
                                   + np.arctan(self.T3 * self.ws) -
                                   np.arctan(self.T4 * self.ws)
                                   + np.arctan(self.T5 * self.ws) -
                                   np.arctan(self.T6 * self.ws)
                                   ))
            self.SUM = self.AVR_phase + self.PSS_phase
            self.AMP = self.Ks1*np.abs(1j*self.TW3*self.ws)/np.abs(1+1j*self.TW3*self.ws) \
                * np.abs(self.Ks2)/np.abs(1+1j*self.T7*self.ws)\
                * np.abs(1+1j*self.T1*self.ws)/np.abs(1+1j*self.T2*self.ws)\
                * np.abs(1+1j*self.T3*self.ws)/np.abs(1+1j*self.T4*self.ws)\
                * np.abs(1+1j*self.T5*self.ws)/np.abs(1+1j*self.T6*self.ws)

            self.Plot()  # 角度在Plot函数中进行了更新，可以利用一下，然后再调用更新dataframe,tableWidget
            self.UpdateDataFrameFromSelf()
            self.UpdateTableWidgetFromDataFrame()
            self.UpdateLineEditFromDataFrame()

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数

    def SaveCSV(self):
        print("hello world! SaveCSV")
        try:
            for i in np.arange(self.df.shape[0]):
                for j in np.arange(self.df.shape[1]):
                    self.df.iloc[i, j] = self.ui.tableWidget.item(i, j).text()
            savefile_name = QtWidgets.QFileDialog.getSaveFileName(
                self, '选择文件', '', '(*.csv ; *.xlsx ; *.xls )')
            self.df.to_csv(savefile_name[0], index=None)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数

    def ReadCSV(self):
        try:
            print("hello world! ReadCSV")
            # openfile_name = [
            #     'C:/Users/ll/Desktop/PSSData.csv', 1]
            openfile_name = QtWidgets.QFileDialog.getOpenFileName(
                self, '选择文件', '', '(*.csv ; *.xlsx ; *.xls )')
            # openfile_name是元组，第一个元素是路径
            if openfile_name[0] == '':
                QtWidgets.QMessageBox.information(
                    self, "读取CSV", "已经放弃打开文件", QtWidgets.QMessageBox.Yes)
            else:
                self.df = pd.read_csv(openfile_name[0])
                self.GUIShow()

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数

    def Plot(self):
        try:
            print("hello world! Plot")
            # 连接的绘制的方法
            # left, bottom, width, height
            plt.clf()
            ax = self.figure.add_axes([0.15, 0.15, 0.80, 0.7])
            ax.plot(self.f, self.AVR_phase, '^-', label='AVR')
            ax.plot(self.f, self.PSS_phase, 'x-', label='PSS')
            ax.plot(self.f, self.SUM, 'o-', label='SUM')
            ax.legend(loc='best', shadow=False, fontsize='medium')
            ax.spines['top'].set_visible(False)  # 去掉上边框
            ax.spines['right'].set_visible(False)  # 去掉右边框
            ax.set_xlabel("f/Hz")
            ax.set_ylabel("phase/degree")
            ax.set_title("Phase - Frequency Character")
            ax.grid()

            self.canvas.draw()
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数

    def Reset(self):
        print("hello world!  Reset")
        data = {"f": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                      1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
                "AVR": [-30, -46, -64, -72, -76, -82, -82, -90, -90, -93,
                        -104, -100, -104, -110, -150, -123, -118, -117, -118, -119],
                "PSS": [-39.00701069, -41.43214653, -34.09457874, -25.55293746, -17.56146285, -10.56449506, -4.613846295, 0.369788613, 4.503697913, 7.90762991,
                        10.6907853, 12.94805649, 14.76003574, 16.19443646, 17.30790747, 18.14781316, 18.7538188, 19.15923904, 19.39215788, 19.47634723],
                "SUM": [-69.00701069, -87.43214653, -98.09457874, -97.55293746, -93.56146285, -92.56449506, -86.6138463, -89.63021139, -85.49630209, -85.09237009,
                        -93.3092147, -87.05194351, -89.23996426, -93.80556354, -132.6920925, -104.8521868, -99.2461812, -97.84076096, -98.60784212, -99.52365277],
                "AMP": [0.211524583, 0.121699253, 0.091243276, 0.078071436, 0.072016367, 0.06952978, 0.069067026, 0.069850578, 0.07144586, 0.073589729,
                        0.076112424, 0.078898689, 0.081866935, 0.084957394, 0.088125034, 0.091335126, 0.094560382, 0.09777903, 0.100973496, 0.10412947],
                "ParaName": ['PSSSet', 'Ks1', 'Ks2', 'Ks3', 'Tw1', 'Tw2', 'Tw3', 'Tw4', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'M', 'N', 'Tj'],
                "ParaValue": [-90, 1, 0.714285714, 1, 5, 5, 5, 0, 0.19, 0.02, 0.3, 0.03, 0, 0, 5, 0.6, 0.12, 5, 1, 7]
                }
        self.df = pd.DataFrame(data)
        self.ui.LineEdit_GD2_GeneratorMass.setText("189.2")
        self.ui.LineEdit_GR2_GeneratorMass.setText("47.3")
        self.ui.LineEdit_Sn.setText("667")
        self.ui.LineEdit_RotorSpeed.setText("3000")
        self.ui.LineEdit_GD2.setText("189.2")
        self.GUIShow()

    def PSSSettingValueChangedBySlider(self):
        print("hello world!  PSSSettingValueChangedBySlider")
        # 设生成了一个类成员函数self.PSSSettingValue
        self.PSSSettingValue = self.ui.Slider_PSSSettingValue.value()
        self.ui.lineEdit_PSSSettingValue.setText(str(self.PSSSettingValue))
        self.UpdateDataFrameFromSelf()
        print(self.PSSSettingValue)

    def PSSSettingValueChangedByLineEdit(self):
        print("hello world!  PSSSettingValueChangedByLineEdit")
        if self.ui.lineEdit_PSSSettingValue.text() in ["-", "", "+"]:
            pass
        else:
            self.PSSSettingValue = float(
                self.ui.lineEdit_PSSSettingValue.text())
            if self.PSSSettingValue >= -60:
                self.PSSSettingValue = -60
            elif self.PSSSettingValue <= -130:
                self.PSSSettingValue = -130
            self.ui.Slider_PSSSettingValue.setValue(self.PSSSettingValue)
            self.UpdateDataFrameFromSelf()
            print(self.PSSSettingValue)

    def residuals_PSS2A(self, p):
        self.T1, self.T2, self.T3, self.T4 = p
        self.PSS_phase = np.array(
            180 / np.pi * ((np.pi / 2.0 - np.arctan(self.TW3 * self.ws)) - np.arctan(self.T7 * self.ws)
                           + np.arctan(self.T1 * self.ws) -
                           np.arctan(self.T2 * self.ws)
                           + np.arctan(self.T3 * self.ws) -
                           np.arctan(self.T4 * self.ws)
                           ))

        return self.PSSSettingValue - self.AVR_phase - self.PSS_phase  # 标幺化后进行的计算，否则误差会很大

    def residuals_PSS2B(self, p):
        self.T1, self.T2, self.T3, self.T4, self.T5, self.T6 = p
        self.PSS_phase = np.array(
            180 / np.pi * ((np.pi / 2.0 - np.arctan(self.TW3 * self.ws)) - np.arctan(self.T7 * self.ws)
                           + np.arctan(self.T1 * self.ws) -
                           np.arctan(self.T2 * self.ws)
                           + np.arctan(self.T3 * self.ws) -
                           np.arctan(self.T4 * self.ws)
                           + np.arctan(self.T5 * self.ws) -
                           np.arctan(self.T6 * self.ws)
                           ))

        return self.PSSSettingValue - self.AVR_phase - self.PSS_phase  # 标幺化后进行的计算，否则误差会很大

    def UpdateDataFrameFromSelf(self):
        print("begin UpdateDataFrameFromSelf")
        self.df["f"] = self.f
        self.df["AVR"] = self.AVR_phase
        self.df["PSS"] = self.PSS_phase
        self.df["SUM"] = self.SUM
        self.df["AMP"] = self.AMP

        self.df["ParaValue"] = np.array([self.PSSSettingValue, self.Ks1, self.Ks2, self.Ks3,
                                         self.TW1, self.TW2, self.TW3, self.TW4,
                                         self.T1, self.T2, self.T3, self.T4, self.T5, self.T6, self.T7, self.T8,
                                         self.T9,
                                         self.M, self.N, self.Tj])
        print("end UpdateDataFrameFromSelf")

    def UpdateSelfFromDataFrame(self):
        print("begin UpdateSelfFromDataFrame")

        self.f = pd.to_numeric(self.df["f"], errors='ignore')
        self.AVR_phase = pd.to_numeric(self.df["AVR"], errors='ignore')
        self.PSS_phase = pd.to_numeric(self.df["PSS"], errors='ignore')
        self.SUM = pd.to_numeric(self.df["SUM"], errors='ignore')
        self.AMP = pd.to_numeric(self.df["AMP"], errors='ignore')

        self.PSSSettingValue, self.Ks1, self.Ks2, self.Ks3, \
            self.TW1, self.TW2, self.TW3, self.TW4, \
            self.T1, self.T2, self.T3, self.T4, self.T5, self.T6, self.T7, self.T8, self.T9, \
            self.M, self.N, self.Tj = pd.to_numeric(
                self.df["ParaValue"], errors='ignore')  # list可以依次赋值
        print("end UpdateSelfFromDataFrame")

    def UpdateTableWidgetFromDataFrame(self):
        print("begin UpdateTableWidgetFromDataFrame")
        for i in np.arange(self.df.shape[0]):
            for j in np.arange(self.df.shape[1]):
                self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(
                    str(self.df.iloc[i, j])))  # 这里必须采用str强制转换
        print("end UpdateTableWidgetFromDataFrame")

    def UpdateLineEditFromDataFrame(self):
        print("begin UpdateLineEditFromDataFrame")
        self.ui.lineEdit_PSSSettingValue.setText(str(self.df.iloc[0, 6]))
        self.ui.LineEdit_Ks1.setText(str(self.df.iloc[1, 6]))
        self.ui.LineEdit_Ks2.setText(str(self.df.iloc[2, 6]))
        self.ui.LineEdit_Ks3.setText(str(self.df.iloc[3, 6]))
        self.ui.LineEdit_TW1.setText(str(self.df.iloc[4, 6]))
        self.ui.LineEdit_TW2.setText(str(self.df.iloc[5, 6]))
        self.ui.LineEdit_TW3.setText(str(self.df.iloc[6, 6]))
        self.ui.LineEdit_TW4.setText(str(self.df.iloc[7, 6]))
        self.ui.LineEdit_T1.setText(str(self.df.iloc[8, 6]))
        self.ui.LineEdit_T2.setText(str(self.df.iloc[9, 6]))
        self.ui.LineEdit_T3.setText(str(self.df.iloc[10, 6]))
        self.ui.LineEdit_T4.setText(str(self.df.iloc[11, 6]))
        self.ui.LineEdit_T5.setText(str(self.df.iloc[12, 6]))
        self.ui.LineEdit_T6.setText(str(self.df.iloc[13, 6]))
        self.ui.LineEdit_T7.setText(str(self.df.iloc[14, 6]))
        self.ui.LineEdit_T8.setText(str(self.df.iloc[15, 6]))
        self.ui.LineEdit_T9.setText(str(self.df.iloc[16, 6]))
        self.ui.LineEdit_M.setText(str(self.df.iloc[17, 6]))
        self.ui.LineEdit_N.setText(str(self.df.iloc[18, 6]))
        self.ui.LineEdit_Tj.setText(str(self.df.iloc[19, 6]))
        print("end UpdateLineEditFromDataFrame")

    def UpdateDataFrameFromLineEdit(self):
        print("begin UpdateDataFrameFromLineEdit")
        self.df.iloc[0, 6] = float(self.ui.lineEdit_PSSSettingValue.text())
        self.df.iloc[1, 6] = str(self.ui.LineEdit_Ks1.text())
        self.df.iloc[2, 6] = str(self.ui.LineEdit_Ks2.text())
        self.df.iloc[3, 6] = str(self.ui.LineEdit_Ks3.text())
        self.df.iloc[4, 6] = str(self.ui.LineEdit_TW1.text())
        self.df.iloc[5, 6] = str(self.ui.LineEdit_TW2.text())
        self.df.iloc[6, 6] = str(self.ui.LineEdit_TW3.text())
        self.df.iloc[7, 6] = str(self.ui.LineEdit_TW4.text())
        self.df.iloc[8, 6] = str(self.ui.LineEdit_T1.text())
        self.df.iloc[9, 6] = str(self.ui.LineEdit_T2.text())
        self.df.iloc[10, 6] = str(self.ui.LineEdit_T3.text())
        self.df.iloc[11, 6] = str(self.ui.LineEdit_T4.text())
        self.df.iloc[12, 6] = str(self.ui.LineEdit_T5.text())
        self.df.iloc[13, 6] = str(self.ui.LineEdit_T6.text())
        self.df.iloc[14, 6] = str(self.ui.LineEdit_T7.text())
        self.df.iloc[15, 6] = str(self.ui.LineEdit_T8.text())
        self.df.iloc[16, 6] = str(self.ui.LineEdit_T9.text())
        self.df.iloc[17, 6] = str(self.ui.LineEdit_M.text())
        self.df.iloc[18, 6] = str(self.ui.LineEdit_N.text())
        self.df.iloc[19, 6] = str(self.ui.LineEdit_Tj.text())
        print("end UpdateDataFrameFromLineEdit")

    def UpdateDataFrameFromTableWidget(self):
        print("begin UpdateDataFrameFromTableWidget")
        for i in np.arange(self.df.shape[0]):
            self.df.iloc[i, 1] = float(
                self.ui.tableWidget.item(i, 1).text())  # 这里必须采用str强制转换
        print("end UpdateDataFrameFromTableWidget")

    def GUIShow(self):
        # 读取后及时更新TableWidget和LineEdit和self
        self.UpdateSelfFromDataFrame()
        self.UpdateTableWidgetFromDataFrame()
        self.UpdateLineEditFromDataFrame()
        self.ws = 2 * np.pi * np.linspace(0.1, 2, num=20)

        # 设定radiobutton
        if np.abs(self.T7) <= 0.00001:
            self.ui.radioButton_PSS1.setChecked(True)
            self.ui.radioButton_PSS2A.setChecked(False)
            self.ui.radioButton_PSS2B.setChecked(False)
        elif np.abs(self.T5 * self.T6) <= 0.00001:
            self.ui.radioButton_PSS1.setChecked(False)
            self.ui.radioButton_PSS2A.setChecked(True)
            self.ui.radioButton_PSS2B.setChecked(False)
        else:
            self.ui.radioButton_PSS1.setChecked(False)
            self.ui.radioButton_PSS2A.setChecked(False)
            self.ui.radioButton_PSS2B.setChecked(True)
        self.Plot()
        print(self.df)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MyForm()
    sys.exit(app.exec_())
