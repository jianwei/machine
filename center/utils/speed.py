
import json
# from point import pointd 
class speed ():
    def __init__(self):
        self.defaultSpeed = 10
        pass
    
    def calculate(self,data):
        if (len(data)>1):
            first  = data[0]
            second  = data [1]
            print ("first",first)
            print ("second",second)
            # firstTime =  first["time"]
            # firstPoint = first["point"][0][1]
            # secondTime = second["time"]
            # secondPoint = second["point"][0][1]

            # speed = (secondPoint - firstPoint) / (secondTime-firstTime)
            # print(speed)
            # return round(speed,2)
        else:
            return self.defaultSpeed
        # pass