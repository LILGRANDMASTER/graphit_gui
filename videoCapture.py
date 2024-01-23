from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    frameSignal = pyqtSignal(np.ndarray)

    def run(self):
        videoFrame = cv2.VideoCapture(0)

        while True:
            ret, cvImg = videoFrame.read()
            
            if ret:
                self.frameSignal.emit(cvImg)



