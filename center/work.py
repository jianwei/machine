import time,sys
sys.path.append("..")
from redisConn.index import redisDB
class work:
    def __init__(self):
        self.redis = redisDB()
        pass

    def loop(self):
        while(1):
            
            print("----------------------begin loop ------------------------------")
            tmie1 = time.time()
            print("tmie1:",tmie1)
            distance_pointer = self.redis.get("distance_pointer")

            print (distance_pointer)
            # print("time:",time.time())
            tmie2 = time.time()
            print("tmie2:",tmie2)
            print("----------------------end loop ------------------------------")
            
            time.sleep(1)


if __name__ == "__main__":
    w = work()
    try:
        w.loop()
    except KeyboardInterrupt:
        self.redis.set("distance_pointer",json.dumps({}))
        print("ctrl+c stop")
        # m.send_cmd("STOP 0")