#!/usr/bin/env python3
import os,sys,time

sys.path.append(os.getcwd()+"/../../../")
from redisConn.index import redisDB


def run():
    redis = redisDB()
    while (True) : 
        value = redis.get("open_camera")
        print("value:>>",value,time.time())
        if(value and int(value)==1):
            cmd  = "ps aux | grep StrongSORT | grep -v 'auto'| grep -v 'sh -c' | grep -v 'grep StrongSORT' |  awk '{print $2}'"
            pid = os.popen(cmd).read()
            print (pid)
            if not pid:
                # pass
                # StrongSORT/track.py
                cmd = "python3 "+os.getcwd()+"/../../../StrongSORT/track.py --source 0  &" 
                os.system(cmd)
            # break
        time.sleep(1)
        # else:
        #     cmd  = "ps aux | grep yolo | grep -v 'auto'| grep -v 'sh -c' | grep -v 'grep yolo'|  awk '{print $2}'"
        #     # cmd  = "ps aux | grep yolo | grep -v 'auto'| grep -v 'sh -c' | grep -v 'grep yolo'"
        #     pid=os.popen(cmd).read()
        #     print ("pid:",pid)
        #     if pid:
        #         closecmd = "kill -9 "+ str(pid)
        #         os.system(closecmd)
        #     redis.set("open_camera",0)
        #     # break
        # time.sleep(1)
   

if __name__ =="__main__":
    run()
