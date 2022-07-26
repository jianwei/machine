#!/usr/bin/env python3
import os,sys,time
# from utils.serial_control import serial_control 
sys.path.append(os.getcwd()+"/../../../")
from redisConn.index import redisDB
redis = redisDB()


def run():
    while (True) : 
        value = redis.get("open_camera")
        print("value:>>",value,time.time())
        if(value and int(value)==1):
            cmd  = "ps aux | grep StrongSORT | grep -v 'auto'| grep -v 'sh -c' | grep -v 'grep StrongSORT' |  awk '{print $2}'"
            pid = os.popen(cmd).read()
            print (pid)
            print (os.getcwd())
            if not pid:
                # cmd = "cd ../../../StrongSORT/ && python3 track.py --source 0 " 
                cmd = "cd ../../../yolov5/ && python3 detect.py --source 0  --weight yolov5s.pt --conf 0.25 &" 
                os.system(cmd)
        time.sleep(1)
        

if __name__ =="__main__":
    try:
        run()
        # arduino_cmd
        cmd = "cd utils && python3 serial_control.py &"
        os.system(cmd)

    except KeyboardInterrupt:
        redis.set("open_camera",0)
        pass
