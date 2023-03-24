import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QApplication, QGroupBox, QFileDialog, QPushButton, QLabel, QTabWidget, QMessageBox
from PyQt5.QtGui import QFont
from typing import Optional, Callable
from app.ifg import Interferogram
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from app.database import Cache
import os

class Canvas(QWidget):
    def __init__(self, parent: Optional[QWidget]=None) -> None:
        super().__init__(parent)
        # self.setGeometry(250,180,500,600)
        # self.resize(300, 300)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = plt.figure(dpi=750)
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)
        
        # self.axes = figure.add_subplot()
        # self.axes.axis('off')

        # self.plot()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        

    def plot(self, plotter:Callable) -> None:
    #     ''' plot some random stuff '''
        
        # self.axes.axis('off')
        # # self.axes.axis('on')
        # # self.axes.set_xticks([])
        # # self.axes.set_yticks([])
        plotter()
        # # self.postplot()
        # self.axes.set_xlim([0, 224])
        # self.axes.set_ylim([0, 224])
        
        self.canvas.draw()
        plt.clf()
        
    
    
    # def postplot(self,):
    #     return

class DataWidget(QWidget):
    def __init__(self, parent: Optional['QWidget']=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Models')
        self.resize(700, 100)


        layout = QVBoxLayout()
        self.setLayout(layout)
            
        self.tabs = QTabWidget()
        self.synth = ModelWidget()
        self.real = ModelWidget()
        
        self.tabs.addTab(self.synth, 'Synthetic')
        self.tabs.addTab(self.real, 'Real')
        self.tabs.currentChanged.connect(self.onChange)
        layout.addWidget(self.tabs)
        self.CheckSynth()

        self.synth.vit.clicked.connect(self.onClickSynth)
        self.synth.resnet.clicked.connect(self.onClickSynth)
        
        self.real.vit.clicked.connect(self.onClickReal)
        self.real.resnet.clicked.connect(self.onClickReal)
        

    def onChange(self, i):
            if i==0:
                self.CheckSynth()
            elif i == 1:
                self.CheckReal()
    
    def CheckSynth(self,):
        self.synth.resnet.setChecked(True)
        modelDir='../models/synthetic/ResVolcNet_2023_01_24_13_58_24.h5'
        Cache().set(modelDir=modelDir)
        
    def CheckReal(self,):
        self.real.resnet.setChecked(True)
        modelDir='../models/real/ResVolcNet_2023_02_07_16_05_27.h5'
        Cache().set(modelDir=modelDir)

    def onClickSynth(self,):
        if self.synth.resnet.isChecked():
            modelDir='../models/synthetic/ResVolcNet_2023_01_24_13_58_24.h5'

        elif self.synth.vit.isChecked():
            modelDir='../models/synthetic/VitVolcNet_2023_02_16_14_31_35.pth'
        
        Cache().set(modelDir=modelDir)

    def onClickReal(self,):
        if self.real.resnet.isChecked():
            modelDir='../models/real/ResVolcNet_2023_02_07_16_05_27.h5'
        
        elif self.real.vit.isChecked():
            modelDir='../models/real/VitVolcNet_2023_02_17_06_52_58.pth'

        Cache().set(modelDir=modelDir)
    
        

class ModelWidget(QWidget):
    def __init__(self, parent: Optional['QWidget']=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Models')
        self.resize(700, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.resnet = QRadioButton('ResNet')
        # self.resnet.setChecked(True)
        # self.resnet.toggled.connect(self.onClicked)
        
        self.vit = QRadioButton("ViT")
        # self.vit.toggled.connect(self.onClicked)
        
        groupbox = QGroupBox('Models')
        groupboxLayout = QHBoxLayout()
        groupboxLayout.addWidget(self.resnet)
        groupboxLayout.addWidget(self.vit)
        groupbox.setLayout(groupboxLayout)
        layout.addWidget(groupbox)
        

        # self.resnet.toggled.connect(lambda:self.btnstate(self.resnet))
        # self.vit.toggled.connect(lambda:self.btnstate(self.vit))

    # def onClicked(self):
    #     if self.resnet.isChecked():
    #         self.vit.setChecked(False)
    #         modelDir = './Application/Models/Synthetic/VolNet_2023_01_24_13_58_24.h5'
            
    #     elif self.vit.isChecked():
    #         self.resnet.setChecked(False)
    #         modelDir = ''
    #     print(modelDir)
        
    #     Cache().set(modelDir=modelDir)

        
    # def btnstate(self, btn:QRadioButton):
    #     if btn.text() == "ResNet":
    #         if btn.isChecked():
    #             print(f'{btn.text()} is selected')
    #         else:
    #             print(f'{btn.text()} is deselected')
                    
    #     if btn.text() == "ViT":
    #         if btn.isChecked():
    #             print(f'{btn.text()} is selected')
    #         else:
                # print(f'{btn.text()} is deselected')

class ImageWidget(QWidget):
    def __init__(self, parent: Optional['QWidget']=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Models')
        self.resize(700, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button = QPushButton('Select File')
        self.button.clicked.connect(self.onClicked)

        self.canvas = Canvas()
        
        groupbox = QGroupBox('Interferogram')
        groupboxLayout = QHBoxLayout()
        groupboxLayout.addWidget(self.button)
        groupboxLayout.addWidget(self.canvas)
        groupbox.setLayout(groupboxLayout)
        layout.addWidget(groupbox)
    
    def onClicked(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Choose File', './Application/Data', 'pkl files (*.pkl)',)
       
        if fileName:
            
            # print(fileName)
            ifg = Interferogram(fileName)
            # self.canvas.postplot = lambda:ifg.plot(self.canvas.axes)
            self.canvas.plot(lambda:ifg.plot(self.canvas.figure))
            Cache().set(fileName=fileName)
            
           


class ProcessWidget(QWidget):
    def __init__(self, parent: Optional['QWidget']=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Models')
        self.resize(700, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button = QPushButton('Process')
        self.button.clicked.connect(self.onClicked)

        predict = QVBoxLayout()
        self.label = QLabel()
        self.label.setText('')
        self.label.setFont(QFont('Times', 12))
        self.canvas = Canvas()

        predict.addWidget(self.label)
        predict.addWidget(self.canvas)

        groupbox = QGroupBox('Processing')
        groupboxLayout = QHBoxLayout()
        groupboxLayout.addWidget(self.button)
        groupboxLayout.addLayout(predict)
        groupbox.setLayout(groupboxLayout)
        layout.addWidget(groupbox)
    
    def onClicked(self):
        
        # print(Cache().data)
        try:
            ifg = Interferogram(**Cache().data)
            label, accurcy = ifg.labelling()
            # print(label)
            # print(accurcy)
            self.label.setText(f'label: {label}, acc: {accurcy*100:0.0f}%')
            self.canvas.plot(lambda:ifg.plot(self.canvas.figure, True))
        except:
            self.popupmsg()

    def popupmsg(self,):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
    
        # setting message for Message Box
        msg.setText("You must select an interferogram file")
        
        # setting Message box window title
        msg.setWindowTitle("Warning")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)
        
        # start the app
        retval = msg.exec_()

        

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = DataWidget()
   ex.show()
   sys.exit(app.exec_())


