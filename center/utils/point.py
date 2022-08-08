import math
class point():
    
    def __init__(self):
        self.distance = 100 #摄像头中心距离除草头的距离
        self.h = 760 #cm
        self.unit  = 1.12 #1.12um  像素大小
        self.f = 3.04  # 3.04mm 焦距
        self.ratio = self.h/self.f
        self.defaultWidth = 3280
        self.defaultHeight = 2464
        self.ws = 1
        self.hs = 1
    

    def setScreenSize(self,screenSize):
        self.showWidth = screenSize[0]
        self.showHeight = screenSize[1]
        self.ws= self.defaultWidth/self.showWidth #调整系数
        self.hs= self.defaultHeight/self.showHeight #调整系数
        # print("self.ws,self.hs",self.ws,self.hs)
    
    def sizex(self,px,angle=90):   # angle 默认90 否则45
        pointx = round(px*self.unit*self.ratio/1000/10*self.ws,2)
        # print("pointx",pointx) 
        return pointx

    def sizey(self,px,angle=90):# angle 默认90 否则45
        pointy = round(px*self.unit*self.ratio/1000/10*self.ws,2)
        # print("pointy",pointy)
        if(angle!=90):
            pointy= pointy / math.sin(45)
        return pointy

    def getDistanceY(self,point,screenSize):
        centery = (point[0][1] + point[3][1])/2 
        print(point,centery,screenSize)
        diff  = centery-screenSize[0][1] 
        distanceY = self.sizey(abs(diff),45)
        y = distanceY if distanceY>0 else -distanceY
        return self.distance+y
        # pass

    
