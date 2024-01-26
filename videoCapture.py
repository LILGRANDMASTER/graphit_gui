from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    frameSignal = pyqtSignal(np.ndarray)
    
    class Color:
       def __init__(self, red, green, blue):
           self.r = red
           self.g = green
           self.b = blue

    
    lbColor = Color(0, 0, 0)
    ubColor = Color(255, 255, 255)

    def run(self):
        videoFrame = cv2.VideoCapture(0)

        while True:
            ret, cvImg = videoFrame.read()
            
            if ret:
                self.frameSignal.emit(self.processImage(cvImg))


    def processImage(self, cvImg):
        frame = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)

        lowerBound = np.array([self.lbColor.r, self.lbColor.g, self.lbColor.b])
        upperBound = np.array([self.ubColor.r, self.ubColor.g, self.ubColor.b])

        oImg = cv2.inRange(frame, lowerBound, upperBound)
        
        contours, hierarchy = cv2.findContours(oImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        cv2.drawContours(frame, contours, -1, (0,255,0), 1, cv2.LINE_AA, hierarchy, 1 )

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return frame
    
    def autocalibrate(self):
        self.lbColor = self.Color(0, 0, 0)
        self.ubColor = self.Color(40, 40, 40)

    def calibrate(self, r1, g1, b1, r2, g2, b2):
        self.lbColor = self.Color(r1, g1, b1)
        self.ubColor = self.Color(r2, g2, b2)




        



        



