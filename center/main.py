import sys, os
sys.path.append("..")
from redisConn.index import redisDB



class mainfunc () :
    def __init__(self):
        self.redis = redisDB()
        # self.redis.set("user","chenjianwei")
        # v = self.redis.get("user")
        # print(v)
        # pass

    def loop(self):
        distance = self.getDistance()

    def getGreen():
        pass
    

    def getDistance(self):
        distance = self.redis.get("distance")
        return distance

    
    

if __name__ == "__main__":
        s = mainfunc()


    
    # rclpy.init(args=args)  # 初始化rclpy
    # node = goNode("wheel_node_go")  # 新建一个节点
    # rclpy.spin(node)  # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    # rclpy.shutdown()  # 关闭rclpy