from pyModbusTCP.client import ModbusClient


def send():
    global motor_state, motor_default_speed, distance, distance_state
    c = ModbusClient(host="192.168.0.10", auto_open=True, auto_close=True)

    regs = c.read_holding_registers(23, 16)
    print(regs)
    for k in range(0, 7, 1):
        l = regs[k + 8]
        j = regs[k]
        distance[k] = l
        distance_state[k] = j
    motor = [0] * 8
    revers = [0] * 8

    n = 0
    for i in motor_state:
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
                                      motor_default_speed[0], motor_default_speed[1],
                                      motor_default_speed[2], motor_default_speed[3],
                                      motor_default_speed[4], motor_default_speed[5],
                                      motor_default_speed[6], motor_default_speed[7],
                                      revers[0], revers[1], revers[2], revers[3],
                                      revers[4], revers[5], revers[6], revers[7])):
        print("write ok")
    else:
        print("write error")

class ModBus:
    max_speed = 2000
    min_speed = 1
    motor_state = [False] * 16
    motor_default_speed = [1000, 2000, 1000, 2000, 1000, 2000, 1000, 2000]
    distance = [0] * 8
    distance_state = [0] * 8
