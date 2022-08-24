# from convertPoints import ConvertPoints

from utils.redis_message_queue import RMQ
import time
import os
import sys
import json
import uuid
import numpy
# from threading import Timer
import threading
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




mainlog = log("main.log")
main_logger = mainlog.getLogger()
main_pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')


def send(cmd):
    if(cmd!=""):
        cmd += "."
        cmd_dict = {
            "uuid": str(uuid.uuid1()),
            "cmd": cmd,
            "from": "camera"
        }
        main_logger.info("end_cmd-cmd:%s", cmd_dict)
        main_pub_rmq.publish(json.dumps(cmd_dict))
    else:
        main_logger.info("cmd null")


def send_wheel_cmd(cmd):
    send(cmd)
    send("MF 40")

def setTimeout(cbname,delay,*argments):
    threading.Timer(delay,cbname,argments).start()


def wheel():
    send("STOP 1")
    send("ROT 255")
    min_time = 1.225  # 1秒 1.225圈
    unit = 1/min_time  # 1圈  unit 秒
    setTimeout(send_wheel_cmd,unit,"STOP 3")
    

class machine ():
    def __init__(self):
        self.redis = redisDB()
        # self.default_speed = 10
        # self.pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
        self.pub_rmq = main_pub_rmq
        self.point = point()
        self.speed = speed(self.point)
        self.line = line(self.point)
        # self.l = log("main.log")
        self.work = work(self.point, self.speed,main_logger)
        self.angle_distance = 5  # cm
        
        self.logger = main_logger
        # self.ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
        # self.convertPoints = ConvertPoints()

    def send_cmd(self, cmd):
        send(cmd)

    def loop(self):
        mock = [
            [
                {"point": [[470, 466], [550, 466], [470, 626], [550, 626]], "id": 2, "name": "bottle", "time": 1661318695.8770459, "screenSize": [1080, 720], "uuid": "16c50720-236d-11ed-929a-1cbfc0958bef", "centerx": 510.0, "centery": 546.0, "center": [510.0, 546.0]},
                #  {'point': [[110, 145], [230, 145], [110, 165], [230, 165]], 'id': 1, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[410, 145], [530, 145], [410, 165], [530, 165]], 'id': 2, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[800, 145], [930, 145], [800, 165], [930, 165]], 'id': 3, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[110, 345], [230, 345], [110, 365], [230, 365]], 'id': 4, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[410, 345], [530, 345], [410, 365], [530, 365]], 'id': 5, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[800, 345], [930, 345], [800, 365], [930, 365]], 'id': 6, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[110, 645], [230, 645], [110, 715], [230, 715]], 'id': 7, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                #  {'point': [[410, 645], [530, 645], [410, 715], [530, 715]], 'id': 8, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]},
                # {'point': [[200, 645], [330, 645], [200, 715], [330, 715]], 'id': 9,'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]}
                {"point": [[736, 0], [959, 0], [736, 548], [959, 548]], "id": 182, "name": "person", "time": 1660786080.6786768, "screenSize": [1080, 720],"center":[847.5,274],"centerx":847.5,"centery":274},
                {"point": [[736, 650], [959, 650], [736, 710], [959, 710]], "id": 182, "name": "person", "time": 1660786080.6786768, "screenSize": [1080, 720],"center":[847.5,660],"centerx":847.5,"centery":660}
            ],
            [
                {"point": [[736, 10], [959, 10], [736, 558], [959, 558]], "id": 182, "name": "person", "time": 1660786079.6786768, "screenSize": [1080, 720],"center":[847.5,284],"centerx":847.5,"centery":284},
                {"point": [[736, 660], [959, 660], [736, 720], [959, 720]], "id": 182, "name": "person", "time": 1660786079.6786768, "screenSize": [1080, 720],"center":[847.5,670],"centerx":847.5,"centery":670}
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
                            # continue
                        currentTime = latsTime
                        machine_speed = self.speed.getSpeed(allPhoto)
                        self.logger.info("machine_speed:%s", machine_speed)
                        # 稳定速度 转速
                        revolution = self.speed.uniformSpeed(machine_speed)
                        self.logger.info("revolution:%s", revolution)
                        self.go(revolution)
                        # 分行 工作
                        line = self.line.convertLine(allPhoto,0)

                        
                        if (line and line[0]):
                            lastLine  =  len (line)
                            y = line[lastLine-1][0]["centery"]
                            uuid_id = line[lastLine-1][0]["id"]
                            if (self.redis.get(uuid_id)==str(1)) :
                                self.logger.info("id 存在,1分钟内不重复处理:%s", uuid_id,self.redis.get(uuid_id),self.redis.get(uuid_id)==str(1))
                            else:
                                self.redis.set(uuid_id,1,1*60)
                                # if (y >= 650 and y <= 720):
                                if (y >= 540 and y <= 720):
                                    workcmd = self.work.work(line,machine_speed)
                                    if (len(workcmd) > 0):
                                        wheel()
                                else:
                                    self.logger.info("------id,centery:%s,%s", uuid_id,y)
                        # 左右位置调整
                        self.logger.info("line:%s", json.dumps(line))
                        if (line and len(line) > 0):
                            center_point = screenSize[0]/2
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

                                    # print("angle,tan,x,diff_point_x,centerx,center_point:",angle,tan,x,diff_point_x,centerx,center_point)

                                    cmd_prefix = ""
                                    target_angle = 90
                                    if(global_angle<=90):
                                        if (centerx<=center_point) :
                                            target_angle = 90-angle
                                            cmd_prefix = "TR" if global_angle<target_angle else "TL"
                                        else:
                                            target_angle = 90+angle
                                            cmd_prefix = "TR"
                                    else:
                                        if (centerx<=center_point) :
                                            target_angle = 90-angle
                                            cmd_prefix = "TL"
                                        else:
                                            target_angle = 90+angle
                                            cmd_prefix = "TR" if global_angle<target_angle else "TL"
                                    # print("target_angle,global_angle5",target_angle,global_angle)
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
