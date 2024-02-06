import sys
from PyQt5.QtWidgets import QWidget

sys.path.insert(1, './ui_files')
from videoSettings import Ui_videoSettings

class VideoSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.ui = Ui_videoSettings()
        self.ui.setupUi(self)
