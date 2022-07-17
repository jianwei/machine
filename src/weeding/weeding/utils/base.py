import rclpy,os,sys,yaml,time,threading
class base ():
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("新节点：%s" % name)
        self.redis = redisDB()
        
        # ros2 topic pub --once /camera_open std_msgs/msg/String 'data: "1"'
        # self.create_subscription(String, "camera_open", self.msg_camera_open_callback, 0)
        self.workDir = os.getcwd()   # src目录
        with open(self.workDir+'/weeding/weeding/config.yaml',encoding='utf-8') as file1:
            self.config = yaml.load(file1,Loader=yaml.FullLoader)#读取yaml文件
        self.config["redisObj"] =  self.redis
        self.cameraObj  = camera(self.redis,self.config)
        self.config["cameraObj"] = self.cameraObj 