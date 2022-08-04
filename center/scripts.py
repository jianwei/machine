import argparse
import serial,json,sys
sys.path.append("..")
from redisConn.index import redisDB

redis = redisDB()


def exec_cmd(cmd):
    print("cmd:=====-",cmd)
    pass
    # ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
    # ser.write(cmd)
    # try:    
    #     # response = self.ser.readall() #read a string from port
    #     print ("serial_control:cmd",cmd)
    # except expression:
    #     print("serial_control,expression:",cmd,expression)

def set_redis(redisDict):
    dict = json.loads(redisDict)
    for key in dict:
        redis.set(key,dict[key])

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=int, default=0, help='类型:1,串口指令.2 set redis')
    parser.add_argument('--cmd', type=str, default="", help='串口指令.')
    parser.add_argument('--dict', type=str, default="", help='redis key,value json格式.')
    opt = parser.parse_args()
    print("dict:",opt.dict)
    
    if (opt.type==1):
        exec_cmd(opt.cmd)
    elif (opt.type==2) :
        set_redis(opt.dict)
    return opt



if __name__ == "__main__":
    m = parse_opt()
    # m.scan()
    # m.loop()