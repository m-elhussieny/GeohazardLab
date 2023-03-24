import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from app.widgets import DataWidget, ImageWidget, ProcessWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Classifcation')
        self.resize(600, 1200)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../icons/lsgi.ico')))
        wid = QWidget(self)
        self.setCentralWidget(wid)
        
        layout = QVBoxLayout()
        wid.setLayout(layout)

        self.model = DataWidget()
        # self.model.setGeometry(QRect(100, 30, 400, 120))
        layout.addWidget(self.model)

        self.image = ImageWidget()
        layout.addWidget(self.image)

        self.process = ProcessWidget()
        layout.addWidget(self.process)
        
        self.show()
    
    def showmsg(self) -> None:
        self.label.setText('You clicked me')
        self.canvas.plot()
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    # start the app
    sys.exit(app.exec_())