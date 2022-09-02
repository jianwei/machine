#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# from asyncio.log import logger
# from distutils.log import error

import json
import serial
import time,termios
from utils.log import log



class serial_control():
    def __init__(self):
        port = "/dev/ttyACM0"  # Arduino端口
        self.l = log("./arduino.log")
        self.logger = self.l.getLogger()
        self.timeout = 0.005


        f = open(port)
        attrs = termios.tcgetattr(f)
        attrs[2] = attrs[2] & ~termios.HUPCL
        termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
        f.close()

        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = port
        self.ser.open()

        #触发复位
        self.ser.write("default.".encode())  
        time.sleep(1)

        
    def close(self):
        self.ser.close()

    # {"uuid": "0ddbb5f8-1b68-11ed-af17-57a903635f20", "cmd": "RST ."}'
    # begin_time:1661395309.6998177
    # 1661395409.5343091  
    def send_cmd(self, message):
        ret = -2
        # self.logger.info ("message:%s",message)
        if ("cmd" in message.keys()):
            cmd = message["cmd"]
        else:
            cmd = None
            self.logger.info("Lost message:%s", message)
        uuid = message["uuid"]
        # print("cmd:",cmd)
        if (cmd):
            self.logger.info("cmd:%s,begin_time:%s",cmd,time.time())
            self.ser.write(cmd.encode())
            self.logger.info("cmd:end write:%s",time.time())
            try:
                cnt=1
                ret_all = ""
                time0 = time.time()
                while True:
                    cnt+=1
                    time1 = float(time.time())
                    response = self.ser.read()
                    time2 = float(time.time())
                    diff = time2-time1
                    if (response):
                        ret_all += str(response,"UTF-8")
                        response_arr = ret_all.splitlines()
                        ret = response_arr[len(response_arr)-1] if len(response_arr) > 0 else ""
                        self.logger.info("1--cnt:%s,send_cmd:uuid:%s,cmd:%s,ret:%s,difftime:%s,response:%s",cnt, uuid, cmd, ret, diff,ret_all)
                        # time.sleep(0.1)

                        if(str(ret)=="0"): 
                            self.logger.info("send_cmd:uuid:%s,cmd:%s,ret:%s,difftime:%s,response:%s", uuid, cmd, ret, diff,ret_all)
                            ret_dict = {
                                "uuid":uuid,
                                "retsult":ret
                            }
                            # self.send_ret(ret)
                            # self.get_ret(json.dumps(ret_dict))
                            self.ret_dict = ret_dict
                            self.logger.info("cmd:%s,end_time:%s",cmd,time.time())
                            return ret
                        time3 = time.time()
                        if(time3-time0>=1):
                            break
            except Exception as e:
                self.l.logError("serial连接或者执行失败,reason:",e)

    def get_ret(self):
        print("ret_dict:",self.ret_dict)
        return self.ret_dict


