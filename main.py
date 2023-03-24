from PyQt5.QtWidgets import QApplication
from app import Window
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # start the app
    sys.exit(app.exec_())
    