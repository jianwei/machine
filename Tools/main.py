# encoding: utf-8
'''
    所有的长度 单位都是厘米
'''
import time,os,sys,yaml
from utils.camera import camera 
from utils.speed import speed 
from utils.point import point 
from utils.line import line 
from tools.weeding import weeding 
from tools.slide import slide 
sys.path.append("..")
from redisConn.index import redisDB
class main():
    
    def __init__(self):
        self.redis = redisDB()
        with open('config.yaml',encoding='utf-8') as file1:
            self.config = yaml.load(file1,Loader=yaml.FullLoader)#读取yaml文件
        self.config["redisObj"] =  self.redis
        self.cameraObj  = camera(self.redis,self.config)
        self.config["cameraObj"] = self.cameraObj 
        pass

    

    def do(self):
        pass
        # speeding = self.speedObj.speed()
        # print("speeding",speeding)


    def camera (self):
        # dict = [{'name': 'tv 0.35', 'point': [(248, 128), (464, 128), (248, 276), (464, 276)]}]
        photo = dict = [
                        {'name': 'tv 0.75', 'point': [(50, 330), (70, 330), (50, 310), (50, 310)]},
                        {'name': 'tv 0.35', 'point': [(230, 330), (250, 330), (230, 310), (250, 310)]},
                        {'name': 'tv 0.15', 'point': [(410, 330), (430, 330), (410, 310), (430, 310)]},


                        {'name': 'tv 0.75', 'point': [(50, 230), (70, 230), (50, 210), (50, 210)]},
                        {'name': 'tv 0.35', 'point': [(230, 230), (250, 230), (230, 210), (250, 210)]},
                        {'name': 'tv 0.15', 'point': [(410, 230), (430, 230), (410, 210), (430, 210)]},

                        {'name': 'tv 0.75', 'point': [(50, 430), (70, 430), (50, 410), (50, 410)]},
                        {'name': 'tv 0.35', 'point': [(230, 430), (250, 430), (230, 410), (250, 410)]},
                        {'name': 'tv 0.15', 'point': [(410, 430), (430, 430), (410, 410), (430, 410)]},
                        
                       ]
        self.cameraObj.add(photo)
        pass


    def loop(self):
        isSliding = False   #只有第一次校准
        # while True : 
        screen = self.config.get("camera").get("screen")
        self.cameraObj.setScreenSize(screen)
        self.line  = line(self.config)
        self.greenline = self.line.getLine()
        # print(self.line.getLine())
        #除草头校准
        if(not isSliding):  
            self.slide = slide(self.config)
            self.slide.adjust(self.greenline,screen)
            self.slide.insert()  # 插入土中
            isSliding = True
        #除草头工作
        self.weeding = weeding(self.config,self.greenline,10)
        # self.weeding.calculate(self.greenline)
        pass
    





if __name__ == "__main__":
    main = main()
    main.loop()
    pass
    # opt = parse_opt()
    # main(opt)