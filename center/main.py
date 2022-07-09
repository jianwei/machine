from convertPoints import ConvertPoints
import time,os,sys
# from work import work
# from run import run
# from scan import scan
import json
sys.path.append("..")
from redisConn.index import redisDB


class machine ():
    def __init__(self):
        self.redis = redisDB()
        # self.work = work()
        # self.scan = scan()
        # self.run = run()
        self.convertPoints = ConvertPoints()

    # def scan(self):
    #     self.scan.scan()

    def go(self):
        # self.run.go(self.greens)
        pass

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
            time.sleep(5)
            # print("greens",greens)
            print("loop")
            
            # break
        pass

    def getGreen(self):
        # imagePoints
        # imageDistance
        # screenSize = json.dumps([1280, 720])
        # greens = json.dumps([[(1178, 457), (1279, 457), (1178, 663), (1279, 663)], [(1189, 459), (1240, 459), (1189, 505), (1240, 505)], [(939, 408), (1269, 408), (939, 717), (1269, 717)], [
        #                     (226, 508), (331, 508), (226, 626), (331, 626)], [(939, 404), (1268, 404), (939, 712), (1268, 712)], [(77, 332), (888, 332), (77, 711), (888, 711)]])
        # # try:
        greens = self.redis.get("allPoints")
        screenSize = self.redis.get("screenSize")
        greens = json.loads(greens)
        print("--------------------------------------------------------------------------------------------------")
        # print("greens",greens)
        # print("screenSize",screenSize)

        
        # self.convertPoints.setScreenSize(json.loads(screenSize))
        # self.convertPoints = 3 # 误差3cm
        # self.convertPoints.formatLineByPoints(self.greens)

        # self.convertPoints.getPx(3)
        # realGreensPoints = []
        for i in range(len(greens)):
            item = greens[i]
            if (item["name"].find("cup")!=-1):
                print("cup--", item)
            if (item["name"].find("phone")!=-1):
                print("phone--", item)
            # realPoints = self.convertPoints.converPoints(item)
            # print("realPoints", realPoints)
            # realGreensPoints.append(realPoints)
        # print("realGreensPoints", realGreensPoints)
        # greenLine = self.convertPoints.formatLine(realGreensPoints)
        # for j in greenLine:
        #     print("greenLineitem---", j)
        # print("greenLine",greenLine)
        # isCenter = self.convertPoints.isCenter(greenLine)
        # print ("screenSize:",screenSize)
        # print ("greens:",greens)
        # print ("greenLine:",greenLine)
        # print ("isCenter:",isCenter)
        # return self.greens

    def getDistance(self):
        distance = 80  # cm
        return distance


if __name__ == "__main__":
    m = machine()
    # m.scan()
    m.loop()
