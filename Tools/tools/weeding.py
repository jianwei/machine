# import math
class weeding ():
    def __init__(self,config,greenline,machineSpeed):
        self.config = config
        self.unit = config.get("weedingtool").get("unit")
        self.diffDistance = 0
        self.greenline = greenline
        self.calculateDistance(greenline)
        self.calculateSpeed(machineSpeed)
        print("weeding __init__",config)
        pass

    

    #计算2个植物之间的距离
    def calculateDistance(self,greenline): 
        first = greenline[0][0].get("center")
        second = greenline[1][0].get("center")
        diff = second[1]-second[0]
        self.diffDistance = self.config.get("cameraObj").sizey(diff)
        return self.diffDistance

    def calculateSpeed(self,machineSpeed):
        time = round(self.diffDistance/machineSpeed,2)
        num = int(self.diffDistance/self.unit)
        preround =round( num*360 / time,2)
        print(num,time,preround)
        pass

    def run(self):
        pass
    def stop(self):
        pass

