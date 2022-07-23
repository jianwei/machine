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
            print (os.getcwd())
            if not pid:
                cmd = "cd ../../../StrongSORT/ && python3 track.py --source 0 " 
                os.system(cmd)
        time.sleep(1)
        

if __name__ =="__main__":
    run()
