
import json
# from point import pointd 
class speed ():
    def __init__(self,redis,point):
        self.defaultSpeed = 0
        self.redis = redis
        self.speed = 2
        self.point  = point
        pass

    def speed (self):   
        return 10
    
    def calculate(self):
        camera = self.redis.get("camera")
        camera = [] if ( not camera) else json.loads(camera)
        first  = camera[0][0]
        last  = camera [len(camera)-1][0]
        if (not first or not last):
            self.speed = 0
            return self.speed
        else:
            firstTime =  first["time"]
            firstPoint = first["point"][0][1]
            lastTime = last["time"]
            lastPoint = last["point"][0][1]

        speed = (self.point.sizey(firstPoint) - self.point.sizey(lastPoint)) / (firstTime-lastTime)
        print (firstPoint)
        print (lastPoint)
        # print (firstPoint)
        # print (firstPoint)
        print(speed)
        return round(speed,2)
        # pass