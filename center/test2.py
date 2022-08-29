#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import serial,time
# import termios


# port = "/dev/ttyACM0"  # Arduino端口
# timeout = 0.005
# ser = serial.Serial(port=port,timeout=0, baudrate=9600,dsrdtr=False)
# ser = serial.Serial()
# print(1)
# ser.port = port
# ser.baudrate = 9600
# # ser.timeout = 1
# ser.setDTR(False)
# ser.open()
# print(2)
# print("ser",ser)
# print(3)


port = '/dev/ttyACM0'
# f = open(port)
# attrs = termios.tcgetattr(f)
# attrs[2] = attrs[2] & ~termios.HUPCL
# termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
# f.close()
ser = serial.Serial()
ser.baudrate = 9600
ser.port = port
# ser.setDTR(False)
ser.open()


def main():
    cmd="MF 40."
    ser.write(cmd.encode())
    try:
        ret_all = ""
        while True:
            print("response:-----------------------------------------------------------------")
            response = ser.readall()
            ret_all += str(response,"UTF-8")
            print(ret_all)
    except Exception as e:
        print("serial连接或者执行失败,reason:")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("ctrl+c stop")
        ser.close()
