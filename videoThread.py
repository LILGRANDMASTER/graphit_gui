from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    frameSignal = pyqtSignal(np.ndarray)
    useFilter = False

    xMouse = 0
    yMouse = 0

    text = ""
    
    delta = 20

    zoom = 100

    
    class Color:
       def __init__(self, red, green, blue):
           self.r = red
           self.g = green
           self.b = blue

    
    lbColor = Color(0, 0, 0)
    ubColor = Color(255, 255, 255)
    color = Color(0, 0, 0)

    def run(self):
        videoFrame = cv2.VideoCapture(0)

        while True:
            ret, cvImg = videoFrame.read()
            
            if ret:
                self.frameSignal.emit(self.processImage(cvImg))



    def zoom_at(self, img, zoom, angle=0):
        coord = (self.xMouse, self.yMouse)

        cy, cx = [i / 2 for i in img.shape[:-1]] if coord is None else coord[::-1]
        rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, int(zoom))
        result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)

        return result

    

    def processImage(self, cvImg):
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, 0]], np.float32)
        kernel = 1 / 3 * kernel

        frame = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        frame = self.zoom_at(frame, int(self.zoom / 100))

        lowerBound = np.array([self.lbColor.r, self.lbColor.g, self.lbColor.b])
        upperBound = np.array([self.ubColor.r, self.ubColor.g, self.ubColor.b])

        oImg = cv2.inRange(frame, lowerBound, upperBound)
        oImg = cv2.filter2D(oImg, -1, kernel)
        
        contours, hierarchy = cv2.findContours(oImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        cv2.drawContours(frame, contours, -1, (0,255,0), 1, cv2.LINE_AA, hierarchy, 1 )

        r = self.color.r
        g = self.color.g
        b = self.color.b

        cv2.circle(frame, (self.xMouse, self.yMouse), 1, (255 - b, 255 - g, 255 - r), thickness=7)
        cv2.putText(frame, self.text, (self.xMouse, self.yMouse), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255 - b, 255 - g, 255 - r), 1, 5)


        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        oImg = cv2.cvtColor(oImg, cv2.COLOR_RGB2BGR)

        if self.useFilter:
            return oImg
        else:
            return frame



    def click(self, event):
        self.xMouse = event[-2]
        self.yMouse = event[-1]

        r = event[0]
        g = event[1]
        b = event[2]

        self.color = self.Color(r, g, b)
        
        r1 = r - self.delta if r - self.delta > 0 else 0
        g1 = g - self.delta if g - self.delta > 0 else 0
        b1 = b - self.delta if b - self.delta > 0 else 0

        r2 = r + self.delta if r + self.delta < 255 else 255
        g2 = g + self.delta if g + self.delta < 255 else 255
        b2 = b + self.delta if b + self.delta < 255 else 255


        color_str = str(r) + " " + str(g) + " " + str(b)
        self.text = color_str
        
        self.calibrate(r1, g1, b1, r2, g2, b2)

    
    def autocalibrate(self):
        self.lbColor = self.Color(0, 0, 0)
        self.ubColor = self.Color(40, 40, 40)

    def calibrate(self, r1, g1, b1, r2, g2, b2):
        self.lbColor = self.Color(r1, g1, b1)
        self.ubColor = self.Color(r2, g2, b2)
