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
 
     
    def loop(self):
        self.get_logger().info("------------------------loop begin-----------------------" )
        self.line  = line(self.config)
        # eg :[[{"point": [[0, 77], [639, 77], [0, 477], [639, 477]], "id": 1, "name": "person", "time": 1658718413, "screenSize": [640, 480]}], [{"point": [[2, 107], [638, 107], [2, 477], [638, 477]], "id": 1, "name": "person", "time": 1658718412, "screenSize": [640, 480]}], [{"point": [[3, 68], [511, 68], [3, 479], [511, 479]], "id": 1, "name": "person", "time": 1658718411, "screenSize": [640, 480]}, {"point": [[487, 367], [638, 367], [487, 479], [638, 479]], "id": 2, "name": "couch", "time": 1658718411, "screenSize": [640, 480]}], [{"point": [[2, 160], [421, 160], [2, 478], [421, 478]], "id": 1, "name": "person", "time": 1658718410, "screenSize": [640, 480]}, {"point": [[459, 367], [639, 367], [459, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718410, "screenSize": [640, 480]}, {"point": [[326, 318], [343, 318], [326, 341], [343, 341]], "id": 4, "name": "person", "time": 1658718410, "screenSize": [640, 480]}], [{"point": [[46, 150], [481, 150], [46, 479], [481, 479]], "id": 1, "name": "person", "time": 1658718409, "screenSize": [640, 480]}, {"point": [[474, 366], [639, 366], [474, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718409, "screenSize": [640, 480]}], [{"point": [[23, 155], [460, 155], [23, 479], [460, 479]], "id": 1, "name": "person", "time": 1658718408, "screenSize": [640, 480]}, {"point": [[458, 366], [639, 366], [458, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718408, "screenSize": [640, 480]}], [{"point": [[0, 167], [376, 167], [0, 479], [376, 479]], "id": 1, "name": "person", "time": 1658718407, "screenSize": [640, 480]}, {"point": [[457, 366], [639, 366], [457, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718407, "screenSize": [640, 480]}], [{"point": [[2, 166], [361, 166], [2, 479], [361, 479]], "id": 1, "name": "person", "time": 1658718406, "screenSize": [640, 480]}, {"point": [[457, 366], [639, 366], [457, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718406, "screenSize": [640, 480]}], [{"point": [[0, 156], [456, 156], [0, 478], [456, 478]], "id": 1, "name": "person", "time": 1658718405, "screenSize": [640, 480]}, {"point": [[458, 366], [639, 366], [458, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718405, "screenSize": [640, 480]}], [{"point": [[0, 158], [478, 158], [0, 478], [478, 478]], "id": 1, "name": "person", "time": 1658718404, "screenSize": [640, 480]}, {"point": [[477, 367], [639, 367], [477, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718404, "screenSize": [640, 480]}], [{"point": [[0, 152], [423, 152], [0, 479], [423, 479]], "id": 1, "name": "person", "time": 1658718403, "screenSize": [640, 480]}, {"point": [[459, 367], [639, 367], [459, 479], [639, 479]], "id": 2, "name": "couch", "time": 1658718403, "screenSize": [640, 480]}, {"point": [[326, 311], [355, 311], [326, 340], [355, 340]], "id": 4, "name": "person", "time": 1658718403, "screenSize": [640, 480]}]]
        while (True):
            allPoints = json.loads(self.redis.get("allPoints"))
            point = allPoints[0]
            screen = point[0].get("screenSize")
            
            # 分组
            self.cameraObj.setScreenSize(screen)
            self.greenline = self.line.getLine()
            # isSliding = False   #只有第一次校准
            #校正位置
            # if(not isSliding):  
            #     self.slide = slide(self.config)
            #     self.slide.adjust(self.greenline,screen)
            #     self.slide.insert()  # 插入土中
            #     isSliding = True

            #除草
            # self.weeding = weeding(self.config,self.greenline,10)
            # self.weeding.run()


            self.get_logger().info(allPoints)
            self.get_logger().info("-------------------------------------loop end-----------------------------------------------" )
            time.sleep(5)
        pass
    
    def main(self):
        self.open_camera('')
            
        


   
def main(args=None):
    rclpy.init(args=args)  
    node = weedingNode("weeding_node")
    node.main()  
    rclpy.spin(node) 
    rclpy.shutdown()  
