# from yolov5.utils.serial_control import serial_control
from utils.serial_control import serial_control
import time,uuid,os,numpy


class work():
    def __init__(self,redis):
        self.lock_file = "./lock.txt"
        # if not self.ser :
        self.ser = serial_control()
        self.redis = redis
        # self.ser.send_cmd("default.")
        print("-------------------------serial_control init-------------------------------------")

   

    def mk_lock_file(self):
        if (not os.path.exists(self.lock_file)):
            file = open(self.lock_file,'w')
            file.close()

    def rm_lock_file(self):
        if (os.path.exists(self.lock_file)):
            os.remove(self.lock_file)
        
    def is_lock (self):
        return os.path.exists(self.lock_file)
        
    def send(self,cmd):
        if (cmd != ""):
            cmd += "."
            cmd_dict = {
                "uuid": str(uuid.uuid1()),
                "cmd": cmd,
                "from": "camera",
            }
            # self.ser = serial_control()
            self.ser.send_cmd(cmd_dict)
            # self.ser.close()
        else:
            print("cmd null")


    def wheel(self,speed):
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
        self.redis.set("is_working","")
        # self.rm_lock_file()

    def run(box_label):
        point = box_label["point"]
        if (point):
            cmd = ""
            centerx = point["centerx"]
            screenSize = point["screenSize"]

            center_point = screenSize[0]/2
            # diff_point_x = centerx-center_point

            # self.point.setScreenSize(screenSize)
            # x= self.point.sizexm(abs(diff_point_x))

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


