#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# from asyncio.log import logger
# from distutils.log import error

import json
import sys
# from tkinter.messagebox import NO
import serial
import time
import os
from utils.redis_message_queue import RMQ
from utils.log import log
sys.path.append("..")
from redisConn.index import redisDB


class arduino():
    def __init__(self):
        self.pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
        self.ret_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino_ret')
        # port = "/dev/ttyACM0"  # Arduino端口
        # port = "/dev/tty.usbmodem14101"  # Arduino端口
        # port = "/dev/tty.usbmodem14201"  # Arduino端口

        port = "/dev/ttyACM0"  # Arduino端口
        self.l = log("./arduino.log")
        self.logger = self.l.getLogger()
        self.timeout = 0.005
        self.ser = serial.Serial(port=port,timeout=0, baudrate=9600)
        #触发复位
        self.ser.write("default.".encode())  
        time.sleep(1)

    # {"uuid": "0ddbb5f8-1b68-11ed-af17-57a903635f20", "cmd": "RST ."}'
    def send_cmd(self, message):
        ret = -2
        if ("cmd" in message.keys()):
            cmd = message["cmd"]
        else:
            self.logger.info("Lost message:%s", message)
        uuid = message["uuid"]
        print("cmd:",cmd)
        self.ser.write(cmd.encode())

        try:
            cnt=1
            ret_all = ""
            while True:
                cnt+=1
                time1 = float(time.time())
                response = self.ser.readall()
                print("response:",response)
                time2 = float(time.time())
                diff = time2-time1
                if (response):
                    ret_all += str(response,"UTF-8")
                    response_arr = ret_all.splitlines()
                    ret = response_arr[len(response_arr)-1] if len(response_arr) > 0 else ""
                    self.logger.info("1--cnt:%s,send_cmd:uuid:%s,cmd:%s,ret:%s,difftime:%s,response:%s",cnt, uuid, cmd, ret, diff,ret_all)

                    if(str(ret)=="0"):
                        self.logger.info("2--cnt:%s,send_cmd:uuid:%s,cmd:%s,ret:%s,difftime:%s,response:%s",cnt, uuid, cmd, ret, diff,ret_all)
                        ret_dict = {
                            "uuid":uuid,
                            "retsult":ret
                        }
                        # self.send_ret(ret)
                        self.send_ret(json.dumps(ret_dict))
                        return ret
        except Exception as e:
            self.l.logError("serial连接或者执行失败,reason:")

    def send_ret(self, ret_dict):
        self.ret_rmq.publish(ret_dict)
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
    a = arduino()
    # a.open_camera()
    a.run_subscribe()
