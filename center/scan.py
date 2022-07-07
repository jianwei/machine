
import os
class scan():
    def __init__(self):
        # self.scan()
        print("scan")
        pass

    def scan(self):
        # os.system('cd ../yolov5')
        os.system(' cd ../yolov5 && python3 detect.py --source 0  --weight yolov5s.pt --conf 0.25')
        # os.system('python3 ../yolov5/detect.py --source 0  --weight yolov5s.pt --conf 0.25')
        # print val
        pass