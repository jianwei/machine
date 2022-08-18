# from convertPoints import ConvertPoints

from utils.redis_message_queue import RMQ
import time
import os
import sys
import json
import uuid
import numpy
# import serial
from utils.speed import speed
from utils.point import point
from utils.line import line
from utils.work import work
from utils.log import log
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
        self.l = log("main.log")
        self.logger = self.l.getLogger()
        # self.ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
        # self.convertPoints = ConvertPoints()

    def send_cmd(self, cmd):
        if(cmd!=""):
            cmd += "."
            cmd_dict = {
                "uuid": str(uuid.uuid1()),
                "cmd": cmd,
                "from": "camera"
            }
            self.logger.info("send_cmd-cmd:%s", cmd_dict)
            self.pub_rmq.publish(json.dumps(cmd_dict))
        else:
            self.logger.info("cmd null")
        # response = self.ser.readall() #read a string from port

    def loop(self):
        mock = [
            [
                #  {'point': [[110, 145], [230, 145], [110, 165], [230, 165]], 'id': 1, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[410, 145], [530, 145], [410, 165], [530, 165]], 'id': 2, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[800, 145], [930, 145], [800, 165], [930, 165]], 'id': 3, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[110, 345], [230, 345], [110, 365], [230, 365]], 'id': 4, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[410, 345], [530, 345], [410, 365], [530, 365]], 'id': 5, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[800, 345], [930, 345], [800, 365], [930, 365]], 'id': 6, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[110, 645], [230, 645], [110, 715], [230, 715]], 'id': 7, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[410, 645], [530, 645], [410, 715], [530, 715]], 'id': 8, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                # {'point': [[200, 645], [330, 645], [200, 715], [330, 715]], 'id': 9,'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]}
                {"point": [[736, 0], [959, 0], [736, 548], [959, 548]], "id": 182, "name": "person", "time": 1660786075.6786768, "screenSize": [1080, 720], "center": [847.5, 274.0], "centerx": 847.5, "centery": 274.0}
            ],
        ]
        # print(mock)
        currentTime = 0
        while (1):
            self.logger.info("----------------------loop begin ------------------------------")
            allPhoto = self.redis.get("allPoints")
            global_angle = self.redis.get("global_angle")
            global_angle = int(global_angle) if global_angle else 90
            # allPhoto = json.dumps(mock)
            # work_flag = self.redis.get("begin_work")
            # self.logger.info(allPhoto)
            work_flag = 1
            if (work_flag and int(work_flag) == 1):
                if (allPhoto):
                    allPhoto = json.loads(allPhoto)
                    if (len(allPhoto) > 0):
                        latsTime = allPhoto[0][0]["time"]
                        screenSize = allPhoto[0][0]["screenSize"]
                        if (latsTime == currentTime):
                            self.logger.info("current latsTime:%s,loop",latsTime )
                            time.sleep(0.1)
                            continue
                        currentTime = latsTime
                        speed = self.speed.getSpeed(allPhoto)
                        self.redis.set("speed", speed)
                        self.logger.info("speed:%s", speed)
                        # 稳定速度 转速
                        revolution = self.speed.uniformSpeed(speed)
                        self.go(revolution)
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
                        self.logger.info("line:%s", json.dumps(line))
                        if (line and len(line) > 0):
                            center_point = screenSize[0]/2
                            diff_point = 20  # 误差
                            diff_angle = 10  # 每次的旋转角度
                            first = line[0]
                            length = len(first)
                            cmd = ""
                            if (length > 0):
                                if (length == 1 or length == 3):
                                    center = first[0] if length == 1 else first[1]
                                    centerx = center["centerx"]
                                    diff_point_x = centerx-center_point

                                    self.point.setScreenSize(screenSize)
                                    x= self.point.sizexm(abs(diff_point_x))
                                    tan = x/(1000*self.point.f)
                                    angle = int(numpy.arctan(tan) * 180.0 / 3.1415926)

                                    print("angle,tan,x,diff_point_x,centerx,center_point:",angle,tan,x,diff_point_x,centerx,center_point)

                                    cmd_prefix = ""
                                    target_angle = 90
                                    print("target_angle,global_angle0",target_angle,global_angle,centerx,center_point)
                                    if(global_angle<=90):
                                        if (centerx<=center_point) :
                                            print("target_angle,global_angle1",target_angle,global_angle,centerx,center_point)
                                            target_angle = 90-angle
                                            cmd_prefix = "TR" if global_angle<target_angle else "TL"
                                        else:
                                            print("target_angle,global_angle2",target_angle,global_angle,centerx,center_point)
                                            target_angle = 90+angle
                                            cmd_prefix = "TR"
                                    else:
                                        if (centerx<=center_point) :
                                            print("target_angle,global_angle3",target_angle,global_angle,centerx,center_point)
                                            target_angle = 90-angle
                                            cmd_prefix = "TR" if global_angle<target_angle else "TL"
                                        else:
                                            print("target_angle,global_angle4",target_angle,global_angle,centerx,center_point)
                                            target_angle = 90+angle
                                            cmd_prefix = "TL"
                                    print("target_angle,global_angle5",target_angle,global_angle)
                                    if(target_angle!=global_angle):
                                        cmd = cmd_prefix + " " + str(abs(target_angle-global_angle))
                                        global_angle = target_angle
                                        print ("send-cmd:",cmd)
                                    else:
                                        print ("send-cmd:none")
                                    # print("target_angle,global_angle2",target_angle,global_angle)
                                    self.redis.set("global_angle", global_angle)
                                    self.send_cmd(cmd)
                    else:
                        self.go(self.speed.revolution)
                else:
                    self.go(self.speed.revolution)
            else:
                self.redis.set("allPoints", json.dumps([]))
            self.logger.info("time:%s,begin_work:%s", time.time(), work_flag)
            self.logger.info("----------------------loop end ------------------------------")
            time.sleep(1)

    def go(self,revolution):
        # revolution = self.speed.revolution
        cmd = "MF "+str(revolution)
        self.send_cmd(cmd)



if __name__ == "__main__":
    m = machine()
    try:
        m.loop()
    except KeyboardInterrupt:
        print("ctrl+c stop")
        redis = redisDB()
        redis.set("allPoints", json.dumps([]))
        redis.set("global_angle", 90)
        m.send_cmd("STOP 0")
