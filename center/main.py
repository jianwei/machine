from convertPoints import ConvertPoints
import time,os,sys,serial
import json
sys.path.append("..")
from redisConn.index import redisDB
# chmod -R 777 /dev/ttyAMA0
# import serial,sys,os,redis,time

class machine ():
    def __init__(self):
        self.redis = redisDB()
        # self.ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
        # self.convertPoints = ConvertPoints()


    def send_cmd(self,cmd):
        # self.ser.write(cmd)
        try:    
            # response = self.ser.readall() #read a string from port
            print ("serial_control:cmd",cmd)
        except expression:
            print("serial_control,expression:",cmd,expression)
  

    def loop(self):
        while (True):
            value = self.redis.get("machine_cmd")
            # print("loop1:",value,type(value))
            if(value):
                value = json.loads(value)
            # print("loop2:",value,type(value))
            if(value):
                if ("wheel" in value):
                    if ( "RST" == value.get("wheel")):
                        self.send_cmd("RST")        # 复位，返回0执行成功
                    if ("QMS" == value.get("wheel")):
                        self.send_cmd("QMS")        # query movement status查询行进速度等信息
                    if ("QOS" == value.get("wheel")):
                        self.send_cmd("QOS")        #  query_operation_status查询滑轨所在的位置等
                    if ("MF" == value.get("wheel")):
                        self.send_cmd("MF "+str(value.get("speed")))       # move_forward以指定速度持续前进；返回0执行成功
                    if ("MB" == value.get("wheel")):
                        self.send_cmd("MB "+str(value.get("speed")))       #  move_backward以指定速度持续后退；返回0执行成功
                    if ("STOP" == value.get("wheel")):
                        self.send_cmd("STOP "+str(value.get("type")))      #  type: 0全停；1刹车；2操作臂停止；返回0执行成功
                    if ("TA" == value.get("wheel")):
                        self.send_cmd("TA "+str(value.get("angle")))       # turn_angle，angle为int度数；返回0执行成功

                if ("slide" in value):
                    if ("ML" == value.get("slide")):
                        self.send_cmd("ML "+str(value.get("distance")))       # move_forward以指定速度持续前进；返回0执行成功
                    if ("MR" == value.get("slide")):
                        self.send_cmd("MR "+str(value.get("distance")))       #  move_backward以指定速度持续后退；返回0执行成功
                    if ("MU" == value.get("slide")):
                        self.send_cmd("MU "+str(value.get("distance")))       #  type: 0全停；1刹车；2操作臂停止；返回0执行成功
                    if ("MD" == value.get("slide")):
                        self.send_cmd("MD "+str(value.get("distance")))       # turn_angle，angle为int度数；返回0执行成功
                if ("motion" in value):
                    if ("ROT" in value.get("motion")):
                        self.send_cmd("ROT "+str(value.get("angle")))       #  rotate按指定角度（int）旋转；返回0执行成功
                    if ("STOP" in value.get("motion")):
                        self.send_cmd("STOP "+str(value.get("type")))       #  0全停；1刹车；2操作臂停止；返回0执行成功
            self.redis.set("machine_cmd","")
            time.sleep(0.1)
        # pass

    


if __name__ == "__main__":
    m = machine()
    # m.scan()
    m.loop()
