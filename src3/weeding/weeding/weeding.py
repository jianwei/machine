#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32
from std_msgs.msg import String


class weedingNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        # ros2 topic pub --once /machine_prepare std_msgs/msg/UInt32  "{data: 1}"
        self.create_subscription(String, "machine_prepare", self.recv_machine_prepare_callback, 0)

    def recv_machine_prepare_callback(self,message):
        self.get_logger().info("recv_machine_prepare_callback: %s" % message.data)

   
def main(args=None):
    rclpy.init(args=args)  
    node = weedingNode("weeding_node")  
    rclpy.spin(node) 
    rclpy.shutdown()  
