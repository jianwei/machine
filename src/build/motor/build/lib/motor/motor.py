#!/usr/bin/env python3
import json
import rclpy,os,sys,yaml,time,threading
from rclpy.node import Node
from std_msgs.msg import String
# sys.path.append(os.getcwd()+"/weeding/weeding/")
# from utils.camera import camera 
sys.path.append(os.getcwd()+"/../")
from redisConn.index import redisDB

class motorNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.redis = redisDB()
        
        # ros2 topic pub --once /motor_run std_msgs/msg/String 'data: "{type:1,number:1, angle:1 ,direction:2}"'
        self.create_subscription(String, "motor_run", self.msg_camera_open_callback, 0)
        
        
    def msg_camera_open_callback(self,message):
        dict = json.loads(message.data)

        self.get_logger().info("msg.data：%s" % message.data)

        # a="{type:1,number:1,angle:1,direction:2}"
        # self.get_logger().info (a)
        self.get_logger().info ("type:%s"%dict["type"])
        self.get_logger().info ("number:%s"%dict["number"])
        self.get_logger().info ("angle:%s"%dict["angle"])
        self.get_logger().info ("direction:%s"%dict["direction"])
        # print (json.loads(a))
        # data = json.loads(message.data)
        # self.get_logger().info("msg.data：%s" % data)
        
    

   
def main(args=None):
    rclpy.init(args=args)  
    node = motorNode("motor_node")  
    rclpy.spin(node) 
    rclpy.shutdown()  
