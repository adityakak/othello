from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

        start_button = QPushButton('Start Watching')
        start_button.setStyleSheet("background-color : green")
        start_button.adjustSize()
        self.show()

def create():
    app = QApplication([])
    app.setStyle('Fusion')
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    create()