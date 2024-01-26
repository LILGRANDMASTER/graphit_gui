import sys
from PyQt5.QtWidgets import QWidget

sys.path.insert(1, './ui_files')
from registrationWindow import Ui_registrationWin

class RegistrationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.ui = Ui_registrationWin()
        self.ui.setupUi(self)


