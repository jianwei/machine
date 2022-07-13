#encoding:utf-8
# -*- coding:UTF-8 -*-
class ConvertPoints():
    def __init__(self):
        # 2592 × 1944 像素
        # 3280 × 2464 像素
        self.h = 76 #cm
        self.unit  = 1.12 #1.12um  像素大小
        self.f = 3.04  # 3.04mm 焦距
        self.ratio = self.h/self.f
        self.defaultWidth = 3280
        self.defaultHeight = 2464
    

    def setScreenSize(self,screenSize):
        self.showWidth = screenSize[0]
        self.showHeight = screenSize[1]
        self.ws= self.defaultWidth/self.showWidth #调整系数
        self.hs= self.defaultHeight/self.showHeight #调整系数
        print("self.ws,self.hs",self.ws,self.hs)
       
    

    def sizex(self,px):
        pointx = round(px*self.unit*self.ratio/1000*self.ws,2)
        print("pointx",pointx)

    def sizey(self,px):
        pointy = round(px*self.unit*self.ratio/1000*self.ws,2)
        print("pointy",pointy)

if __name__ == "__main__":
    dict = [{'name': 'tv 0.35', 'point': [(248, 128), (464, 128), (248, 276), (464, 276)]}]
    x = 464-248
    y = 276-128
    #210 297
    print (x,y)
    cv = ConvertPoints()
    cv.setScreenSize([640, 480])
    cv.sizex(x)
    cv.sizey(y)