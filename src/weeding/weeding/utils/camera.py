import time,json,os,threading

class camera ():
    def __init__(self,redis,config):
        self.redis = redis
        self.config = config
        self.key = config.get("redis").get("camera")
        self.h = config.get("camera").get("height") #cm
        self.unit  = config.get("camera").get("unit") #1.12um  像素大小
        self.f = config.get("camera").get("f")  # 3.04mm 焦距
        self.ratio = self.h/self.f
        self.defaultWidth = config.get("camera").get("defaultScreen")[0]
        self.defaultHeight = config.get("camera").get("defaultScreen")[1]
        self.cameralength = 200
        self.allPhoto = []
        pass

    
    def open(self):
        cmd = "python3 "+os.getcwd()+"/../yolov5/detect.py --source 0  --weight yolov5s.pt --conf 0.25 &" 
        os.system(cmd)
        time.sleep(10)
        screen = self.config.get("camera").get("screen")
        self.setScreenSize(screen)
        while (True):
            self.add()
            time.sleep(1)

    def setScreenSize(self,screenSize):
        self.showWidth = screenSize[0]
        self.showHeight = screenSize[1]
        self.ws= self.defaultWidth/self.showWidth #调整系数
        self.hs= self.defaultHeight/self.showHeight #调整系数
       
    
    #px 转化为距离
    def sizex(self,px):
        pointx = round(px*self.unit*self.ratio/1000*self.ws,2)
        print("pointx",pointx)
        return pointx

    
    #px 转化为距离
    def sizey(self,px):
        pointy = round(px*self.unit*self.ratio/1000*self.hs,2)
        # print("pointy",pointy)
        return pointy

    def distanceToPointy(self,distance):
        defaultPx = round((distance * self.f*1000/self.h)/self.unit,2)
        return int(defaultPx/self.hs)

    def distanceToPointx(self,distance):
        defaultPx = round((distance * self.f*1000/self.h)/self.unit,2)
        return int(defaultPx/self.ws)
    
    def add(self):
        value = self.redis.get("camera")
        photo = self.redis.get("singlephoto") 
        if value:
            allPhoto = json.loads(value)
        else:
            allPhoto = []
        if(not allPhoto or len(allPhoto)==0):
            allPhoto = []
        if len(allPhoto) >self.cameralength:
            allPhoto = allPhoto[:self.cameralength]
        allPhoto.insert(0,photo)
        # for item in allPhoto:
        #     print("item---->",item)
        
        self.redis.set("camera",json.dumps(allPhoto))
        self.allPhoto = allPhoto
        pass
    
    def calDistance(self):
        last =  self.allPhoto[0]

