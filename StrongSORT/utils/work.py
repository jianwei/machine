# from yolov5.utils.serial_control import serial_control
from turtle import st
from utils.serial_control import serial_control
import time
import uuid
import os
import numpy
import json


class work():
    def __init__(self, redis):
        self.ser = serial_control()
        self.global_angle = 90
        self.redis = redis
        self.default_speed = 15
        print("-------------------------serial_control init-------------------------------------")

    def send(self, cmd):
        ret = ""
        if (cmd != ""):
            cmd += "."
            cmd_dict = {
                "uuid": str(uuid.uuid1()),
                "cmd": cmd,
                "from": "camera",
            }
            # self.ser = serial_control()
            ret = self.ser.send_cmd(cmd_dict)
            # self.ser.close()
        else:
            print("cmd null")
        return ret

    def work_and_run(self, camera_type):

        navigation_points = self.redis.get("navigation_points")
        vegetable_points = self.redis.get("vegetable_points")

        # print("navigation_points:", navigation_points,type(navigation_points))
        # print("vegetable_points:", vegetable_points,type(vegetable_points))
        if (navigation_points):
            last_point_navigation_point = json.loads(navigation_points)[0]
        else:
            last_point_navigation_point = {}
        is_working = self.redis.get("is_working")

        if (camera_type == 0):  # item_navigation_points
            if (str(is_working) == "0" or str(is_working) == ""):
                if (len(last_point_navigation_point) > 0):  # 转弯
                    has_turn = self.redis.get("has_turn")
                    if (str(has_turn) == "0" or str(has_turn) == ""):
                        self.send("STOP 0")
                        self.turn(last_point_navigation_point)
                        self.redis.set("turn_flag", 1)
                    self.send("MF " + str(self.default_speed))
                else:
                    self.send("MF " + str(self.default_speed))
        elif (camera_type == 1):  # item_vegetable_points
            if (vegetable_points and len(vegetable_points) > 0):
                done = vegetable_points[0]
                working_time_out = 3*60
                last_working_time = self.redis.get("last_working_time")
                last_working_time = float(
                    last_working_time) if last_working_time != "" else 0
                now = time.time()
                diff = now - float(last_working_time)
                centery = done["centery"]
                # print("centery,:", centery)
                # print("last_working_time", last_working_time)
                # print("diff", diff)

                if (is_working == "0" or is_working == 0 or is_working == "" and diff >= 2):
                    centery = done["centery"]
                    if (centery >= 50 and centery <= 150):
                        self.redis.set("is_working", 1, working_time_out)
                        self.redis.set("last_working_time",
                                       time.time(), working_time_out)
                        self.wheel(self.default_speed)
                    else:
                        print("centery is outer:", centery)
                else:
                    print("is_working,last_working_time,now:",
                          is_working, now, last_working_time)
                print(
                    "-------------------------------- end -------------------------------------------")

    def wheel(self, speed):
        # if (not os.path.isfile(self.lock_file)):
        rot_speed = 60
        unit_sleep = 1 / (rot_speed * 50 / 2 / 1000)  # 转1圈所需要的时间
        # unit_sleep -= 0.04  # 误差
        print("unit_sleep:%s", unit_sleep)
        # print(time.time(), "------------------------------------------------------wheel-----------------------------------------")
        self.send("STOP 0")
        self.send("MD")
        time.sleep(2)
        # print(time.time(), "-----------------------------------------")
        self.send("STOP 2")
        self.send("RROT " + str(rot_speed))
        time.sleep(unit_sleep)
        self.send("STOP 2")
        self.send("MU")
        time.sleep(2)
        self.send("STOP 2")
        self.send("MF " + str(speed))
        time.sleep(1)
        self.redis.set("is_working", "")
        self.redis.set("is_navtion_now", 0)
        # self.rm_lock_file()

    def turn(self, box_label):
        # print("box_label:",box_label,type(box_label))
        # box_label = box_label[0]
        self.redis.set("is_navtion_now", 1)
        # point = box_label["point"]
        point = box_label[0]
        unit = 0.0386  # 1 pint 0.0386cm
        gap = 30  # cm 导航摄像头的视野盲区
        if (point):
            cmd = ""
            centerx = point["centerx"]
            centery = point["centery"]
            screenSize = point["screenSize"]
            center_point = screenSize[0]/2
            diff_point_x = centerx-center_point
            tan = (diff_point_x*unit)/(gap+centery*gap)
            angle = int(numpy.arctan(tan) * 180.0 / 3.1415926)
            global_angle = self.global_angle
            cmd_prefix = ""
            target_angle = 90
            if (global_angle <= 90):
                if (centerx <= center_point):
                    target_angle = 90-angle
                    cmd_prefix = "TR" if global_angle < target_angle else "TL"
                else:
                    target_angle = 90+angle
                    cmd_prefix = "TR"
            else:
                if (centerx <= center_point):
                    target_angle = 90-angle
                    cmd_prefix = "TL"
                else:
                    target_angle = 90+angle
                    cmd_prefix = "TR" if global_angle < target_angle else "TL"
            # print("target_angle,global_angle5",target_angle,global_angle)
            if (target_angle != global_angle):
                cmd = cmd_prefix + " " + str(abs(target_angle-global_angle))
                global_angle = target_angle
                print("send-cmd:", cmd)
            else:
                print("send-cmd:none")
            # print("cmd:",cmd)
            turn_ret = self.send(cmd)
            print("cmd,turn_ret:", cmd, turn_ret)
            # if(turn_ret==0 or turn_ret=="0") :
            # 继续前行
            self.send(cmd)
