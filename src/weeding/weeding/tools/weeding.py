# import math
import time,os
class weeding ():
    # def __init__(self,config,greenline,machineSpeed):
    def __init__(self,config):
        self.config = config
        self.redis = config.get("redisObj")
        self.unit = config.get("weedingtool").get("unit")
        # self.greenline = greenline
        # self.machineSpeed = machineSpeed
        # self.calculate()
        pass
    
    def setData(self,greenline,machineSpeed):
        self.greenline = greenline
        self.machineSpeed = machineSpeed



    def calculate(self):
        weedingTool = []
        if self.greenline :
            firstLen = len(self.greenline[0])
            secondLen = len(self.greenline[1])
            l = len(self.greenline)
            for i in range(firstLen):
                if(firstLen==secondLen):
                    item1 = self.greenline[l-1][i]
                    item2 = self.greenline[l-2][i]
                elif(firstLen>secondLen):
                    item2 = self.greenline[l-2][i]
                    item1 = item2
                else:
                    item1 = self.greenline[l-1][i]
                    item2 = item1
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
        if int(diffDistance) > 0:
            time = round(diffDistance/machineSpeed,2)
            # print("time",time)
            num = int(diffDistance/self.unit) if diffDistance/self.unit>1 else 1
            preround =round( num*360 / time,2)
            return preround
        else:
            return 0

    def run(self):
        print("self.weedingTool",self.weedingTool)
        key  = self.config.get("redis").get("camera")
        while (True):
            # value = self.config.get("redis").get("camera")
            value = self.redis.get(key)
            print ("camera--:",value)
            self.config.get("cameraObj").add()
            time.sleep(1)
        pass

    #停止工作,关闭除草头以及相机
    def stop(self):
        self.pause()
        # pass

    #暂停工作,关闭除草头
    def pause(self):
        cmd  = "ps aux | grep yolo | grep -v 'auto'| grep -v 'sh -c' |  awk '{print $2}'"
        pid=os.popen(cmd).read()
        closecmd = "kill -9 "+ str(pid)
        os.system(closecmd)
        self.redis.set("open_camera",0)
        pass

