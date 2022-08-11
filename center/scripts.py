import argparse
import string
import serial,json,sys,os
sys.path.append("..")
from redisConn.index import redisDB

redis = redisDB()
global_angle = redis.get("global_angle")
if global_angle:
    global_angle = int(global_angle)
else :
    global_angle = 0


def exec_cmd(cmd):
    cmd = json.loads(cmd)
    str_cmd = ""
    response = -1
    for key in cmd:
        str_cmd = key+ " " + str(cmd[key])
        if(key=="TA"):  #转向处理
            flag = turn(cmd[key])
            turnangle = abs(global_angle-cmd[key])
            str_cmd = flag+ " " + str(turnangle)
        if(key=="STOP" and cmd[key]==1):
            # 关闭摄像头
            dict = json.dumps({"begin_work":0})
            redis.set("global_angle",0)
            set_redis(dict)
    redis.set("global_angle",cmd[key]) 
    print("exec_cmd,str_cmd:",str_cmd)
    response = send_cmd(str_cmd)
    print ("exec_cmd:",response)
    return response

def send_cmd(cmd):
    port = "/dev/ttyACM0"
    ser = serial.Serial(port, 9600, timeout=1)
    ser.flushInput()  # 清空缓冲器
    ret = -2
    try:
        while True:
            ser.write(cmd.encode())
            arr = ser.readall()
            response = arr.splitlines()
            ret = response[1].decode("UTF-8") if len(response)>1 else ""
            print(arr,response,ret)
            if(response):
                ser.close()
                break
    except Exception as e:
        print("serial连接或者执行失败,reason:", e)
        ser.close()
    return ret


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
                        # global_angle = 0
                        dict = json.dumps({"TA":90})
                        exec_cmd(dict)
                        open_camera()
                    else:
                        val=0
            else:
                # reset 
                dict = json.dumps({"RST":1})
                exec_cmd(dict)
                # 关闭摄像头
                # open_camera()

        redis.set(key,val)

def turn(angle):
    flag = "TR" if (global_angle - angle)<0 else "TL" 
    return flag

        
def open_camera():
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