#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# from asyncio.log import logger
# from distutils.log import error

import json
import sys
# from tkinter.messagebox import NO
import serial
import time
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
        self.l = log()
        self.logger = self.l.getLogger()
        self.timeout = 0.005
        self.ser = serial.Serial(port=port,timeout=0, baudrate=9600)
        #触发复位
        self.ser.write("default.".encode())  
        time.sleep(1)

    # {'queue': 'arduino', 'message': '{"uuid": "0ddbb5f8-1b68-11ed-af17-57a903635f20", "cmd": "RST ."}', 'time': '2022-08-14 08:28:44'}
    def send_cmd(self, message):
        ret = -2
        # message = json.loads(msg)
        if ("cmd" in message.keys()):
            cmd = message["cmd"]
        else:
            self.logger.info("Lost message:%s", message)
        uuid = message["uuid"]
        # self.logger.info("send_cmd:uuid:%s,cmd:%s,ret:%s",uuid,cmd,ret)
        self.ser.write(cmd.encode())
        cnt = 0
        try:
            while True:
                time.sleep(0.1)
                # long_cmd_arr = ["TL","TR"]
                # if(cmd.split()[0] in long_cmd_arr):
                #     self.ser.timeout = 0.5
                # else:
                #     self.ser.timeout=self.timeout
                
                cnt += 1
                print("---------------------read,cmd:",cmd, "--------------------", cnt,cmd.split())
                time1 = float(time.time())
                # self.ser.write(cmd.encode())
                response = self.ser.readall()
                # response = self.ser.read(10)


                # tdata = self.ser.read() 
                # data_left = self.ser.inWaiting()  
                # print("data_left,tdata",data_left,tdata)



                print("---------------------response:",
                    response, "-----------------------")
                time2 = float(time.time())
                diff = time2-time1
                if (response):
                    response_arr = response.splitlines()
                    ret = response_arr[len(
                        response_arr)-1].decode("UTF-8") if len(response_arr) > 0 else ""
                    self.logger.info(
                        "send_cmd:uuid:%s,cmd:%s,ret:%s,difftime:%s", uuid, cmd, ret, diff)
                    self.send_ret(ret)
                    return ret
        except Exception as e:
            self.l.logError("serial连接或者执行失败,reason:")

    def send_ret(self, ret):
        self.ret_rmq.publish(ret)
        pass

    def run_subscribe(self):
        self.pub_rmq.run_subscribe(self)


if __name__ == '__main__':
    redis = redisDB()
    redis.set("global_angle", 0)
    a = arduino()
    a.run_subscribe()
