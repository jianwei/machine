#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32
from std_msgs.msg import String


class weedingNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)

        self.create_subscription(String, "machine_prepare", self.recv_machine_prepare_callback, 0)

        # self.create_subscription(
        #     String, "machine_config", self.recv_machine_config_callback, 0)

    def recv_machine_prepare_callback(self,message):
        self.get_logger().info("recv_machine_prepare_callback: %s" % message.data)

   
def main(args=None):
    rclpy.init(args=args)  # 初始化rclpy
    node = weedingNode("weeding_node")  # 新建一个节点
    rclpy.spin(node)  # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown()  # 关闭rclpy
