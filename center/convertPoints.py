
# from operator import le
# from numpy import append


class ConvertPoints():
    def __init__(self):
        self.h = 950 #cm
        self.unit  = 1.4 #1.4um  像素大小
        self.f = 3.6  # 3.6mm 焦距
        self.ratio = self.h/self.f
        self.showWidth = 640    #640
        self.showHeight = 480    #480
        self.defaultWidth = 2592
        self.defaultHeight = 1944
        self.diff = 10 #cm 误差前后10厘米
        self.ws= self.defaultWidth/self.showWidth #调整系数
        self.hs= self.defaultHeight/self.showHeight #调整系数
        # 2592 × 1944 像素
        # 3280 × 2464 像素
        self.fullHeight = round(self.showHeight*self.unit*self.ratio/1000/10*self.hs,2)
        pass
    
    # v 物距   雷达扫描 单位mm
    def convert(self,points):
        realPoints  = []
        pointw = round(points[0]*self.unit*self.ratio/1000/10*self.ws,2)
        pointh = round(points[1]*self.unit*self.ratio/1000/10*self.hs,2)
        realPoints = [pointw,pointh]
        return realPoints
    
    def setScreenSize(self,screenSize):
        self.showWidth = screenSize[0]
        self.defaultHeight = screenSize[1]

    def converPoints(self,points):
        for i in range(len(points)):
            item = self.convert(points[i])
            points[i] = item
        return points


    def formatLine(self,realpoints):
        centerPointer = []
        line=[]
        index = []
        greenLine = []
        for i in range(len(realpoints)):
            centerItem = self.getCenter(realpoints[i])
            centerPointer.append(centerItem)
        for i in range(len(centerPointer)):
            # print("i:",i)
            item = centerPointer[i]
            y = item[1]
            if (len(line) ==0):
                lineItem = [y]
                line.append(lineItem)
                index.append([i])
            else : 
                isAdd = False
                for j in range(len(line)):
                    lineItem = line[j]
                    indexItem = index[j]
                    if(y-self.diff<=line[j][0]<=y+self.diff):
                        lineItem.append(y)
                        indexItem.append(i)
                        isAdd = True
                        break
                if(not isAdd):
                    lineItem = [y]
                    line.append(lineItem)
                    index.append([i])
        for i in  range(len(index)):
            greenItem = []
            for j in range(len(index[i])):
                greenItem.append(realpoints[index[i][j]])
            greenLine.append(greenItem)
        greenLine = self.sortGreenLine(greenLine,line)
        return greenLine

    def isCenter(self,greenLine):
        # if()
        diff  = 5 #cm
        firstLine = greenLine[0][0][0]
        firstY = firstLine[1]
        print("firstLine",self.fullHeight,firstLine,firstY)
        if(self.fullHeight-diff<=firstY<=self.fullHeight+diff):
            return True
        return False
        pass


    def sortGreenLine(self,greenLine,line):
        greenLine.sort(reverse=True)  # False  reverse倒序 
        # for item in greenLine:
            # print("item",item)
            # for itemPointer in item:
                # print("itemPointer",itemPointer)
        return greenLine

    def getYDistance (self,points):
        # for item in 
        pass


    def getCenter(self,points):
        xCenter = round((points[1][0] - points[0][0])/2,2)
        yCenter = round((points[2][1] - points[0][1])/2,2)
        center = [xCenter,yCenter]
        return center
