#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32
import os




class stopNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.create_subscription(UInt32,"wheel_action_stop",self.recv_wheel_go_callback,0)
    

    def recv_wheel_go_callback(self,message):
        self.get_logger().info("recv_wheel_stop_callback %s" % message.data)
        filename = "lock.file"
        self.get_logger().info("remove file begin-----------------")
        if( os.path.exists(filename)):
            os.remove("lock.file")
        self.get_logger().info("remove file end-----------------")

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = stopNode("wheel_node_stop")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy