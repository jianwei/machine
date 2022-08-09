class work():
    def __init__(self,point,speed):
        # self.defaultSpeed = 10  # 默认速度
        self.circle_time = 3  #电机转一圈所需要的时间
        self.point = point
        self.speed = speed
        pass

    def work(self,lineData):
        cmd = ""
        if(lineData and lineData[0]):
            length = len(lineData)
            line1 = lineData[length-1]
            line2 = []
            if(length>1):
                line2 = lineData[length-2]
            y1 = self.getCenterY(line1)
            y2 = self.getCenterY(line2)
            diffPointer = abs(y1-y2)
            diff_distance = self.point.sizey(diffPointer,45)
            cmd = "ROT 0"
            print ("line1",line1,y1,diffPointer,diff_distance)
            # print ("line2",line2,y2,diffPointer,diff_distance)
            # pass
        return cmd
        

    def getCenterY(self,line):
        if(len(line)>0):
            return line[0]["centery"]
        else: 
            return 2000
        # pass

