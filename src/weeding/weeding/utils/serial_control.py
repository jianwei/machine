#导入pyserial模块
# chmod -R 777 /dev/ttyAMA0
import serial,sys,os,redis,time
sys.path.append(os.getcwd()+"/../../../../")
from redisConn.index import redisDB
redis = redisDB()            
class serial_control ():
    def __init__(self):
        # self.ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
        pass
    
    def sendMsg(self):
        while (True):
            print("serial_control:",time.time())
            cmd = redis.get("arduino_cmd")
            if(cmd):
                # self.ser.write(cmd)
                # try:    
                #     response = self.ser.readall() #read a string from port
                #     print ("serial_control:cmd",cmd,response)
                # except expression:
                #     print("serial_control,expression:",cmd,expression)
                pass
            time.sleep(1)



if __name__ =="__main__":
    # try:
    ser = serial_control()
    ser.sendMsg()    
