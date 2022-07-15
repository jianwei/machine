#!/usr/bin/env python3
import rclpy,os
from rclpy.node import Node
from std_msgs.msg import UInt32
from std_msgs.msg import String


class weedingNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.create_subscription(String, "machine_prepare", self.recv_machine_prepare_callback, 0)
        self.workDir = os.getcwd()   # src目录


    # ros2 topic pub --once /machine_prepare std_msgs/msg/String 'data: "1"'
    def recv_machine_prepare_callback(self,message):
        self.get_logger().info("recv_machine_prepare_callback: %s" % message.data)
        self.get_logger().info(os.getcwd())
        if(int(message.data)==1):
            #1. 打开摄像头
            self.get_logger().info("open yolov5"  )
            cmd = "python3 "+self.workDir+"/../yolov5/detect.py --source 0  --weight yolov5s.pt --conf 0.25"
            os.system(cmd)
        

            
        


   
def main(args=None):
    rclpy.init(args=args)  
    node = weedingNode("weeding_node")  
    rclpy.spin(node) 
    rclpy.shutdown()  
