
import json
# from point import pointd 
class speed ():
    def __init__(self,point):
        self.defaultSpeed = 1  # 默认速度
        self.revolution = 12    #默认转速 ，对应默认速度
        self.diffSpeed = 1     # 允许的速度差
        self.point = point
        self.increment= 0        # 速度增量
        pass
    
    def getPointSpeed(self,data):
        length = len(data)
        speed = 0
        index_list = [-1,-1,-1]
        flag = False
        if (length>1):
            for i in range(length-1):
                first  = data[i]
                second  = data [i+1]
                for j in range(len(first)):
                    index = first[j]["id"]
                    for k in range(len(second)):
                        index2 = second[k]["id"]
                        if (index==index2):
                            flag = True
                            index_list[2]=k
                            break
                    if  (flag):
                        index_list[1]=j
                        break   
                if (flag):
                    index_list[0]=i
                    break
            print("index_list",index_list)    
            speed = self.getrealspeed(data,index_list)
            return speed
        else:
            return self.defaultSpeed

    #确保匀速行驶 转速　
    def uniformSpeed(self,speed):
        # revolution = self.revolution
        if(speed-self.defaultSpeed < self.diffSpeed) :  #加速
            self.revolution += self.increment
        elif (speed-self.defaultSpeed > self.diffSpeed): #减速
            self.revolution -= self.increment
        self.revolution=20 if self.revolution <=20 else self.revolution
        self.revolution=30 if self.revolution >=30 else self.revolution
        return self.revolution

    def getSpeed(self,data):
        point_speed = self.getPointSpeed(data)
        speed = 0
        if (point_speed and point_speed>0):
            random = data[0][0]
            screenSize = random["screenSize"]
            self.point.setScreenSize(screenSize)
            speed = self.point.sizey(point_speed,45)
            # print("screenSize,speed",screenSize,speed)
        return speed
    
    def getrealspeed(self,data,index_list):
        index = index_list[0]
        point1 = data[index][index_list[1]]
        point2 = data[index+1][index_list[2]]
        center1 = self.getCenter(point1)
        center2 = self.getCenter(point2)
        diffY = abs(center2[1]-center1[1])
        if (diffY<=0):
            return 0 
        diffTime = point1["time"] - point2["time"]
        if (diffTime<=0):
            return -1
        speed = diffY / diffTime
        return speed
            

    def getCenter(self,point):
        point = point["point"]
        centerx = (point[0][0] + point[1][0])/2 
        centery = (point[0][1] + point[3][1])/2 
        return [centerx,centery]
