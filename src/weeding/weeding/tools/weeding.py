# import math
class weeding ():
    def __init__(self,config,greenline,machineSpeed):
        self.config = config
        self.unit = config.get("weedingtool").get("unit")
        self.greenline = greenline
        self.machineSpeed = machineSpeed
        self.calculate()
        pass

    def calculate(self):
        weedingTool = []
        if self.greenline :
            firstLen = len(self.greenline[0])
            for i in range(firstLen):
                l = len(self.greenline)
                item1 = self.greenline[l-1][i]
                item2 = self.greenline[l-2][i]
                distance = self.calculateDistance(item1,item2)
                preround = self.calculateSpeed(self.machineSpeed,distance)
                weedingTool.append({
                    "distance":distance,
                    "preround":preround
                })
        self.weedingTool = weedingTool
        return weedingTool

    #计算2个植物之间的距离
    def calculateDistance(self,item1,item2): 
        first = item1.get("centery")
        second = item2.get("centery")
        diff = first-second
        diffDistance = self.config.get("cameraObj").sizey(diff)
        return diffDistance
        # pass
        

    def calculateSpeed(self,machineSpeed,diffDistance):
        time = round(diffDistance/machineSpeed,2)
        num = int(diffDistance/self.unit) if diffDistance/self.unit>1 else 1
        preround =round( num*360 / time,2)
        return preround

    def run(self):
        print("self.weedingTool",self.weedingTool)
        # pass



    def stop(self):
        pass

