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
from colorSettingsWidget import ColorSettingsWidget
from shaft_visual import Shaft_Visual
from videoCapture import VideoThread

class Main_Window(QMainWindow):

	def __init__(self):
		super().__init__()

		#WINDOW PARAMETERS
		self.resize(1100, 1000)
		self.setWindowTitle('GRAPHIT')
		self.setWindowIcon(QIcon('./icons/grafit_rosatom.png'))

		#OPENCV VIDEO SHAPE
		self.imgWidth = 800
		self.imgHeight = 500

		#CREATING CENTRAL WIDGET
		self.mainWidget = QWidget()
		
		#CREATING LAYOUTS
		mainGrid = QGridLayout()
		mainGrid.setRowStretch(0, 1)
		mainGrid.setRowStretch(1, 2)

		#CREATING WIDGETS
		registrationWin = RegistrationWidget()
		servoSettings = ServoSettingsWidget()
		self.videoCapture = VideoCaptureWidget()
		self.colorSettings = ColorSettingsWidget()
		shaftVisual = Shaft_Visual()


		
		#ADDING WIDGETS TO LAYOUTS
		mainGrid.addWidget(registrationWin, 0, 0)
		mainGrid.addWidget(servoSettings, 1, 1)
		mainGrid.addWidget(self.videoCapture, 1, 0)
		mainGrid.addWidget(shaftVisual, 0, 1)

		#SETTING LAYOUTS TO CENTRAL WIDGET
		self.mainWidget.setLayout(mainGrid)
		self.setCentralWidget(self.mainWidget)
		
		#CREATING MENU BAR
		self._createActions()
		self._createMenuBar()


		#CREATING VIDEO THREAD FROM OPENCV
		self.vidThread = VideoThread()
		self.vidThread.start()


		#CONNECT SLOTS AND SIGNALS
		self.vidThread.frameSignal.connect(self.updateImage)
		self.videoCapture.ui.autocalibrateColor.clicked.connect(self.vidThread.autocalibrate)
		self.videoCapture.ui.colorSettings.clicked.connect(self.openColorSettingsWindow)

		#Выглядит по уебански, но работает
		self.colorSettings.ui.apply.clicked.connect(
			lambda: self.vidThread.calibrate(
				int(self.colorSettings.ui.rl.text()),
				int(self.colorSettings.ui.gl.text()),
				int(self.colorSettings.ui.bl.text()),
				int(self.colorSettings.ui.ru.text()),
				int(self.colorSettings.ui.gu.text()),
				int(self.colorSettings.ui.bu.text())
			)
		)
		
		


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
		self.videoCapture.ui.opencvFrameLabel.setPixmap(qtImg)

	def openColorSettingsWindow(self):
		self.colorSettings.show()





app = QApplication(sys.argv)
win = Main_Window()
win.show()

exit(app.exec_())




