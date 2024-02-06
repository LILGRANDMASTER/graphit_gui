# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\videoSettings.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_videoSettings(object):
    def setupUi(self, videoSettings):
        videoSettings.setObjectName("videoSettings")
        videoSettings.resize(423, 111)
        self.widget = QtWidgets.QWidget(videoSettings)
        self.widget.setGeometry(QtCore.QRect(10, 10, 401, 88))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.autocalibrateColor = QtWidgets.QPushButton(self.widget)
        self.autocalibrateColor.setObjectName("autocalibrateColor")
        self.gridLayout.addWidget(self.autocalibrateColor, 1, 0, 1, 1)
        self.useFilter = QtWidgets.QPushButton(self.widget)
        self.useFilter.setObjectName("useFilter")
        self.gridLayout.addWidget(self.useFilter, 1, 1, 1, 1)
        self.zoomValue = QtWidgets.QSlider(self.widget)
        self.zoomValue.setOrientation(QtCore.Qt.Horizontal)
        self.zoomValue.setObjectName("zoomValue")
        self.gridLayout.addWidget(self.zoomValue, 1, 2, 1, 1)
        self.colorSettings = QtWidgets.QPushButton(self.widget)
        self.colorSettings.setObjectName("colorSettings")
        self.gridLayout.addWidget(self.colorSettings, 2, 0, 1, 1)
        self.changeView = QtWidgets.QPushButton(self.widget)
        self.changeView.setObjectName("changeView")
        self.gridLayout.addWidget(self.changeView, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.retranslateUi(videoSettings)
        QtCore.QMetaObject.connectSlotsByName(videoSettings)

    def retranslateUi(self, videoSettings):
        _translate = QtCore.QCoreApplication.translate
        videoSettings.setWindowTitle(_translate("videoSettings", "Form"))
        self.label.setText(_translate("videoSettings", "Настройка цвета"))
        self.label_3.setText(_translate("videoSettings", "Увеличение"))
        self.autocalibrateColor.setText(_translate("videoSettings", "Автокалибровка"))
        self.useFilter.setText(_translate("videoSettings", "Применить фильтр"))
        self.colorSettings.setText(_translate("videoSettings", "Ручная настройка"))
        self.changeView.setText(_translate("videoSettings", "Изменить вид"))
        self.label_2.setText(_translate("videoSettings", "Отображение"))
