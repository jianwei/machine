#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32
import os




class goNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.create_subscription(UInt32,"wheel_action_go",self.recv_wheel_go_callback,0)
    

    def recv_wheel_go_callback(self,message):
        self.get_logger().info("recv_wheel_go_callback %s" % message.data)
        filename = "lock.file"
        if(not os.path.exists(filename)):
            os.mknod("lock.file")
        self.get_logger().info("----------------go------------")
        while (True):
            if(not os.path.exists(filename)):
                break

        self.get_logger().info("----------------end------------")

                
        

    

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = goNode("wheel_node_go")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy