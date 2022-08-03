# from convertPoints import ConvertPoints
import time,os,sys,serial,json
# import json
sys.path.append("..")
from redisConn.index import redisDB
# chmod -R 777 /dev/ttyAMA0
# import serial,sys,os,redis,time

class machine ():
    def __init__(self):
        self.redis = redisDB()
        self.default_speed = 10
        # self.ser = serial.Serial('/dev/ttyAMA0', 9600,timeout=0.5)
        # self.convertPoints = ConvertPoints()


    def send_cmd(self,cmd):
        # self.ser.write(cmd)
        try:    
            # response = self.ser.readall() #read a string from port
            print ("serial_control:cmd",cmd)
        except expression:
            print("serial_control,expression:",cmd,expression)



    
    def loop(self):
        mock= [ 
            [{'point': [[310, 145], [1039, 145], [310, 714], [1039, 714]], 'id': 14, 'name': 'person', 'time': 1659515712.9082823, 'screenSize': [1080, 720]}],
            [{'point': [[329, 131], [1067, 131], [329, 715], [1067, 715]], 'id': 14, 'name': 'person', 'time': 1659515712.6249225, 'screenSize': [1080, 720]}],
            [{'point': [[355, 127], [1074, 127], [355, 712], [1074, 712]], 'id': 14, 'name': 'person', 'time': 1659515712.353984, 'screenSize': [1080, 720]}],
            [{'point': [[354, 120], [1075, 120], [354, 716], [1075, 716]], 'id': 14, 'name': 'person', 'time': 1659515712.081453, 'screenSize': [1080, 720]}],
            [{'point': [[359, 125], [1073, 125], [359, 715], [1073, 715]], 'id': 14, 'name': 'person', 'time': 1659515711.8160756, 'screenSize': [1080, 720]}],
            [{'point': [[364, 129], [1078, 129], [364, 715], [1078, 715]], 'id': 14, 'name': 'person', 'time': 1659515711.5396397, 'screenSize': [1080, 720]}],
            [{'point': [[354, 269], [760, 269], [354, 714], [760, 714]], 'id': 14, 'name': 'person', 'time': 1659515711.2633321, 'screenSize': [1080, 720]}],
            [{'point': [[301, 355], [706, 355], [301, 716], [706, 716]], 'id': 14, 'name': 'person', 'time': 1659515711.0012357, 'screenSize': [1080, 720]}],
            [{'point': [[312, 403], [729, 403], [312, 716], [729, 716]], 'id': 14, 'name': 'person', 'time': 1659515710.7441657, 'screenSize': [1080, 720]}],
            [{'point': [[186, 443], [610, 443], [186, 718], [610, 718]], 'id': 14, 'name': 'person', 'time': 1659515710.478745, 'screenSize': [1080, 720]}],
            [{'point': [[203, 411], [617, 411], [203, 715], [617, 715]], 'id': 14, 'name': 'person', 'time': 1659515710.2219586, 'screenSize': [1080, 720]}],
            [{'point': [[251, 353], [665, 353], [251, 716], [665, 716]], 'id': 14, 'name': 'person', 'time': 1659515709.9528716, 'screenSize': [1080, 720]}],
            [{'point': [[271, 333], [679, 333], [271, 716], [679, 716]], 'id': 14, 'name': 'person', 'time': 1659515709.6865573, 'screenSize': [1080, 720]}],
            [{'point': [[286, 321], [684, 321], [286, 715], [684, 715]], 'id': 14, 'name': 'person', 'time': 1659515709.4055076, 'screenSize': [1080, 720]}],
            [{'point': [[289, 314], [700, 314], [289, 716], [700, 716]], 'id': 14, 'name': 'person', 'time': 1659515709.1500921, 'screenSize': [1080, 720]}],
            [{'point': [[287, 311], [699, 311], [287, 717], [699, 717]], 'id': 14, 'name': 'person', 'time': 1659515708.8671112, 'screenSize': [1080, 720]}],
            [{'point': [[293, 334], [697, 334], [293, 716], [697, 716]], 'id': 14, 'name': 'person', 'time': 1659515708.6087961, 'screenSize': [1080, 720]}],
            [{'point': [[290, 615], [564, 615], [290, 719], [564, 719]], 'id': 10, 'name': 'person', 'time': 1659515705.1807458, 'screenSize': [1080, 720]}],
            [{'point': [[267, 591], [598, 591], [267, 719], [598, 719]], 'id': 10, 'name': 'person', 'time': 1659515704.9241168, 'screenSize': [1080, 720]}],
            [{'point': [[210, 523], [568, 523], [210, 716], [568, 716]], 'id': 10, 'name': 'person', 'time': 1659515704.6700547, 'screenSize': [1080, 720]}],
            [{'point': [[210, 510], [578, 510], [210, 716], [578, 716]], 'id': 10, 'name': 'person', 'time': 1659515704.4159667, 'screenSize': [1080, 720]}],
            [{'point': [[208, 504], [588, 504], [208, 718], [588, 718]], 'id': 10, 'name': 'person', 'time': 1659515704.1587694, 'screenSize': [1080, 720]}]
        ]
        print(mock)
        while (1):
            # key = "allPoints"
            # allPhoto = self.redis.get(key)
            allPhoto = mock
            print("time:",time.time())
            
            time.sleep(1)



        pass

    


if __name__ == "__main__":
    m = machine()
    # m.scan()
    m.loop()
