from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QGridLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import functools

class Shaft_Visual(QWidget):

	def __init__(self):
		super().__init__()
		self.resize(400,400)

		#Массивы для стержней и вертикальных лэйаутов
		self.shafts = []
		self.vboxes  = []

		self.init_widgets()


	def init_widgets(self):
		
		#Создание массива стержней
		for i in range(0,40):
			self.shafts.append(QPushButton())
			self.shafts[i].setMinimumSize(5, 50)
			self.shafts[i].setMaximumSize(20, 600)
			self.shafts[i].clicked.connect(functools.partial(self.change_color_green, i))

		
		#Создание вертикальных лэйаутов
		for i in range(0, 5):
			self.vboxes.append(QVBoxLayout())

		#Горизонтальный лэйаут для отображения стержней
		#В месте отверстия используем вертикальный лэйаут
		self.hbox = QHBoxLayout()

		

		index = 0			#Номер стержня (размер стержня 355)

		#Визуализация расположения стержней
		for i in range(0,30):
			if(i >= 10 and i < 15):
				self.hbox.addLayout(self.vboxes[i - 10])

				self.vboxes[i - 10].addWidget(self.shafts[index])
				index += 1
				self.vboxes[i - 10].addWidget(self.shafts[index])
				index += 1
			else:
				self.hbox.addWidget(self.shafts[index])
				index += 1

		self.setLayout(self.hbox)


	def change_color_green(self, index):
		self.shafts[index].setStyleSheet('QPushButton {background-color: green; color: green;}')

	def change_color_red(self, index):
		self.shafts[index].setStyleSheet('QPushButton {background-color: red; color: red;}')