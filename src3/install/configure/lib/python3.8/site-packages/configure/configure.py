#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import yaml
import os
from std_msgs.msg import String
import time

class configure(Node):

    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("新节点:%s" % name)
        fs = open(os.path.join(os.getcwd(),("./configure/configure/config.yaml")),encoding="UTF-8")
        datas = str(yaml.load(fs,Loader=yaml.FullLoader)) 
        time.sleep(5)  #5s 后发布消息,配置信息
        msg = String()
        msg.data = datas
        pub_novel = self.create_publisher(String,"machine_config", 1000)
        pub_novel.publish(msg)

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = configure("configure_node")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy