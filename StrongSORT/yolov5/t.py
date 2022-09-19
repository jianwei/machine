#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# from time import time
import uuid
import time
import serial
import termios
import re
from utils.serial_control import serial_control
from utils.log import log
ser = serial_control()

def main(cmd):
    cmd_dict = {
        "uuid": str(uuid.uuid1()),
        "cmd": cmd,
        "from": "camera",
    }
    ser.send_cmd(cmd_dict)
    print(ser.get_ret())



if __name__ == "__main__":
    try:
        main("STOP 0.")
    except KeyboardInterrupt:
        print("ctrl+c stop")
        ser.close()

