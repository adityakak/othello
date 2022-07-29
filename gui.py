from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        def close_program():
            print("Closing")
            self.close()

        flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

        close_button = QPushButton('Close Program')
        close_button.clicked.connect(close_program)
        
        self.show()

def create():
    app = QApplication([])
    app.setStyle('Fusion')
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    create()