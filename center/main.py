# from convertPoints import ConvertPoints
from utils.redis_message_queue import RMQ
import time
import os
import sys
import json
import uuid
# import serial
from utils.speed import speed
from utils.point import point
from utils.line import line
from utils.work import work
sys.path.append("..")
from redisConn.index import redisDB
# chmod -R 777 /dev/ttyAMA0
# import serial,sys,os,redis,time


class machine ():
    def __init__(self):
        self.redis = redisDB()
        # self.default_speed = 10
        self.pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
        self.point = point()
        self.speed = speed(self.point)
        self.line = line(self.point)
        self.work = work(self.point, self.speed)
        self.angle_distance = 5  # cm
        # self.ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
        # self.convertPoints = ConvertPoints()

    def send_cmd(self, cmd):
        cmd +="."
        cmd_dict = {
            "uuid": str(uuid.uuid1()),
            "cmd": cmd,
            "from":"weeding"
        }
        print("cmd:",cmd_dict)
        self.pub_rmq.publish(json.dumps(cmd_dict))
        # response = self.ser.readall() #read a string from port

    def loop(self):
        # mock = [
        #     [
        #         #  {'point': [[110, 145], [230, 145], [110, 165], [230, 165]], 'id': 1, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         #  {'point': [[410, 145], [530, 145], [410, 165], [530, 165]], 'id': 2, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         #  {'point': [[800, 145], [930, 145], [800, 165], [930, 165]], 'id': 3, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         #  {'point': [[110, 345], [230, 345], [110, 365], [230, 365]], 'id': 4, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         #  {'point': [[410, 345], [530, 345], [410, 365], [530, 365]], 'id': 5, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         #  {'point': [[800, 345], [930, 345], [800, 365], [930, 365]], 'id': 6, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         #  {'point': [[110, 645], [230, 645], [110, 715], [230, 715]], 'id': 7, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         #  {'point': [[410, 645], [530, 645], [410, 715], [530, 715]], 'id': 8, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
        #         {'point': [[800, 645], [930, 645], [800, 715], [930, 715]], 'id': 9,'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]}
        #     ],
        # ]
        # print(mock)
        currentTime = 0
        while (1):
            print("----------------------loop begin ------------------------------")
            allPhoto = self.redis.get("allPoints")
            # global_angle = self.redis.get("global_angle")
            # global_angle = int(global_angle) if global_angle else 0
            global_angle = 90
            # allPhoto = json.dumps(mock)
            # flag = self.redis.get("begin_work")
            work_flag = 1
            if (work_flag and int(work_flag) == 1):
                if (allPhoto):
                    allPhoto = json.loads(allPhoto)
                    # print("allPhoto",allPhoto)
                    if(len(allPhoto)>0):
                        latsTime = allPhoto[0][0]["time"]
                        screenSize = allPhoto[0][0]["screenSize"]
                        if (latsTime == currentTime):
                            print("current latsTime:", latsTime, ",loop!")
                            time.sleep(0.1)
                            continue
                        currentTime = latsTime
                        speed = self.speed.getSpeed(allPhoto)
                        self.redis.set("speed", speed)
                        print("speed:", speed)
                        # 稳定速度 转速
                        # revolution = self.speed.uniformSpeed(speed)
                        # 分行 工作
                        line = self.line.convertLine(allPhoto)
                        # print(line)
                        # for item in line:
                        #     print("item:",item)

                        # if (line and line[0]):
                        #     length = len(line[0])
                        #     y = line[length-1][0]["centery"]
                        #     print(123, length, y)
                        #     if (y >= 650 and y <= 720):
                        #         # work
                        #         workcmd = self.work.work(line)
                        #         if (len(workcmd) > 0):
                        #             self.send_cmd(workcmd)
                        # 左右位置调整
                        print("line",line)
                        if (line and len(line) > 0):
                            center_point = screenSize[0]/2
                            diff_point = 20   #误差
                            diff_angle = 10   #每次的旋转角度
                            first = line[0]
                            length = len(first)
                            cmd = ""
                            if (length > 0):
                                if (length == 1 or length == 3):
                                    center = first[0] if length == 1 else first[1]
                                    centerx = center["centerx"]
                                    print("centerx------------+++++++++",centerx,center_point)
                                    if (centerx < (center_point-diff_point)):
                                        flag = "TL"
                                        global_angle += diff_angle
                                        cmd = str(flag)+" "+str(10)
                                    elif (centerx > (center_point+diff_point)):
                                        flag = "TR"
                                        global_angle += diff_angle
                                        cmd = flag+" "+str(10)
                                    else:
                                        if (global_angle != 90):
                                            diffangle = global_angle - 90
                                            flag = "TR" if diffangle > 0 else "TL"
                                            cmd = flag+" "+str(abs(diffangle))+"."
                                if (len(cmd) > 0):
                                    self.redis.set("global_angle", global_angle)
                                    self.send_cmd(cmd)
                else:
                    revolution = self.speed.revolution
            else:
                self.redis.set("allPoints", json.dumps([]))
            print("time:", time.time(), ",begin_work:", work_flag)
            print("----------------------loop end ------------------------------")
            time.sleep(1)
        pass


if __name__ == "__main__":
    m = machine()
    try:
        m.loop()
    except KeyboardInterrupt:
        print("ctrl+c stop")
        redis = redisDB()
        redis.set("allPoints", json.dumps([]))
        m.send_cmd("STOP 0")
