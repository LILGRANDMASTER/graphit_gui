from PyQt5.QtWidgets import QLabel

class VideoFrameLabel(QLabel):
    imgWidth = 800
    imgHeight = 500

    def __init__(self):
        super().__init__()
        self.resize(self.imgWidth, self.imgHeight)
        self.setText("Wait before video appears...")

