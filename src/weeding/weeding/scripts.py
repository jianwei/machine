#!/usr/bin/env python3
import os,sys,time

sys.path.append(os.getcwd()+"/../../../")
from redisConn.index import redisDB


def run():
    redis = redisDB()
    while (True) : 
        value = redis.get("open_camera")
        print("value:>>",value,int(value)==1)
        if(int(value)==1):
            cmd = "python3 "+os.getcwd()+"/../../../yolov5/detect.py --source 0  --weight yolov5s.pt --conf 0.25 &" 
            os.system(cmd)
            break
        time.sleep(1)
   

if __name__ =="__main__":
    run()
