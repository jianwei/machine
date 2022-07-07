import sys, os
from this import s
import time
sys.path.append("..")
from redisConn.index import redisDB
from run import run 
from scan import scan 
from work import work
from convertPoints import ConvertPoints
import json 
class machine () :
    def __init__(self):
        self.redis = redisDB()
        self.work = work()
        self.scan = scan()
        self.run = run()
        self.convertPoints = ConvertPoints()
    
    
    # def scan(self):
    #     self.scan.scan()

    def go(self):
        self.run.go(self.greens)
        # pass 

    def stop(self):
        self.run.stop()
        pass
    
    def work(self):
        self.work.work()
        pass


    def loop(self):
        while (True):
            greens = self.getGreen()
            self.go()
            # time.sleep(5)
            # print("greens",greens)
            print("loop")
            break
        pass

    def getGreen(self):
        # imagePoints
        # imageDistance
        # try:
        greens = self.redis.get("imagePoints")
        screenSize = self.redis.get("screenSize")
        self.greens = json.loads(greens)
        self.convertPoints.setScreenSize(json.loads(screenSize))
        self.realGreensPoints = []
        for i in range(len(self.greens)):
            realPoints = self.convertPoints.converPoints(self.greens[i])
            self.realGreensPoints.append(realPoints)
        greenLine = self.convertPoints.formatLine(self.realGreensPoints)
        isCenter = self.convertPoints.isCenter(greenLine)
        print ("screenSize:",screenSize)
        print ("greens:",greens)
        print ("greenLine:",greenLine)
        print ("isCenter:",isCenter)
        return self.greens
    

    def getDistance(self):
        distance = 80  #cm
        return distance

    
    

if __name__ == "__main__":
        m = machine()
        # m.scan()
        m.loop()
