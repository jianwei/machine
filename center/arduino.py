#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# from asyncio.log import logger
# from distutils.log import error
import sys
import os
from utils.redis_message_queue import RMQ
from utils.log import log
from utils.arduino import arduino
sys.path.append("..")
from redisConn.index import redisDB


class arduinoScript():
    def __init__(self):
        self.pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
        self.ret_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino_ret')
        self.ser = arduino()
        self.l = log("./arduino.log")
        self.logger = self.l.getLogger()
       

    # {"uuid": "0ddbb5f8-1b68-11ed-af17-57a903635f20", "cmd": "RST ."}'
    # begin_time:1661395309.6998177
    # 1661395409.5343091  
    def send_cmd(self, message):
        self.ser.send_cmd(message)
        

    def get_ret(self):
        ret = self.ser.get_ret()
        print(ret)
        pass

    def run_subscribe(self):
        self.pub_rmq.run_subscribe(self)
    
    def open_camera(self):
        print ("---------------------------------------open camera--------------------------------------")
        cmd = "cd ../StrongSORT/ && python3 track.py --source 0  &"
        os.system(cmd)
        pass


if __name__ == '__main__':
    redis = redisDB()
    redis.set("global_angle", 90)
    a = arduinoScript()
    # a.open_camera()
    a.run_subscribe()
