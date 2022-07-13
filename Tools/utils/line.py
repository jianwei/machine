import json,sys
import functools 

def cmpx(a,b): 
    return a.get("centerx") - b.get("centerx")

def cmpy(a,b): 
    return a[0].get("centery") - b[0].get("centery")

class line ():
    def __init__(self,config):
        self.config = config
        self.redis = config.get("redisObj")
        self.camera = config.get("cameraObj")
        self.green = json.loads(self.redis.get("camera"))[0]
        self.lineList = []
        self.sortGreen(self.green)
        self.convertLine(self.green)
        
    def getLine(self):
        return self.lineList

    def sortGreen(self,green):
        green = self.getCenter(green)
        green.sort(key=functools.cmp_to_key(cmpx))
        self.green = green
        return green


    def convertLine(self,green):
        diff = self.config.get("line").get("diff")
        green = self.getCenter(green)
        diffPx = self.camera.distanceToPointy(diff)
        lineList = []
        for item in green:
            isAdded = False
            if(len(lineList)<1):
                lineList.append([item])
                isAdded = True
            else:
                centerY = item.get("center")[1]
                for itemLine in lineList:
                    lineY = itemLine[0].get("centery")
                    if(float(lineY-diffPx)<=float(centerY)<=float(lineY+diffPx)):
                        itemLine.append(item)
                        isAdded = True                       
            if (not isAdded):
                lineList.append([item])
        lineList.sort(key=functools.cmp_to_key(cmpy))
        self.lineList = lineList
        return lineList


    def getCenter(self,green):
        for item in green:
            point = item.get("point")
            centerx = round((point[0][0]+point[1][0]) /2,2)
            centery = round((point[1][1]+point[3][1]) /2,2)
            item["center"] = [centerx,centery]
            item["centerx"] = centerx
            item["centery"] = centery
        return green
