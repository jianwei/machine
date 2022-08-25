#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


from redis import Redis, ConnectionPool
import time
import os
import json
import numpy
import sys
sys.path.append("..")
from redisConn.index import redisDB


class RMQ(object):

    def __init__(self, url, name):
        # self.client = Redis(host=url)
        pool = ConnectionPool.from_url(url=url, decode_responses=True)
        self.client = Redis(connection_pool=pool)
        self.queue_name = name
        self.redis = redisDB()
        # global_angle = self.redis.

        # l = log()
        # self.logger = l.getLogger()

    def publish(self, data):
        """ 发布 """
        self.client.publish(self.queue_name, data)
        return True

    def subscribe(self):
        """ 订阅 """
        pub = self.client.pubsub()
        pub.subscribe(self.queue_name)
        return pub

    # {'queue': 'arduino', 'message': '{"uuid": "0ddbb5f8-1b68-11ed-af17-57a903635f20", "cmd": "RST ."}', 'time': '2022-08-14 08:28:44'}
    def run_subscribe(self, that):
        """ 启动订阅 """
        pub = self.subscribe()
        while True:
            _, queue_name, message = pub.parse_response()
            if _ == 'subscribe':
                print('... 队列启动，开始接受消息 ...')
                continue
            data = {'queue': queue_name, 'message': message,
                    "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
            print("------------------------------------------------------------------------------------")
            that.logger.info("run_subscribe--data:%s",data)
            # print(data)
            # continue
            if (that):
                obj_msg  = json.loads(message)
                if ("xbox" in obj_msg.keys()):
                    cmd = self.xbox(obj_msg)
                    print("cmd2:", cmd)
                    if (cmd):
                        # message = json.loads(message)
                        obj_msg["cmd"] = cmd+"."
                that.send_cmd(obj_msg)
                if("next_cmd" in obj_msg.keys()):
                    next_cmd = obj_msg["next_cmd"]
                    # print ("next_cmd-----------------:",next_cmd)
                    for item in next_cmd:
                        # print ("item-----------------:",item)
                        # parent_cmd = obj_msg[""]
                        cmd = item["cmd"] +"."
                        sleep = int(item["sleep"])
                        print ("cmd,sleep-----------------:",cmd,sleep)
                        
                        if (sleep>0):
                            time.sleep(sleep)
                            msg ={
                                "uuid": obj_msg["uuid"],
                                "cmd": cmd,
                                "from": "camera->next",
                            } 
                        that.send_cmd(msg)   





    def turn(self, angle, type):
        angle = int(angle)
        global_angle = int(self.redis.get("global_angle"))
        ret = (90-angle) if type == 1 else (90+angle)
        print("global_angle,ret,angle, type:",global_angle,ret,angle, type)

        if (global_angle == 0):
            if (type == 1):
                global_angle = 90-angle
            elif (type == 2):
                global_angle = 90+angle
            self.redis.set("global_angle", global_angle)
        cmd = ""
        if (type ==1):  # y<0 x>0
            self.redis.set("global_angle",90-angle)
            if(global_angle>90):
                turn_angle = global_angle-90+angle
                cmd = "TR "+ str(turn_angle)
            else:
                if((90-global_angle)>angle):
                    cmd = "TL "+ str((90-global_angle)-angle)
                else:
                    cmd = "TR "+ str(abs((90-global_angle)-angle))
        elif (type==2) : #y<0 x<0
            self.redis.set("global_angle",90+angle)
            if(global_angle<90):
                cmd = "TL "+ str(abs(angle+(90-global_angle)))
            else:
                if(global_angle>(90+angle)):
                    cmd = "TR "+ str(abs(global_angle-angle-90))
                else:
                    cmd = "TL "+ str(abs(global_angle-angle-90))
        return cmd

    def xbox(self, message):
        # message = json.loads(message)
        msgObj = message["xbox"]
        # print("msgObj",msgObj)
        cmd = ""
        cache_status = self.redis.get("begin_work")
        print("cache_status:",cache_status)
        if (str(cache_status)=="0" or cache_status==None):
            # 后退
            if int(msgObj["RY"]) > 0:
                val = int(int(abs(msgObj["RY"]))/32767 * 255)
                val = val if val>=40 else 40
                val = val if val<=150 else 150
                cmd = "MB "+str(val)

            
            # 前进
            elif int(msgObj["RY"]) < 0:
                val = int(int(abs(msgObj["RY"]))/32767 * 255)
                val = val if val>=40 else 40
                val = val if val<=150 else 150
                cmd = "MF "+str(val)

            
            elif (int(abs(msgObj["LY"]))==32767 or int(abs(msgObj["LX"]))==32767 ):
                # 左转
                if (int(msgObj["LY"]) < 0 and int(msgObj["LX"]) < 0):
                    x = abs(int(msgObj["LX"]))
                    y = abs(int(msgObj["LY"]))
                    angle = int(numpy.arctan(x/y) * 180.0 / 3.1415926)
                    cmd = self.turn(angle, 2)

                # 右转
                elif int(msgObj["LY"]) < 0 and int(msgObj["LX"]) > 0:
                    x = abs(int(msgObj["LX"]))
                    y = abs(int(msgObj["LY"]))
                    angle = int(numpy.arctan(x/y) * 180.0 / 3.1415926)
                    cmd = self.turn(angle, 1)
                
                print("cmd1:",cmd)
                if (cmd and str(cmd.split()[1])=="0"):
                    cmd = ""

            #上
            elif int(msgObj["YY"]) < 0:
                cmd = "MU"
            
            #下
            elif int(msgObj["YY"]) > 0:
                cmd = "MD"

            # 左右
            elif int(msgObj["XX"]) > 0:
                cmd = "MR 10"
            
            # 复位
            elif int(msgObj["A"]) > 0:
                cmd = "RST"
                self.redis.set("global_angle", 0)

            # 开机准备走路
            elif int(msgObj["X"]) > 0:
                cmd = "TL 90"

        # 2操作臂停止
        if int(msgObj["B"]) > 0:
            cmd = "STOP 2"

        # 机器停止
        elif int(msgObj["Y"]) > 0:
            cmd = "STOP 0"
        
        # 2开始或者关闭工作
        elif int(msgObj["RB"]) > 0:
            cache_status = self.redis.get("begin_work")
            # print("cache_status:", cache_status)
            if (cache_status and int(cache_status) == 0):
                self.redis.set("begin_work", 1)
                # self.open_camera()
            else:
                self.redis.set("begin_work", 0)

        # 复位
        
        # elif (msgObj["LB"]>0):

        return cmd


