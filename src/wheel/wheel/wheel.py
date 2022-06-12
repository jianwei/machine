#!/usr/bin/env python3
from math import fabs
from tkinter import W
import rclpy
import os
from rclpy.node import Node
from std_msgs.msg import String,UInt32
import time
# import pigpio



class WheelNode(Node):
  
    def __init__(self,name):
        super().__init__(name)
        self.lockfilename = "lockfile.lock"
        # 1 go , 0 stop , 2 back
        self.get_logger().info("新节点：%s" % name)
        self.create_subscription(UInt32,"wheel_action_go",self.recv_wheel_go_callback,0)
        self.create_subscription(UInt32,"wheel_action_stop",self.recv_wheel_stop_callback,0)
        # pi = pigpio.pi()
        # if not pi.connected:      # 检查是否连接成功
        #     print("pigpio not connected.")
        #     exit()
        # pi.set_mode(18, pigpio.OUTPUT)  # 设置引脚18输出
        # pi.set_mode(26, pigpio.OUTPUT)
        # pi.set_mode(7, pigpio.OUTPUT)  # 设置引脚7输出
        # pi.write(7, 1)  # 设置引脚7高电平，引脚7是刹车，如果输入低电平则刹车

        # pi.set_mode(13, pigpio.OUTPUT)  # 设置引脚13输出
        # pi.write(13, 1)  # 设置引脚13高电平，引脚13是刹车，如果输入低电平则刹车

        # pi.set_mode(8, pigpio.OUTPUT)  # 设置引脚8输出
        # pi.write(8, 1)  # 设置引脚8高电平，引脚8控制电机正反向

        # pi.set_mode(19, pigpio.OUTPUT)  # 设置引脚19输出
        # pi.write(19, 0)  # 设置引脚19低电平，引脚19控制电机正反向

        # pi.set_PWM_frequency(18, 50)
        # pi.set_PWM_range(18, 100)
        # pi.set_PWM_dutycycle(18, 5)

        # pi.set_PWM_frequency(26, 50)
        # pi.set_PWM_range(26, 100)
        # pi.set_PWM_dutycycle(26, 5)
        # self.pi = pi
        self.declare_parameter("isGo",False)


    def recv_wheel_go_callback(self,message):
        self.get_logger().info("%s" % message.data)
        self.go()
        


    def recv_wheel_stop_callback(self,message):
        self.get_logger().info("%s----" % message.data)
        self.stop()
       


     # 后退
    def back(self):
        print("action back function")
        self.stop()
        # self.pi.set_mode(8, pigpio.OUTPUT)  # 设置引脚8输出
        # self.pi.write(8, 0)  # 设置引脚8高电平，引脚8控制电机正反向
        # self.pi.set_mode(19, pigpio.OUTPUT)  # 设置引脚19输出
        # self.pi.write(19, 1)  # 设置引脚19低电平，引脚19控制电机正反向
        self.move()

    def go(self):
        self.get_logger().info("action go function")
        self.move()
        pass

      # 移动
    def move(self):
        print("action move function  begin----------"+str(time.time()))
        isGo = self.get_parameter('isGo').get_parameter_value().integer_value
        while(self.isGo):
            print("self.isGo",self.isGo)
            time.sleep(0.5)
        print("action move function  end-----------"+str(time.time()))
        pass


    # 停止
    def stop(self):
        print("action stop function")
        self.isGo = False
        print("action stop function",self.isGo)
        # self.pi.write(7, 0)
        # self.pi.write(13, 0)
        # self.pi.stop()
        pass

    def destroy(self):
        print("action destroy function")
        pass



    def back(self):
        self.isGo = 0
        self.get_logger().info("back",self.isGo )
        pass
    
    
    # def stop(self):
    #     self.get_logger().info("stop" )
    #     pass
 
    



def main(args=None):
    
    rclpy.init(args=args) # 初始化rclpy
    node = WheelNode("wheel")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy

    