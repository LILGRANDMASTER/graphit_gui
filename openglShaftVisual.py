import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtGui import QColor
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import enum



forms = {
    'triangle': 3,
    'sqare': 4,
    'pentagon': 5,
    'hexagon': 6,
    'heptagon': 7,
    'octagon': 8,
    'ninesided': 9,
    'decagon': 10
}

class OpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Устанавливаем цвет фона (черный)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)  # Очищаем буфер цвета
        glLoadIdentity()  # Сбрасываем текущую матрицу

        self.drawPolygon('octagon', 1, [1.0, 1.0, 1.0])  # Рисуем внешний восьмиугольник
        self.drawPolygon('octagon', 0.5, [0.0, 0.0, 0.0]) #Рисуем внутренний восьмиугольник
        self.drawHatching()

        glFlush()  # Принудительно выводим все команды на выполнение

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)  # Устанавливаем область вывода


    def drawPolygon(self, type, size, color):
        glColor3f(color[0], color[1], color[2])  # Устанавливаем цвет рисования (белый)

        # Рисуем многоугольник
        glBegin(GL_POLYGON)
        for i in range(forms[type]):
            angle = 2 * 3.14159 * i / forms[type]
            x = size * np.cos(angle)
            y = size * np.sin(angle)
            glVertex2f(x, y)
        glEnd()

    def drawHatching(self):
        glColor3f(0.0, 0.0, 0.0)  # Устанавливаем цвет вертикальных линий (черный)
        glBegin(GL_LINES)
        num_lines = 50  # Количество линий
        for i in range(num_lines):
            x = -1 + (1.0 / num_lines) * i
            glVertex2f(x, 1)
            glVertex2f(x, -1)
        glEnd()


#ДЛЯ ОТЛАДКИ
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем OpenGL виджет и устанавливаем его в качестве центрального виджета окна
        self.openGLWidget = OpenGLWidget(self)
        self.setCentralWidget(self.openGLWidget)

        self.setWindowTitle("PyQt OpenGL Octagon")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())