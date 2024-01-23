import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
								QApplication, QVBoxLayout, QWidget,
								QLabel, QGridLayout, QPushButton, 
								QHBoxLayout, QLineEdit, QComboBox,
								QMainWindow, QMenuBar, QMenu, QAction
							)

sys.path.insert(1, './ui_files')
from cvVideoCapture import Ui_cvVideoCapture

class VideoCaptureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.ui = Ui_cvVideoCapture()
        self.ui.setupUi(self)
