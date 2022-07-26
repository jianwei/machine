#导入pyserial模块
import serial,sys,os
sys.path.append(os.getcwd()+"/../../../../")
from redisConn.index import redisDB
redis = redisDB()              
class serial_control ():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
        pass
    
    def sendMsg(self):
        while (True):
            cmd = redis.get("arduino_cmd")
            ser.write(cmd)
            response = ser.readall() #read a string from port
            print (response)
            pass

if __name__ =="__main__":
    # try:
    ser = serial_control()
    ser.sendMsg()    
