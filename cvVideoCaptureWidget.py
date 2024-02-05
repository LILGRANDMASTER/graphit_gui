import sys
from PyQt5.QtWidgets import QWidget


sys.path.insert(1, './ui_files')
from cvVideoCapture import Ui_cvVideoCapture
from PyQt5.QtGui import QMouseEvent, QColor, QCursor
from PyQt5.QtCore import pyqtSignal, QTimer, QPoint

class VideoCaptureWidget(QWidget):
	mouseSignal = pyqtSignal(tuple)
	cursorSignal = pyqtSignal(tuple)

	def __init__(self, parent=None):
		super().__init__(parent=None)

		self.ui = Ui_cvVideoCapture()
		self.ui.setupUi(self)

		self.timer = QTimer()
		self.timer.timeout.connect(self.mouseMotion)
		self.timer.start(5000)
		

	def mouseDoubleClickEvent(self, event):
		print('double click')
		pixmap = self.ui.opencvFrameLabel.pixmap()
		image = pixmap.toImage()

		print(event.x() - 23, event.y() - 20)
		c = image.pixel(event.x() - 23, event.y() - 20)
		colors = QColor(c).getRgb()

		colors = colors + (event.x() - 23, event.y() - 20)

		self.mouseSignal.emit(colors)

	def mouseMotion(self):
		self.timer.setInterval(100)

		cursorPos = QCursor.pos()
		tup = (cursorPos.x(), cursorPos.y() - 375)

		pixmap = self.ui.opencvFrameLabel.pixmap()
		image = pixmap.toImage()

		c = image.pixel(tup[0] - 23, tup[1] - 20)
		colors = QColor(c).getRgb()

		colors = colors + (tup[0] - 23, tup[1] - 20)
	
		self.cursorSignal.emit(colors)
		
		
