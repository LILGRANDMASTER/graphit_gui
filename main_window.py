import sys
from PyQt5.QtGui import QMouseEvent
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


from regisgrationWidget import RegistrationWidget
from servoSettingsWidget import ServoSettingsWidget
from colorSettingsWidget import ColorSettingsWidget
from videoSettingsWidget import VideoSettingsWidget
from videoFrameLabel import VideoFrameLabel
from videoThread import VideoThread
from openglShaftVisual import OpenGLWidget
from modbus import ModBus

class Main_Window(QMainWindow):

	def __init__(self):
		super().__init__()

		#WINDOW PARAMETERS
		self.resize(1100, 1000)
		self.setWindowTitle('GRAPHIT')
		self.setWindowIcon(QIcon('./icons/grafit_rosatom.png'))
		self.setMouseTracking(True)

		#CREATING CENTRAL WIDGET
		self.mainWidget = QWidget()
		
		#CREATING LAYOUTS
		mainGrid = QGridLayout()
		hbox = QHBoxLayout()
		videoVBox = QVBoxLayout()

		#LAYOUT SETTINGS
		mainGrid.setRowStretch(0, 1)
		mainGrid.setRowStretch(1, 2)
		mainGrid.setColumnStretch(0, 1)
		mainGrid.setColumnStretch(1, 2)

		mainGrid.addLayout(hbox, 0, 1)
		mainGrid.addLayout(videoVBox, 1, 0)

		#CREATING WIDGETS
		registrationWin 	= RegistrationWidget()
		self.servoSettings 		= ServoSettingsWidget()
		self.colorSettings 	= ColorSettingsWidget()
		self.videoSettings 	= VideoSettingsWidget()
		self.videoFrame 	= VideoFrameLabel()
		
		openglShaftVisual 	= OpenGLWidget()
		info 				= QLabel()


		
		#ADDING WIDGETS TO LAYOUTS
		mainGrid.addWidget(registrationWin, 0, 0)
		mainGrid.addWidget(self.servoSettings, 1, 1)
		
		videoVBox.addWidget(self.videoFrame, Qt.AlignmentFlag.AlignLeft)
		videoVBox.addWidget(self.videoSettings, Qt.AlignmentFlag.AlignLeft)
		
		hbox.addWidget(openglShaftVisual)
		hbox.addWidget(info)
		hbox.addWidget(info)

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
		self.videoSettings.ui.autocalibrateColor.clicked.connect(self.vidThread.autocalibrate)
		self.videoSettings.ui.colorSettings.clicked.connect(self.openColorSettingsWindow)
		self.videoSettings.ui.useFilter.clicked.connect(self.useVideoFilter)
		self.videoFrame.mouseSignal.connect(self.vidThread.click)
		self.videoSettings.ui.zoomValue.valueChanged.connect(self.readZoomValue)

		#Выглядит по уебански, но работает
		color = [0] * 6
		try:
			color[0] = int(self.colorSettings.ui.r1.text())
			color[1] = int(self.colorSettings.ui.g1.text())
			color[2] = int(self.colorSettings.ui.b1.text())
			color[3] = int(self.colorSettings.ui.r2.text())
			color[4] = int(self.colorSettings.ui.g2.text())
			color[5] = int(self.colorSettings.ui.b2.text())
		except ValueError:
			print('Отсутствует значение цвета')

		
		self.colorSettings.ui.apply.clicked.connect(
			lambda: self.vidThread.calibrate(
				color[0], color[1], color[2], color[3], color[4], color[5]	
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
		result = qtFormatImage.scaled(self.videoFrame.imgWidth, self.videoFrame.imgHeight, Qt.KeepAspectRatio)
		return QPixmap.fromImage(result)
	

	@pyqtSlot(np.ndarray)
	def updateImage(self, cvImg):
		"""Updates imageLabel with opencv image"""
		qtImg = self.cv2qt(cvImg)
		self.videoFrame.setPixmap(qtImg)

	def openColorSettingsWindow(self):
		self.colorSettings.show()

	def useVideoFilter(self):
		self.vidThread.useFilter = not self.vidThread.useFilter

	def readZoomValue(self):
		self.vidThread.zoom = self.videoSettings.ui.zoomValue.value()





app = QApplication(sys.argv)
win = Main_Window()
win.show()

exit(app.exec_())




