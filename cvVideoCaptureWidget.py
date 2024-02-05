import sys
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget

sys.path.insert(1, './ui_files')
from cvVideoCapture import Ui_cvVideoCapture

class VideoCaptureWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=None)

		self.ui = Ui_cvVideoCapture()
		self.ui.setupUi(self)


	def mouseDoubleClickEvent(self, event):
		print(event.x(), event.y())

		
