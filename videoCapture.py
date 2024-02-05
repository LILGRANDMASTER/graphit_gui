from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import pyautogui

x_mouse = 0
y_mouse = 0
mouse_coord = [0]*2
r = 0
g = 0
b = 0 
text = ""
class VideoThread(QThread):
    frameSignal = pyqtSignal(np.ndarray)
    useFilter = False



    class Color:
        def __init__(self, red, green, blue):
            self.r = red
            self.g = green
            self.b = blue

    lbColor = Color(0, 0, 0)
    ubColor = Color(255, 255, 255)

    def run(self):
        videoFrame = cv2.VideoCapture(1)

        while True:
            ret, cvImg = videoFrame.read()

            if ret:
                self.frameSignal.emit(self.processImage(cvImg))

    def zoom_at(self, img, zoom, angle=0):
        global x_mouse, y_mouse, mouse_coord
        coord = (x_mouse, y_mouse)

        cy, cx = [i / 2 for i in img.shape[:-1]] if coord is None else coord[::-1]
        rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, int(zoom))
        result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)

        return result

    def processImage(self, cvImg):
        global r,g,b,mouse_coord, text
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, 0]], np.float32)
        kernel = 1 / 3 * kernel
        zoom = 200
        N_square = 10
        N_points = 500

        frame = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)

        
        frame = self.zoom_at(frame, int(zoom / 100))

        lowerBound = np.array([self.lbColor.r, self.lbColor.g, self.lbColor.b])
        upperBound = np.array([self.ubColor.r, self.ubColor.g, self.ubColor.b])
        oImg = cv2.inRange(frame, lowerBound, upperBound)
        oImg = cv2.filter2D(oImg, -1, kernel)

       

        contours, hierarchy = cv2.findContours(oImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, (10 ** (-N_square)) * cv2.arcLength(cnt, True), True)
            n = approx.ravel()
            
            if (len(approx) >= 3):
                for i in range(0, 5, 1):
                    for i in range(2, len(approx), 1):
                        x_1 = approx[i - 2][0][0]
                        y_1 = approx[i - 2][0][1]
                        x_2 = approx[i][0][0]
                        y_2 = approx[i][0][1]
                        x_0 = approx[i - 1][0][0]
                        y_0 = approx[i - 1][0][1]
                        eter = i + 1
                        try:
                            approx[i - 1][0][0] = int(x_0 + (np.abs(
                                (y_2 - y_1) * x_0 - (x_2 - x_1) * y_0 - x_1 * (y_2 - y_1) + y_1 * (x_2 - x_1)) * (
                                                                     y_2 - y_1)) // (
                                                              eter * ((y_2 - y_1) ** 2 + (x_2 - x_1) ** 2)))
                            approx[i - 1][0][1] = int(y_0 - (np.abs(
                                (y_2 - y_1) * x_0 - (x_2 - x_1) * y_0 - x_1 * (y_2 - y_1) + y_1 * (x_2 - x_1)) * (
                                                                     x_2 - x_1)) // (
                                                              eter * ((y_2 - y_1) ** 2 + (x_2 - x_1) ** 2)))
                        except ValueError:
                            print(' ')

            i = 0
            x_max = 0
            y_max = 0
            x_min = 32768
            y_min = 32768
            for j in n:
                if (i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]
                    if (x >= x_max):
                        x_max = x
                    if (y >= y_max):
                        y_max = y
                    if (x <= x_min):
                        x_min = x
                    if (y <= y_min):
                        y_min = y
                i = i + 1
            center_x = int((x_max + x_min) / 2)
            center_y = int((y_max + y_min) / 2)
            if (n.size >= N_points):
                i = 0
                min_dist = 32768
                for j in n:
                    if (i % 2 == 0):
                        x = n[i]
                        y = n[i + 1]
                        dist = np.sqrt(((center_x - x) ** 2 + (center_y - y) ** 2))
                        if (dist < min_dist):
                            min_dist = dist
                    i = i + 1
                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 1)
                cv2.circle(frame, (center_x, center_y), 1, (0, 0, 255), thickness=2)
                countur_width = (min_dist) / ((zoom / 100) * np.sqrt(2))
                distance_uncorrect = 1 / (countur_width) * 5 * 26.671
                width_new = "(" + "%f" % distance_uncorrect + ")"
                cv2.putText(frame, width_new, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                           (0, 0, 255), 1, 2)
        cv2.circle(frame, (x_mouse, y_mouse), 1, (255 - b, 255 - g, 255 - r), thickness=7)
        cv2.putText(frame, text, (x_mouse, y_mouse), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255 - b, 255 - g, 255 - r), 1, 5)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        oImg = cv2.cvtColor(oImg, cv2.COLOR_RGB2BGR)

        if self.useFilter:
            return oImg
        else:
            return frame

    def click(self, event):
        print('click')
        global x_mouse, y_mouse, mouse_coord, text, r, g, b
        
        x = event[-2]
        y = event[-1]

        r = event[0]
        g = event[1]
        b = event[2]

        mouse_coord = (x,y)
        
        delta = 20
        if r - delta > 0:
            r1 = r - delta
        else:
            r1 = 0
        if g - delta > 0:
            g1 = g - delta
        else:
            g1 = 0
        if b - delta > 0:
            b1 = b - delta
        else:
            b1 = 0
        if r + delta < 255:
            r2 = r + delta
        else:
            r2 = 255
        if g + delta < 255:
            g2 = g + delta
        else:
            g2 = 255
        if b + delta < 255:
            b2 = b + delta
        else:
            b2 = 255


        
        
        color_str = str(r) + " " + str(g) + " " + str(b)
        text = color_str
        

        self.calibrate(r1, g1, b1, r2, g2, b2)


    def motion(self, event):
        global x_mouse, y_mouse, r, g, b, text

        x_mouse = event[-2]
        y_mouse = event[-1]
        
        r = event[0]
        g = event[1]
        b = event[2]

        color_str = str(r) + " " + str(g) + " " + str(b)
        text = color_str




    def autocalibrate(self):
        self.lbColor = self.Color(0, 0, 0)
        self.ubColor = self.Color(40, 40, 40)

    def calibrate(self, r1, g1, b1, r2, g2, b2):
        self.lbColor = self.Color(r1, g1, b1)
        self.ubColor = self.Color(r2, g2, b2)




        



        



