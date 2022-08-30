#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import os
from utils.redis_message_queue import RMQ
from utils.log import log
from utils.serial_control import serial_control
from pathlib import Path

path = str(Path(__file__).resolve().parents[1])
sys.path.append(path)
from redisConn.index import redisDB

class arduino():
    def __init__(self):
        self.pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
        self.ret_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino_ret')
        self.ser = serial_control()
        self.l = log("./arduino.log")
        self.logger = self.l.getLogger()



    def send_cmd(self, message):
        # self.ser.send_cmd(message)
        ser = serial_control()
        ser.send_cmd(message)
        ser.close()


    def get_ret(self):
        ret = self.ser.get_ret()
        print(ret)
        pass

    def run_subscribe(self):
        self.pub_rmq.run_subscribe(self)

    def open_camera(self):
        print("---------------------------------------open camera--------------------------------------")
        cmd = "cd ../StrongSORT/ && python3 track.py --source 0  &"
        os.system(cmd)
        pass


if __name__ == '__main__':
    redis = redisDB()
    redis.set("global_angle", 90)
    a = arduino()
    # a.open_camera()
    a.run_subscribe()
