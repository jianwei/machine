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

# is_working = False

def send(cmd):
    if(cmd!=""):
        cmd += "."
        cmd_dict = {
            "uuid": str(uuid.uuid1()),
            "cmd": cmd,
            "from": "camera",
        }
        ser =  serial_control()
        ser.send_cmd(cmd_dict)
        ser.close()
    else:
        main_logger.info("cmd null")



def wheel(speed):
    rot_speed = 60
    unit_sleep = 1/(rot_speed*50/2/1000)   #转1圈所需要的时间
    unit_sleep -= 0.04    #误差
    main_logger.info("unit_sleep:%s",unit_sleep)
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
        self.pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')


    def send_cmd(self, cmd):
        send(cmd)

    def loop(self):
        randId = random.random()
        mock = [
            [ 
                {"point": [[450, 311], [517, 311], [450, 393], [517, 393]], "id": 0, "name": "person", "time": 1662082814.425567, "screenSize": [640, 480], "centerx": 483.5, "centery": 352.0, "center": [483.5, 352.0]},
                {"point": [[450, 310], [522, 310], [450, 393], [522, 393]], "id": 0, "name": "person", "time": 1662082814.305369, "screenSize": [640, 480], "centerx": 486.0, "centery": 351.5, "center": [486.0, 351.5]}, 
                {"point": [[451, 311], [517, 311], [451, 393], [517, 393]], "id": 0, "name": "person", "time": 1662082814.0092382, "screenSize": [640, 480], "centerx": 484.0, "centery": 352.0, "center": [484.0, 352.0]} 
            ]
        ]
        

        # navigation_points
        # {"point": [[302, 221], [434, 221], [302, 378], [434, 378]], "id": 229, "name": "cup", "time": 1661393590.437084, "screenSize": [1080, 720], "centerx": 368.0, "centery": 299.5, "center": [368.0, 299.5]}
        # print(mock)
        currentTime = 0
        # global is_working
        is_working = self.redis.get("is_working")
        a=0
        while (1):
            a+=1
            self.logger.info("----------------------loop begin ------------------------------%s",a)
            allPhoto = self.redis.get("allPoints")
            # navigation_points = self.redis.get("navigation_points")
            global_angle = self.redis.get("global_angle")
            global_angle = int(global_angle) if global_angle else 90
            self.logger.info("is_working:%s", is_working)


            # allPhoto = json.dumps(mock)
            # navigation_points = json.dumps(navigation_points_mock)

            # work_flag = self.redis.get("begin_work")

            work_flag = 1
            
            
            if (work_flag and int(work_flag) == 1):
                if (allPhoto ):
                    allPhoto = json.loads(allPhoto)
                    # navigation_points = json.loads(navigation_points)
                    if (len(allPhoto) > 0 ):
                        # try :                         
                        #     latsTime = allPhoto[0][0]["time"]
                        #     screenSize = allPhoto[0][0]["screenSize"]
                        # except Exception as e :
                        #     latsTime = navigation_points[0][0]["time"]
                        #     screenSize = navigation_points[0][0]["screenSize"]
                        # if (latsTime == currentTime):
                        #     self.logger.info("current latsTime:%s,loop",latsTime )
                        #     time.sleep(0.1)
                        #     continue
                        # currentTime = latsTime

                        # machine_speed = self.speed.getSpeed(allPhoto)
                        # machine_speed = self.speed.getSpeed(navigation_points)
                        # self.logger.info("machine_speed:%s", machine_speed)
                        # self.logger.info("allPhoto:%s", allPhoto)
                         # 分行 工作
                        if (allPhoto):
                            line = self.line.convertLine(allPhoto,0)
                            if (line and line[0]):
                                # print(4)
                                lastLine  =  len (line)
                                y = line[lastLine-1][0]["centery"]
                                uuid_id = "vegetable-"+str(line[lastLine-1][0]["id"])
                                # if (self.redis.get(uuid_id)==str(1)) :
                                #     self.logger.info("id 存在,1分钟内不重复处理:%s,%s,%s", uuid_id,self.redis.get(uuid_id),self.redis.get(uuid_id)==str(1))
                                #     self.logger.info("------id,centery:%s,%s", uuid_id,y)
                                # else:
                                self.redis.set("is_working",1)
                                self.logger.info("id,centery:%s,%s", uuid_id,y)
                                # "center": [122.5, 212.0]
                                # ponit_y = 366  #中心点
                                # if (y >= (212-25)):
                                # now_time = 
                                # last_done_time = time.time()
                                # now_time = time.time()
                                # if now_time - last_done_time)
                                self.redis.set(uuid_id,1,1*60)
                                # workcmd = self.work.work(line,machine_speed)
                                workcmd = self.work.work(line,10)
                                if (len(workcmd) > 0):
                                    wheel(self.speed.revolution)
                                else:
                                    self.logger.info("------id,centery:%s,%s", uuid_id,y)
                        # if (is_working==0 or is_working=="0"):
                            # self.logger.info("false-------------------is_working----------------------------------------:%s", is_working)
                            #  稳定速度 转速
                            
                            # revolution = self.speed.uniformSpeed(machine_speed)
                            # self.logger.info("revolution:%s", revolution)
                            # # if(revolution>=40)
                            # revolution = 30 if revolution>=40 else revolution
                            # self.go(revolution)
                        
                            # # 左右位置调整
                            # line = self.line.convertLine(navigation_points,0)
                            # self.logger.info("line:%s", json.dumps(line))
                            # if (line and len(line) > 0):
                            #     center_point = screenSize[0]/2
                            #     first = line[0]
                            #     length = len(first)
                            #     cmd = ""
                            #     if (length > 0):
                            #         if (length == 1 or length == 3):
                            #             center = first[0] if length == 1 else first[1]
                            #             centerx = center["centerx"]
                            #             diff_point_x = centerx-center_point

                            #             self.point.setScreenSize(screenSize)
                            #             x= self.point.sizexm(abs(diff_point_x))
                            #             tan = x/(1000*self.point.f)
                            #             angle = int(numpy.arctan(tan) * 180.0 / 3.1415926)

                            #             # print("angle,tan,x,diff_point_x,centerx,center_point:",angle,tan,x,diff_point_x,centerx,center_point)

                            #             cmd_prefix = ""
                            #             target_angle = 90
                            #             if(global_angle<=90):
                            #                 if (centerx<=center_point) :
                            #                     target_angle = 90-angle
                            #                     cmd_prefix = "TR" if global_angle<target_angle else "TL"
                            #                 else:
                            #                     target_angle = 90+angle
                            #                     cmd_prefix = "TR"
                            #             else:
                            #                 if (centerx<=center_point) :
                            #                     target_angle = 90-angle
                            #                     cmd_prefix = "TL"
                            #                 else:
                            #                     target_angle = 90+angle
                            #                     cmd_prefix = "TR" if global_angle<target_angle else "TL"
                            #             # print("target_angle,global_angle5",target_angle,global_angle)
                            #             if(target_angle!=global_angle):
                            #                 cmd = cmd_prefix + " " + str(abs(target_angle-global_angle))
                            #                 global_angle = target_angle
                            #                 print ("send-cmd:",cmd)
                            #             else:
                            #                 print ("send-cmd:none")
                            #             # print("target_angle,global_angle2",target_angle,global_angle)
                            #             self.redis.set("global_angle", global_angle)
                            #             self.send_cmd(cmd)
                    else:
                        self.go(self.speed.revolution)
                else:
                    self.go(self.speed.revolution)
            else:
                self.redis.set("allPoints", json.dumps([]))
                # self.pub_rmq.run_subscribe(self)

            self.logger.info("time:%s,begin_work:%s", time.time(), work_flag)
            self.logger.info("----------------------loop end ------------------------------")
            # time.sleep(1)

    def go(self,revolution):
        # revolution = self.speed.revolution
        revolution = 30 if revolution>=30 else revolution
        cmd = "MF "+str(revolution)
        self.send_cmd(cmd)

    def run_subscribe(self):
        self.pub_rmq.run_subscribe(self)



if __name__ == "__main__":
    m = machine()
    try:
        m.loop()
        # m.run_subscribe()
        
    except KeyboardInterrupt:
        print("ctrl+c stop")
        redis = redisDB()
        redis.set("allPoints", json.dumps([]))
        redis.set("global_angle", 90)
        m.send_cmd("STOP 0")
