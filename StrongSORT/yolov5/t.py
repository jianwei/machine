#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# from time import time
import uuid
import time
import serial
import termios
import re
from utils.serial_control import serial_control
ser = serial_control()


def main(cmd):
    cmd_dict = {
        "uuid": str(uuid.uuid1()),
        "cmd": cmd,
        "from": "camera",
    }
    ser.send_cmd(cmd_dict)
    print(ser.get_ret())


def __init__():
    port = "/dev/ttyACM0"  # Arduino端口
    f = open(port)
    attrs = termios.tcgetattr(f)
    attrs[2] = attrs[2] & ~termios.HUPCL
    termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
    f.close()

    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = port
    ser.open()

    # 触发复位
    # print("begin sleep",time.time())
    # ser.write("default.".encode())
    # time.sleep(1)
    # print("end sleep",time.time())
    return ser


def send_cmd(cmd, ser):
    ser.write(cmd.encode())
    ret_all = ""
    while (1):
        response = ser.read()
        ret_all += str(response, "UTF-8")
        response_arr = ret_all.splitlines()
        ret = response_arr[len(response_arr) - 1] if len(response_arr) > 0 else ""
        s1 = re.compile('^(-?[1-9]|0{1}\d*)$')
        r1 = s1.findall(ret)
        if (len(r1) > 0):
            print("cmd:",cmd,r1[0])
            break
    pass

if __name__ == "__main__":
    try:
        main("STOP 0.")
        main("MU.")
        main("STOP 2.")
        main("MF 15.")
        # ser = __init__()
        # send_cmd("STOP 0.", ser)
        # send_cmd("MF.", ser)
        # send_cmd("STOP 0.", ser)
        # s1=re.compile('^(-?[1-9]|0{1}\d*)$')
        # r1=s1.findall("1a")
        # print(r1)
    except KeyboardInterrupt:
        print("ctrl+c stop")
        # main("STOP.")
        ser.close()
