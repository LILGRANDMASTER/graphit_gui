import sys
from PyQt5.QtWidgets import QWidget

sys.path.insert(1, './ui_files')
from servoSettings import Ui_servoSettings

class ServoSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_servoSettings()
        self.ui.setupUi(self)
