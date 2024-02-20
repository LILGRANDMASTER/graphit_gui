import sys
from PyQt5.QtWidgets import QWidget
from pyModbusTCP.client import ModbusClient

sys.path.insert(1, './ui_files')
from servoSettings import Ui_servoSettings

class ServoSettingsWidget(QWidget):
    max_speed = 2000
    min_speed = 1
    motor_state = [False] * 16
    motor_default_speed = [1000, 2000, 1000, 2000, 1000, 2000, 1000, 2000]
    distance = [0] * 8
    distance_state = [0] * 8

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_servoSettings()
        self.ui.setupUi(self)

        #connecting buttions
        self.ui.activate1.clicked.connect(lambda: self.changeMotorState(0))
        self.ui.activate2.clicked.connect(lambda: self.changeMotorState(2))
        self.ui.activate3.clicked.connect(lambda: self.changeMotorState(4))
        self.ui.activate4.clicked.connect(lambda: self.changeMotorState(6))
        self.ui.activate5.clicked.connect(lambda: self.changeMotorState(8))
        self.ui.activate6.clicked.connect(lambda: self.changeMotorState(10))
        self.ui.activate7.clicked.connect(lambda: self.changeMotorState(12))
        self.ui.activate8.clicked.connect(lambda: self.changeMotorState(14))

        self.ui.stop1.clicked.connect(lambda: self.changeMotorState(1))
        self.ui.stop2.clicked.connect(lambda: self.changeMotorState(3))
        self.ui.stop3.clicked.connect(lambda: self.changeMotorState(5))
        self.ui.stop4.clicked.connect(lambda: self.changeMotorState(7))
        self.ui.stop5.clicked.connect(lambda: self.changeMotorState(9))
        self.ui.stop6.clicked.connect(lambda: self.changeMotorState(11))
        self.ui.stop7.clicked.connect(lambda: self.changeMotorState(13))
        self.ui.stop8.clicked.connect(lambda: self.changeMotorState(15))


    def readSpeed(self):
        self.motor_default_speed[0] = int(self.ui.velocity1.text())
        self.motor_default_speed[1] = int(self.ui.velocity2.text())
        self.motor_default_speed[2] = int(self.ui.velocity3.text())
        self.motor_default_speed[3] = int(self.ui.velocity4.text())
        self.motor_default_speed[4] = int(self.ui.velocity5.text())
        self.motor_default_speed[5] = int(self.ui.velocity6.text())
        self.motor_default_speed[6] = int(self.ui.velocity7.text())
        self.motor_default_speed[7] = int(self.ui.velocity8.text())


    def changeMotorState(self, index):
        self.motor_state[index] = not self.motor_state[index]
        self.readSpeed()
        self.send()


    def send(self):
        c = ModbusClient(host="192.168.0.10", auto_open=True, auto_close=True)

        regs = c.read_holding_registers(23, 16)
        print(regs)
        for k in range(0, 7, 1):
            l = regs[k + 8]
            j = regs[k]
            self.distance[k] = l
            self.distance_state[k] = j
        motor = [0] * 8
        revers = [0] * 8

        n = 0
        for i in self.motor_state:
            if (n % 2 == 0):
                if i == True:
                    motor[n // 2] = 1
                else:
                    motor[n // 2] = 0
            else:
                if i == True:
                    revers[n // 2] = 1
                else:
                    revers[n // 2] = 0
            n += 1

        if c.write_multiple_registers(0, (motor[0], motor[1], motor[2], motor[3],
                                        motor[4], motor[5], motor[6], motor[7],
                                        self.motor_default_speed[0], self.motor_default_speed[1],
                                        self.motor_default_speed[2], self.motor_default_speed[3],
                                        self.motor_default_speed[4], self.motor_default_speed[5],
                                        self.motor_default_speed[6], self.motor_default_speed[7],
                                        revers[0], revers[1], revers[2], revers[3],
                                        revers[4], revers[5], revers[6], revers[7])):
            print("write ok")
        else:
            print("write error")


    
