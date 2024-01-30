import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtGui import QColor
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class OpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Устанавливаем цвет фона (черный)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)  # Очищаем буфер цвета
        glLoadIdentity()  # Сбрасываем текущую матрицу

        self.draw_octagon(0.5, "red")  # Рисуем внешний восьмиугольник
        self.draw_octagon(0.3, "green")  # Рисуем внутренний восьмиугольник

        glFlush()  # Принудительно выводим все команды на выполнение

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)  # Устанавливаем область вывода

    def draw_octagon(self, size, color):
        if(color == "red"):
            glColor3f(1.0, 0.0, 0.0)  # Устанавливаем цвет (красный)
        else:
            glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_POLYGON)  # Начинаем рисовать многоугольник

        # Указываем вершины восьмиугольника
        glVertex2f(-size, size)
        glVertex2f(-size/2, size*1.5)
        glVertex2f(size/2, size*1.5)
        glVertex2f(size, size)
        glVertex2f(size, -size)
        glVertex2f(size/2, -size*1.5)
        glVertex2f(-size/2, -size*1.5)
        glVertex2f(-size, -size)

        glEnd()  # Завершаем рисование многоугольника

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