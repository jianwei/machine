#!/usr/bin/env python3
import rclpy,os,sys,yaml,time,_thread
from rclpy.node import Node
from std_msgs.msg import UInt32
from std_msgs.msg import String
sys.path.append(os.getcwd()+"/weeding/weeding/")
from utils.camera import camera 
sys.path.append(os.getcwd()+"/../")
from redisConn.index import redisDB

class cameraNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.redis = redisDB()
        
        # ros2 topic pub --once /camera_open std_msgs/msg/String 'data: "1"'
        self.create_subscription(String, "camera_open", self.msg_camera_open_callback, 0)
        self.workDir = os.getcwd()   # src目录
        with open(self.workDir+'/weeding/weeding/config.yaml',encoding='utf-8') as file1:
            self.config = yaml.load(file1,Loader=yaml.FullLoader)#读取yaml文件
        self.config["redisObj"] =  self.redis
        self.cameraObj  = camera(self.redis,self.config)
        self.config["cameraObj"] = self.cameraObj 
        


    def msg_camera_open_callback(self,message):
        # print("msg_camera_open_callback")
        self.get_logger().info("msg.data：%s" % message.data)
        if(int(message.data)==1):
            #1. 打开摄像头
            self.cameraObj.open()
        pass
    

   
def main(args=None):
    rclpy.init(args=args)  
    node = cameraNode("camera_node")  
    rclpy.spin(node) 
    rclpy.shutdown()  
