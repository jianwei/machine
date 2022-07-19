#!/usr/bin/env python3
import json
import rclpy,os,sys,yaml,time,threading
from rclpy.node import Node
from std_msgs.msg import String
sys.path.append(os.getcwd()+"/montor/montor/")
from utils.wedding import wedding_motor 
sys.path.append(os.getcwd()+"/../")
from redisConn.index import redisDB

class motorNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.redis = redisDB()
        self.wedding_motor = wedding_motor()
        # ros2 topic pub --once /motor_run std_msgs/msg/String 'data: "{\"type\":1,\"number\":1,\"angle\":1,\"direction\":2}"'
        self.create_subscription(String, "motor_run", self.msg_motor_run_callback, 0)
        
        
    def msg_motor_run_callback(self,message):
        dict = json.loads(message.data)
        self.get_logger().info("msg.data：%s" % message.data)
        if(dict.type==1):   #除草电机
            self.wedding_motor.run(dict)
        if(dict.type==2):   #除草头左右电机
            self.wedding_motor.run(dict)
        if(dict.type==3):   #除草头上下电机
            self.wedding_motor.run(dict)

        
        
    

   
def main(args=None):
    rclpy.init(args=args)  
    node = motorNode("motor_node")  
    rclpy.spin(node) 
    rclpy.shutdown()  
