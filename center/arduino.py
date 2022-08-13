#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import serial
from utils.redis_message_queue import RMQ


class arduino():
    def __init__(self):
        self.pub_rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')
        self.ret_rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino_ret')
        # port = "/dev/ttyACM0"  # Arduino端口
        # port = "/dev/tty.usbmodem14101"  # Arduino端口
        # port = "/dev/tty.usbmodem14201"  # Arduino端口
        port = "/dev/ttyACM0"  # Arduino端口
        self.ser = serial.Serial(
            port, 9600, timeout=1, dsrdtr=False)  # 设置端口，每秒回复一个信息

    def send_cmd(self,cmd):
        ret = -2
        try:
            while True:
                self.ser.write(cmd.encode())
                response = self.ser.readall()
                if (response):
                    response_arr = response.splitlines()
                    ret = response_arr[len(response_arr)-1].decode("UTF-8") if len(response_arr) > 0 else ""
                    break
        except Exception as e:
            print("serial连接或者执行失败,reason:", e)
            self.ser.close()
        print(response, ret)
        self.send_ret(ret)
        return ret
    
    def send_ret(self,ret):
        self.ret_rmq.publish(ret)
        pass

    def run_subscribe(self):
        self.pub_rmq.run_subscribe(self)


if __name__ == '__main__':
    a = arduino()
    a.run_subscribe()

    
