import time
import pigpio


class action():
    def __init__(self):
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

        pi.set_PWM_frequency(26, 50)
        pi.set_PWM_range(26, 100)
        pi.set_PWM_dutycycle(26, 5)
        self.pi = pi

    # 来回走
    # def round(self):
    #     self.go()
    #     self.stop()
    #     self.back()
    #     self.stop()

    # 前进
    def go(self):
        print("action go function")
        self.move()

    # 后退
    def back(self):
        print("action back function")
        self.stop()
        self.pi.set_mode(8, pigpio.OUTPUT)  # 设置引脚8输出
        self.pi.write(8, 0)  # 设置引脚8高电平，引脚8控制电机正反向
        self.pi.set_mode(19, pigpio.OUTPUT)  # 设置引脚19输出
        self.pi.write(19, 1)  # 设置引脚19低电平，引脚19控制电机正反向
        self.move()

    # 移动
    def move(self,sleepTime):
        print("action move function  begin----------"+str(time.time()))
        time.sleep(sleepTime)
        print("action move function  end-----------"+str(time.time()))
        pass

    # 停止
    def stop(self):
        print("action stop function")
        self.pi.write(7, 0)
        self.pi.write(13, 0)
        self.pi.stop()
        # pass

    def destroy(self):
        print("action destroy function")
        pass


if __name__ == "__main__":
    sleepTime = 3
    obj = action()
    try:
        obj.go(sleepTime)
        pass
    except KeyboardInterrupt:
        obj.destroy()
