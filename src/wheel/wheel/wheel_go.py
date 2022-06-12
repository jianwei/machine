#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32
import os
import pigpio




class goNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.create_subscription(UInt32,"wheel_action_go",self.recv_wheel_go_callback,0)
        pi = pigpio.pi()
        if not pi.connected:      # 检查是否连接成功
            print("pigpio not connected.")
            exit()
        pi.set_mode(18, pigpio.OUTPUT)  # 设置引脚18输出
        pi.set_mode(26, pigpio.OUTPUT)
        pi.set_mode(7, pigpio.OUTPUT)  # 设置引脚7输出
        pi.write(7, 1)  # 设置引脚7高电平，引脚7是刹车，如果输入低电平则刹车

        pi.set_mode(13, pigpio.OUTPUT)  # 设置引脚13输出
        pi.write(13, 1)  # 设置引脚13高电平，引脚13是刹车，如果输入低电平则刹车

        pi.set_mode(8, pigpio.OUTPUT)  # 设置引脚8输出
        pi.write(8, 1)  # 设置引脚8高电平，引脚8控制电机正反向

        pi.set_mode(19, pigpio.OUTPUT)  # 设置引脚19输出
        pi.write(19, 0)  # 设置引脚19低电平，引脚19控制电机正反向

        pi.set_PWM_frequency(18, 50)
        pi.set_PWM_range(18, 100)
        pi.set_PWM_dutycycle(18, 5)

        # pi.set_PWM_frequency(26, 50)
        # pi.set_PWM_range(26, 100)
        # pi.set_PWM_dutycycle(26, 5)
        self.pi = pi
        
    

    def recv_wheel_go_callback(self,message):
        self.get_logger().info("recv_wheel_go_callback %s" % message.data)
        filename = "lock.file"
        if(not os.path.exists(filename)):
            os.mknod("lock.file")
        self.get_logger().info("----------------go------------")
        while (True):
            if(not os.path.exists(filename)):
                self.pi.write(7, 0)
                self.pi.write(13, 0)
                self.pi.stop()
                break
        self.get_logger().info("----------------end------------")

                
        

    

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = goNode("wheel_node_go")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy