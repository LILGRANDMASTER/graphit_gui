import sys
import numpy as np
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
								QApplication, QVBoxLayout, QWidget,
								QLabel, QGridLayout, QPushButton, 
								QHBoxLayout, QLineEdit, QComboBox,
								QMainWindow, QMenuBar, QMenu, QAction
							)

from PyQt5 import uic


from regisgrationWidget import RegistrationWidget
from servoSettingsWidget import ServoSettingsWidget
from cvVideoCaptureWidget import VideoCaptureWidget
from videoCapture import VideoThread

class Main_Window(QMainWindow):

	def __init__(self):
		super().__init__()

		#WINDOW PARAMETERS
		self.resize(1100, 1000)
		self.setWindowTitle('GRAPHIT')
		self.setWindowIcon(QIcon('./icons/grafit_rosatom.png'))

		#OPENCV VIDEO SHAPE
		self.imgWidth = 500
		self.imgHeight = 300

		#CREATING CENTRAL WIDGET
		self.mainWidget = QWidget()
		
		#CREATING LAYOUTS
		mainGrid = QGridLayout()

		#CREATING WIDGETS
		registrationWin = RegistrationWidget()

		servoSettings = ServoSettingsWidget()

		self.videoCapture = VideoCaptureWidget()

		#self.opencvFrameLabel = QLabel("hello, world")
		#self.opencvFrameLabel.resize(self.imgWidth, self.imgHeight)

		
		#ADDING WIDGETS TO LAYOUTS
		mainGrid.addWidget(registrationWin, 0, 0)
		mainGrid.addWidget(servoSettings, 1, 1)
		mainGrid.addWidget(self.videoCapture, 1, 0)

		#SETTING LAYOUTS TO CENTRAL WIDGET
		self.mainWidget.setLayout(mainGrid)
		self.setCentralWidget(self.mainWidget)
		
		#CREATING MENU BAR
		self._createActions()
		self._createMenuBar()


		#CREATING VIDEO THREAD FROM OPENCV
		self.vidThread = VideoThread()
		self.vidThread.frameSignal.connect(self.updateImage)
		self.vidThread.start()
		


	def _createMenuBar(self):
		menu_bar = self.menuBar()

		#File menu
		self.fileMenu = menu_bar.addMenu('Файл')

		self.fileMenu.addAction(self.openAction)
		self.fileMenu.addAction(self.loadAction)
		self.fileMenu.addAction(self.saveAsAction)
		self.fileMenu.addAction(self.exitAction)

		#Help menu
		self.helpMenu = menu_bar.addMenu('Помощь')

		self.helpMenu.addAction(self.helpAction)
		self.helpMenu.addAction(self.aboutAction)


	def _createActions(self):
		#File
		self.openAction 		= QAction("Открыть...", self)
		self.loadAction 		= QAction("Загрузить...", self)
		self.saveAsAction 		= QAction("Сохранить как...", self)
		self.exitAction 		= QAction("Выйти", self)

		#Help
		self.helpAction			= QAction("Справка", self)
		self.aboutAction		= QAction("О программе", self)


	def cv2qt(self, cvImg):
		"""Converts cv image to qt image"""
		rgbImage = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
		h, w, ch = rgbImage.shape
		bytesPerLine = ch * w

		qtFormatImage = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
		result = qtFormatImage.scaled(self.imgWidth, self.imgHeight, Qt.KeepAspectRatio)
		return QPixmap.fromImage(result)
	

	@pyqtSlot(np.ndarray)
	def updateImage(self, cvImg):
		"""Updates imageLabel with opencv image"""
		qtImg = self.cv2qt(cvImg)
		self.videoCapture.ui.opencvFrameLabel1.setPixmap(qtImg)
		self.videoCapture.ui.opencvFrameLabel2.setPixmap(qtImg)
		#self.opencvFrameLabel.setPixmap(qtImg)






app = QApplication(sys.argv)
win = Main_Window()
win.show()

exit(app.exec_())




