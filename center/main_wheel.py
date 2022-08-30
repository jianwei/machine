# from convertPoints import ConvertPoints

# from math import fabs
from utils.redis_message_queue import RMQ
import time
import os
import sys
import json
import uuid
import numpy
import random
from utils.speed import speed
from utils.point import point
from utils.line import line
from utils.work import work
from utils.log import log
from utils.serial_control import serial_control


from pathlib import Path
path = str(Path(__file__).resolve().parents[1])
sys.path.append(path)
from redisConn.index import redisDB





mainlog = log("main.log")
main_logger = mainlog.getLogger()
main_pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
redis = redisDB()
redis.set("is_working",0)
ser =  serial_control()
# is_working = False

def send(cmd):
    if(cmd!=""):
        cmd += "."
        cmd_dict = {
            "uuid": str(uuid.uuid1()),
            "cmd": cmd,
            "from": "camera",
        }
        ser.send_cmd(cmd_dict)
    else:
        main_logger.info("cmd null")



def wheel(speed):
    rot_speed = 60
    unit_sleep = 1/(rot_speed*50/2/1000)   #转1圈所需要的时间
    unit_sleep += 0.02    #误差
    print("unit_sleep",unit_sleep)

    send("STOP 0")
    send("MD")
    time.sleep(2)
    send("STOP 2")
    send("RROT "+str(rot_speed))
    time.sleep(unit_sleep)
    send("STOP 2")
    send("MU")
    time.sleep(2)
    send("STOP 2")
    redis.set("is_working",0)
    send("MF "+str(speed))

    

class machine ():
    def __init__(self):
        self.redis = redisDB()
        self.pub_rmq = main_pub_rmq
        self.point = point()
        self.speed = speed(self.point)
        self.line = line(self.point)
        self.work = work(self.point, self.speed,main_logger)
        self.angle_distance = 5  # cm
        self.logger = main_logger


    def send_cmd(self, cmd):
        send(cmd)

    def loop(self):
        randId = random.random()
        mock = [
                [{"point":[[1,140],[129,140],[1,440],[129,440]],"id":0,"name":"person","time":1661850838.4855962,"screenSize":[640,480],"centerx":65.0,"centery":290.0,"center":[65.0,290.0]}],
                [{"point":[[1,35],[187,35],[1,449],[187,449]],"id":0,"name":"person","time":1661850838.4098039,"screenSize":[640,480],"centerx":94.0,"centery":242.0,"center":[94.0,242.0]}]
               ]
        # {"point": [[302, 221], [434, 221], [302, 378], [434, 378]], "id": 229, "name": "cup", "time": 1661393590.437084, "screenSize": [1080, 720], "centerx": 368.0, "centery": 299.5, "center": [368.0, 299.5]}
        # print(mock)
        currentTime = 0
        # global is_working
        is_working = self.redis.get("is_working")
        a=0
        while (1):
            a+=1
            self.logger.info("----------------------loop begin ------------------------------%s",a)
            allPhoto = self.redis.get("navigation_points")
            global_angle = self.redis.get("global_angle")
            global_angle = int(global_angle) if global_angle else 90
            self.logger.info("is_working:%s", is_working)
            allPhoto = json.dumps(mock)
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
                       
                        if (is_working==0 or is_working=="0"):
                            
                            revolution = self.speed.uniformSpeed(machine_speed)
                            self.logger.info("revolution:%s", revolution)
                            # if(revolution>=40)
                            revolution = 40 if revolution>=40 else revolution
                            self.go(revolution)
                        
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
