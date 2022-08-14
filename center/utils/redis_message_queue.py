#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from redis import Redis, ConnectionPool
import time,os,json,numpy,sys
sys.path.append("..")
from redisConn.index import redisDB


class RMQ(object):

    def __init__(self, url, name):
        # self.client = Redis(host=url)
        pool = ConnectionPool.from_url(url=url, decode_responses=True)
        self.client = Redis(connection_pool=pool)
        self.queue_name = name
        self.redis = redisDB()

        
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
            that.logger.info("run_subscribe--data:%s",data)
            # print(data)
            if (that):
                if ("xbox" in json.loads(message).keys()):
                    cmd = self.xbox(message)
                    print("cmd:", cmd)
                    if (cmd):
                        message = json.loads(message)
                        message["cmd"] = cmd+"."
                        # that.send_cmd(message)

    def xbox(self, message):
        message = json.loads(message)
        msgObj = json.loads(message["xbox"])
        cmd = ""
        # 前进
        if int(msgObj["RY"]) > 0:
            val = int(int(abs(msgObj["RY"]))/32767 * 255)
            cmd = "MF "+str(val)

        # 后退
        elif int(msgObj["RY"]) < 0:
            val = int(int(abs(msgObj["RY"]))/32767 * 255)
            cmd = "MB "+str(val)

        # 左转
        elif int(msgObj["LY"]) < 0 and int(msgObj["LX"]) < 0:
            x = abs(int(msgObj["LX"]))
            y = abs(int(msgObj["LY"]))
            angle = int(numpy.arctan(x/y) * 180.0 / 3.1415926)
            # print("-------------------------------------------------------")
            # print("z:----", x, y)
            # print("angle----", angle)
            # print("-------------------------------------------------------")
            cmd = "TL " + str(angle)

        # 右转
        elif int(msgObj["LY"]) < 0 and int(msgObj["LX"]) > 0:
            x = abs(int(msgObj["LX"]))
            y = abs(int(msgObj["LY"]))
            angle = int(numpy.arctan(x/y) * 180.0 / 3.1415926)
            # print("-------------------------------------------------------")
            # print("z:----", x, y)
            # print("angle----", angle)
            # print("-------------------------------------------------------")
            cmd = "TR " + str(angle)

        # 上下
        elif int(msgObj["XX"]) < 0:
            cmd = "ML 10"

        # 左右
        elif int(msgObj["XX"]) > 0:
            cmd = "MR 10"
        
        # 2操作臂停止
        elif int(msgObj["B"]) > 0:
            cmd = "STOP 2"

        # 2操作臂停止
        elif int(msgObj["A"]) > 0:
            cmd = "RST"
        
        # 2开始或者关闭工作
        elif int(msgObj["RB"]) > 0:
            cache_status = self.redis.get("begin_work")
            print("cache_status:",cache_status)
            if (cache_status and int(cache_status)==0):
                self.redis.set("begin_work",1)
                self.open_camera()
            else:
                self.redis.set("begin_work",0)

        # 开机准备走路
        elif int(msgObj["X"]) > 0:
            cmd = "TL 90"
        return cmd

    def open_camera(self):
        # cmd = "cd ../../StrongSORT/ && python3 track.py --source 0  &" 
        # os.system(cmd)
        pass