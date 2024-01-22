import sys
from PyQt5.QtCore import Qt
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

class Main_Window(QMainWindow):

	def __init__(self):
		super().__init__()

		self.resize(1100, 800)
		self.setWindowTitle('GRAPHIT')
		self.setWindowIcon(QIcon('./icons/grafit_rosatom.png'))

		#CREATING CENTRAL WIDGET
		self.mainWidget = QWidget()
		
		#CREATING LAYOUTS
		mainGrid = QGridLayout()

		#CREATING WIDGETS
		registrationWin = RegistrationWidget()
		servoSettings = ServoSettingsWidget()

		
		#ADDING WIDGETS TO LAYOUTS
		mainGrid.addWidget(registrationWin, 0, 0)
		mainGrid.addWidget(servoSettings, 1, 1)

		#SETTING LAYOUTS TO CENTRAL WIDGET
		self.mainWidget.setLayout(mainGrid)
		self.setCentralWidget(self.mainWidget)
		
		#CREATING MENU BAR
		self._createActions()
		self._createMenuBar()


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





app = QApplication(sys.argv)
win = Main_Window()
win.show()

exit(app.exec_())




