import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from typing import Optional
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout

class Canvas(QWidget):
    def __init__(self, parent: Optional[QWidget]=None) -> None:
        super().__init__(parent)
        # self.setGeometry(250,180,500,600)
        # self.resize(300, 300)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        figure = plt.figure(dpi=750)
        self.canvas = FigureCanvas(figure)
        toolbar = NavigationToolbar(self.canvas, self)
        
        self.axes = figure.add_subplot()
        self.axes.axis('off')

        # self.plot()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

    def plot(self,) -> None:
        ''' plot some random stuff '''
        
        # self.axes.axis('on')
        self.axes.axis('on')
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.postplot()
        self.canvas.draw()
    
    
    def postplot(self,):
        pass


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    canvas = Canvas()
    mainWindow = QMainWindow()
    mainWindow.setCentralWidget(canvas)
    
    mainWindow.show()
    import time
    time.sleep(5)
    canvas.plot()
    sys.exit(app.exec_())
    