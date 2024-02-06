from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent, QColor

class VideoFrameLabel(QLabel):
    imgWidth = 800
    imgHeight = 500
    mouseSignal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.resize(self.imgWidth, self.imgHeight)
        self.setText("Wait before video appears...")


    def mouseDoubleClickEvent(self, event):
        image = self.pixmap().toImage()

        colors = QColor(image.pixel(event.x(), event.y())).getRgb()
        colors = colors + (event.x(), event.y())

        self.mouseSignal.emit(colors)

