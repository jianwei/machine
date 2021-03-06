#!/usr/bin/env python3
import json
import rclpy,os,sys,yaml,time,_thread
from rclpy.node import Node
from std_msgs.msg import UInt32
from std_msgs.msg import String
sys.path.append(os.getcwd()+"/../")
from redisConn.index import redisDB
sys.path.append(os.getcwd()+"/weeding/weeding/")
from utils.camera import camera 
from utils.speed import speed 
from utils.line import line 
from tools.weeding import weeding 
from tools.slide import slide 
# from tools.wheel import wheel 



class weedingNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.redis = redisDB()
        
        # ros2 topic pub --once /mock_data std_msgs/msg/String 'data: "1"'
        # self.create_subscription(String, "mock_data", self.msg_mock_data_callback, 0)
        # self.create_subscription(String, "machine_prepare", self.msg_machine_prepare_callback, 0)
        # self.create_subscription(String, "machine_work", self.msg_machine_work_callback, 0)
        # self.create_subscription(String, "machine_stop", self.msg_machine_stop_callback, 0)
        self.create_subscription(String, "open_camera", self.open_camera, 0)
        self.create_subscription(String, "machine_pause", self.meg_machine_pause_callback, 0)
        # self.pub_novel = self.create_publisher(String,"wheel", 10)

        self.workDir = os.getcwd()   # src目录

        with open(self.workDir+'/weeding/weeding/config.yaml',encoding='utf-8') as file1:
            self.config = yaml.load(file1,Loader=yaml.FullLoader)#读取yaml文件
        self.config["redisObj"] =  self.redis
        self.cameraObj  = camera(self.redis,self.config)
        self.config["cameraObj"] = self.cameraObj 
        self.weeding=weeding(self.config)


    # ros2 topic pub --once /open_camera std_msgs/msg/String 'data: "1"'
    def open_camera(self,message):
        self.get_logger().info("open_camera" )
        #1. 打开摄像头
        self.redis.set("open_camera",1)
        time.sleep(10)
        self.loop()
        # self.get_logger().info(os.getcwd())
        # if(int(message.data)==1):
        #     #1. 打开摄像头
        #     self.redis.set("open_camera",1)
            # self.pub_novel.publish(msg)
            # self.cameraObj.open()
            # self.line  = line(self.config)
            # self.greenline = self.line.getLine()
            # #除草头校准
            # self.slide = slide(self.config)
            # self.slide.adjust(self.greenline)
            # self.slide.insert()  # 插入土中
            # #除草头工作
            # self.weeding = weeding(self.config,self.greenline,10)
            # self.get_logger().info("prepare done")

    
    def msg_machine_work_callback(self,message):
        self.get_logger().info("msg_machine_work_callback: %s" % message.data)
        #除草头工作
        self.weeding.run()
        pass

    #ros2 topic pub --once /machine_stop std_msgs/msg/String 'data: "1"'
    def msg_machine_stop_callback(self,message):
        self.get_logger().info("msg_machine_stop_callback: %s" % message.data)
        #停止工作,关闭除草头以及相机
        # self.weeding.stop()
        self.redis.set("open_camera",0)
        self.redis.set("allPoints",json.dumps([]))

    #ros2 topic pub --once /machine_pause std_msgs/msg/String 'data: "1"'
    def meg_machine_pause_callback(self,message):
        self.get_logger().info("meg_machine_pause_callback: %s" % message.data)
        self.redis.set("open_camera",0)
        #暂停工作,关闭除草头
        # self.weeding.pause()
        pass
 

    

    def msg_mock_data_callback (self,message):
        photo = [
                        {'name': 'tv 0.75', 'point': [(50, 330), (70, 330), (50, 310), (50, 310)],'time': 1657954787},
                        {'name': 'tv 0.35', 'point': [(230, 330), (250, 330), (230, 310), (250, 310)],'time': 1657954787},
                        {'name': 'tv 0.15', 'point': [(410, 330), (430, 330), (410, 310), (430, 310)], 'time': 1657954787  },

                        {'name': 'tv 0.75', 'point': [(50, 230), (70, 230), (50, 210), (50, 210)],'time': 1657954787},
                        {'name': 'tv 0.35', 'point': [(230, 230), (250, 230), (230, 210), (250, 210)],'time': 1657954787},
                        {'name': 'tv 0.15', 'point': [(410, 230), (430, 230), (410, 210), (430, 210)],'time': 1657954787},

                        {'name': 'tv 0.75', 'point': [(50, 430), (70, 430), (50, 410), (50, 410)],'time': 1657954787},
                        {'name': 'tv 0.35', 'point': [(230, 430), (250, 430), (230, 410), (250, 410)],'time': 1657954787},
                        {'name': 'tv 0.15', 'point': [(410, 430), (430, 430), (410, 410), (430, 410)],'time': 1657954787},
                ]
        self.get_logger().info("mockdata:%s" % photo)
        self.cameraObj.add(photo)
        pass

    
        
    def loop(self):
        self.get_logger().info("------------------------loop begin-----------------------" )

        while (True):
            allPoints = self.redis.get("allPoints")
            self.get_logger().info(allPoints)
            self.get_logger().info("-------------------------------------loop end-----------------------------------------------" )
            time.sleep(5)

        # isSliding = False   #只有第一次校准
        # while True : 
        # screen = self.config.get("camera").get("screen")
        # self.cameraObj.setScreenSize(screen)
        # self.line  = line(self.config)
        # self.greenline = self.line.getLine()
        # #除草头校准
        # if(not isSliding):  
        #     self.slide = slide(self.config)
        #     self.slide.adjust(self.greenline,screen)
        #     self.slide.insert()  # 插入土中
        #     isSliding = True
        # #除草头工作
        # self.weeding = weeding(self.config,self.greenline,10)
        # self.weeding.run()
        pass
    
    def main(self):
        self.open_camera('')
            
        


   
def main(args=None):
    rclpy.init(args=args)  
    node = weedingNode("weeding_node")
    node.main()  
    rclpy.spin(node) 
    rclpy.shutdown()  
