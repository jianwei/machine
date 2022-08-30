#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils.serial_control import serial_control
ser =  serial_control()


def main():
    cmd = "MF 10."
    ser.send_cmd(cmd.encode())
    print(ser.get_ret())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("ctrl+c stop")
        ser.close()
