#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import serial,time
import termios


port = "/dev/ttyACM0"  # Arduino端口

f = open(port)
attrs = termios.tcgetattr(f)
attrs[2] = attrs[2] & ~termios.HUPCL
termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
f.close()
ser = serial.Serial()
ser.baudrate = 9600
ser.port = port
# ser.setDTR(False)
ser.open()

# ser = serial.Serial(port=port,timeout=0, baudrate=9600)
# ser.write("default.".encode())  

def main():
    # cmd="MF 40."
    cmd="STOP."
    print("before cmd:",cmd)
    ser.write(cmd.encode())
    print("end cmd:",cmd)
    try:
        print(123)
        ret_all = ""
        n = 1
        while True:
            n+=1
            print("response:0-----------------------------------------------------------------",n)
            response = ser.read()
            print("response:1-----------------------------------------------------------------",n,response)
            if (response):
                print("response:2-----------------------------------------------------------------",n,response)
                ret_all += str(response,"UTF-8")
                print(ret_all)
            time.sleep(0.1)
    except Exception as e:
        print("serial连接或者执行失败,reason:")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("ctrl+c stop")
        ser.close()
