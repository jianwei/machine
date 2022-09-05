from select import select
from utils.serial_control import serial_control
import threading,time,uuid,os


class work():
    def __init__(self):
        self.lock_file = "./lock.txt"
        # if not self.ser :
        self.ser = serial_control()

   

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
            # ser = serial_control()
            self.ser.send_cmd(cmd_dict)
            self.ser.close()
        else:
            print("cmd null")


    def wheel(self,speed):
        # if (not os.path.isfile(self.lock_file)):
        rot_speed = 60
        unit_sleep = 1 / (rot_speed * 50 / 2 / 1000)  # 转1圈所需要的时间
        unit_sleep -= 0.04  # 误差
        print("unit_sleep:%s", unit_sleep)
        print(time.time(), "------------------------------------------------------wheel-----------------------------------------")
        self.send("STOP 0")
        self.send("MD")
        time.sleep(2)
        print(time.time(), "-----------------------------------------")
        self.send("STOP 2")
        self.send("RROT " + str(rot_speed))
        time.sleep(unit_sleep)
        self.send("STOP 2")
        self.send("MU")
        time.sleep(2)
        self.send("STOP 2")
        # redis.set("is_working",0)
        # self.send("MF " + str(speed))
        self.rm_lock_file()
