import sys, os
sys.path.append("..")
from redisConn.index import redisDB
from run import run 
from scan import scan 
from work import work 
class machine () :
    def __init__(self):
        self.redis = redisDB()
        self.work = work()
        self.scan = scan()
        self.run = run()

    def go(self):
        pass 

    def stop(self):
        pass
    
    def work(self):
        pass


    def loop(self):
        distance = self.getDistance()

    def getGreen():
        pass
    

    def getDistance(self):
        distance = self.redis.get("distance")
        return distance

    
    

if __name__ == "__main__":
        s = machine()
