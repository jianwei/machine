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
            cmd  = "ps aux | grep yolo | grep -v 'auto'| grep -v 'sh -c' | grep -v 'grep yolo' |  awk '{print $2}'"
            # cmd  = "ps aux | grep yolo | grep -v 'auto'| grep -v 'sh -c' | grep -v 'grep yolo'"
            pid = os.popen(cmd).read()
            print (pid)
            if not pid:
                # pass
                cmd = "python3 "+os.getcwd()+"/../../../yolov5/detect.py --source 0  --weight yolov5s.pt --conf 0.25 &" 
                os.system(cmd)
            # break
        else:
            cmd  = "ps aux | grep yolo | grep -v 'auto'| grep -v 'sh -c' |  awk '{print $2}'"
            pid=os.popen(cmd).read()
            closecmd = "kill -9 "+ str(pid)
            os.system(closecmd)
            redis.set("open_camera",0)
            # break
        time.sleep(1)
   

if __name__ =="__main__":
    run()
