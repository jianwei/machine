

class slide():
    
    def __init__(self,config):
        self.config = config
        self.diff = config.get("weedingtool").get("diff")
        self.leftdiff = config.get("weedingtool").get("leftdiff")
        self.radius = config.get("weedingtool").get("radius")
        self.camera = config.get("cameraObj")
        self.adjustPointer = []
        self.toolPointer = []

    
    def adjust(self,lineList,screen) :
        lastLine = lineList[len(lineList)-1]
        diffPx = self.camera.distanceToPointx(self.diff)
        radiusPx = self.camera.distanceToPointx(self.radius)
        leftdiffPx = self.camera.distanceToPointx(self.leftdiff)
        firstCenter = lastLine[0].get("center") 
        for item in lastLine:
            point = item.get("point")
            adjustPointerItem = point[0][0]-leftdiffPx
            toolItem = adjustPointerItem+radiusPx
            self.adjustPointer.append(adjustPointerItem)
            self.toolPointer.append(toolItem)
        ret = {"adjustPointer":self.adjustPointer,"toolPointer":self.toolPointer}
        return   ret  #eg: {'adjustPointer': [24, 204, 384], 'toolPointer': [76, 256, 436]}

    def insert(self):  # 插入土中
        pass