import sys
import datetime
from PyQt5.QtWidgets import QWidget

sys.path.insert(1, './ui_files')
from registrationWindow import Ui_registrationWin

class RegistrationWidget(QWidget):
	reg = False

	def __init__(self, parent=None):
		super().__init__(parent=None)

		self.ui = Ui_registrationWin()
		self.ui.setupUi(self)
        
		self.ui.login.clicked.connect(self.saveRegistration)

	def saveRegistration(self):
		
		today = datetime.datetime.today().strftime('%d.%m.%Y-%H:%M')
		fio = self.ui.opSecName.text() + ' ' + self.ui.opName.text() + ' ' + self.ui.opProton.text() + ' ' + today + '\n'

		self.ui.login.setStyleSheet('QPushButton {background-color: green;}')

		journal = open('./log/registration.txt', 'a', encoding='utf-8')
		if self.reg == False:
			journal.write(fio)
			self.reg = True
		journal.close()

