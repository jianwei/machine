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
            self.redis.get("distance_pointer")
            print (distance_pointer)
            print("time:",time.time())
            print("----------------------end loop ------------------------------")
            time.sleep(1)


if __name__ == "__main__":
    w = work()
    try:
        w.loop()
    except KeyboardInterrupt:
        print("ctrl+c stop")
        # m.send_cmd("STOP 0")