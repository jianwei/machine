import argparse
import string
import serial,json,sys,os
sys.path.append("..")
from redisConn.index import redisDB

redis = redisDB()
global_angle = 0


def exec_cmd(cmd):
    cmd = json.loads(cmd)
    str_cmd = ""
    response = -1
    for key in cmd:
        str_cmd = key+ " " + str(cmd[key])
        if(key=="TA"):  #转向处理
            flag = turn(cmd[key])
            str_cmd = flag+ " " + str(cmd[key])

    # ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
    # ser.write(str_cmd)
    # try:    
    #     response = ser.readall().decode('utf-8');#read a string from port
    #     print(response.decode('utf-8') );
    # except expression:
    #     print("serial_control,expression:",cmd,expression)
    print (response)
    return response

def set_redis(redisDict):
    dict = json.loads(redisDict)
    for key in dict:
        val = dict[key]
        if(key=="begin_work"):
            val=1
            begin_work_cache = redis.get("begin_work")
            if(begin_work_cache!=""):
                if (int(dict["begin_work"])==1 ):
                    if(int(begin_work_cache)!=1):
                        dict = {"TA":90}
                        exec_cmd(dict)
                        open_camera()
                    else:
                        val=0
            else:
                open_camera()
        redis.set(key,val)

def turn(angle):
    flag = "TR" if (global_angle - angle)<0 else "TL" 
    return flag

        
def open_camera():
    # print ("open camera fun")
    # cmd  = "ps aux | grep track | grep -v 'auto'| grep -v '/usr/libexec'  |  awk '{print $2}'"
    # pid = os.popen(cmd).read()
    # print (pid)
    # if not pid:
    #     print ("open camera")
    cmd = "cd ../StrongSORT/ && python3 track.py --source 0  &" 
    os.system(cmd)
    

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=int, default=0, help='类型:1,串口指令.2 set redis')
    parser.add_argument('--dict', type=str, default="", help='串口指令 以及 redis key,value json格式.')
    opt = parser.parse_args()
    
    if (opt.type==1):
        exec_cmd(opt.dict)
    elif (opt.type==2) :
        set_redis(opt.dict)
    return opt



if __name__ == "__main__":
    m = parse_opt()