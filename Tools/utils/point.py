
class point():
    
    def __init__(self):
        # 2592 × 1944 像素
        # 3280 × 2464 像素
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
    
    def sizex(self,px):
        pointx = round(px*self.unit*self.ratio/1000/10*self.ws,2)
        # print("pointx",pointx)
        return pointx

    def sizey(self,px):
        pointy = round(px*self.unit*self.ratio/1000/10*self.ws,2)
        # print("pointy",pointy)
        return pointy

    
