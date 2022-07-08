
#encoding:utf-8
# -*- coding:UTF-8 -*-
class ConvertPoints():
    def __init__(self):
        self.h = 300 #cm
        self.unit  = 1.4 #1.4um  像素大小
        self.f = 3.6  # 3.6mm 焦距
        self.ratio = self.h/self.f
        self.defaultWidth = 2592
        self.defaultHeight = 1944
        self.diff = 3 #cm 误差前后10厘米
    

    



    def setScreenSize(self,screenSize):
        self.showWidth = screenSize[0]
        self.showHeight = screenSize[1]
        self.ws= self.defaultWidth/self.showWidth #调整系数
        self.hs= self.defaultHeight/self.showHeight #调整系数
        # 2592 × 1944 像素
        # 3280 × 2464 像素
        self.fullHeight = round(self.showHeight*self.unit*self.ratio/1000/10*self.hs,2)

   
    
    # v 物距   雷达扫描 单位mm
    def convert(self,points):
        realPoints  = []
        pointw = round(points[0]*self.unit*self.ratio/1000/10*self.ws,2)
        pointh = round(points[1]*self.unit*self.ratio/1000/10*self.hs,2)
        realPoints = [pointw,pointh]
        return realPoints
    
    

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
        diff  = 5 #cm
        firstLine = greenLine[0][0][0]
        firstY = firstLine[1]
        print("firstLine",self.fullHeight,firstLine,firstY)
        if(self.fullHeight-diff<=firstY<=self.fullHeight+diff):
            return True
        return False


    def sortGreenLine(self,greenLine,line):
        greenLine.sort(reverse=True)  # False  reverse倒序 
        return greenLine


    def getCenter(self,points):
        xCenter = round((points[1][0] - points[0][0])/2,2)
        yCenter = round((points[2][1] - points[0][1])/2,2)
        center = [xCenter,yCenter]
        return center

    def size(self,px):
        pointw = round(px*self.unit*self.ratio/1000/10*self.ws,2)
        print("pointw",pointw)

if __name__ == "__main__":
    dict = [{'name': 'person 0.35', 'point': [(716, 204), (779, 204), (716, 337), (779, 337)]}, {'name': 'cup 0.36', 'point': [(1, 624), (215, 624), (1, 716), (215, 716)]}, {'name': 'bowl 0.52', 'point': [(3, 624), (210, 624), (3, 710), (210, 710)]}, {'name': 'laptop 0.53', 'point': [(1062, 181), (1279, 181), (1062, 707), (1279, 707)]}, {'name': 'chair 0.68', 'point': [(916, 239), (1085, 239), (916, 535), (1085, 535)]}, {'name': 'cell phone 0.70', 'point': [(1064, 184), (1279, 184), (1064, 704), (1279, 704)]}, {'name': 'person 0.84', 'point': [(202, 1), (990, 1), (202, 716), (990, 716)]}]
    # dict = [{'name': 'cell phone 0.27', 'point': [[189, 448], [353, 448], [189, 713], [353, 713]]},{'name': 'cup 0.79', 'point': [[896, 479], [1249, 479], [896, 719], [1249, 719]]}]
    for item in dict:
        # print (item)
        if (item["name"].find("cup")!=-1):
            cup =  item["point"][1][0]
        elif (item["name"].find("phone")!=-1):
            phone =  item["point"][0][0]
    z =    cup-phone
    print (z)
    cv = ConvertPoints()
    cv.setScreenSize([1280, 720])
    cv.size(z)