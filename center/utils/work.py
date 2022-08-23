class work():
    def __init__(self, point, speed, logger):
        # self.defaultSpeed = 10  # 默认速度
        self.circle_time = 3  # 电机转一圈所需要的时间
        self.point = point
        self.speed = speed
        self.logger = logger.getLogger()
        self.time = 2  # 操作臂每圈所需要的时间
        pass

    def work(self, lineData, machine_speed):
        print("machine_speed--------------------", machine_speed)
        cmd = ""
        if (lineData and lineData[0]):
            length = len(lineData)
            line1 = lineData[length-1]
            line2 = []
            if (length > 1):
                line2 = lineData[length-2]
            y1 = self.getCenterY(line1)
            y2 = self.getCenterY(line2)
            diffPointer = abs(y1-y2)
            diff_distance = self.point.sizey(diffPointer, 45)
            wheel_speed = 10
            wheel_speed = self.get_speed(diff_distance, machine_speed)
            self.logger.info("work:y1,y2, diffPointer, diff_distance,wheel_speed:--%s,%s,%s,%s,%s",
                             y1, y2, diffPointer, diff_distance, wheel_speed)
            cmd = "ROT " + str(int(wheel_speed))
        return cmd

    def get_speed(self, distance, machine_speed):
        min_time = 1.225  # 1秒 1.225圈
        unit = 1/min_time  # 1圈  unit 秒
        max_speed = 255
        time = distance/machine_speed
        speed = unit * max_speed / time
        return int(speed)

    def getCenterY(self, line):
        if (len(line) > 0):
            return line[0]["centery"]
            # return (line[0]["point"][0][1] + line[0]["point"][2][1])/2
        else:
            return 1000
        # pass
