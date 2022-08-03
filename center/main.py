# from convertPoints import ConvertPoints
import time,os,sys,serial,json
# import json
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
        while (1):
            
            print(time.time())

            time.sleep(1)



        pass

    


if __name__ == "__main__":
    m = machine()
    # m.scan()
    m.loop()
