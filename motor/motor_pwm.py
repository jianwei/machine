

# import RPi.GPIO as GPIO
# import time
# class stepper_motor():
#     '''
#         Test script for step motor HW23-601 (https://www.mouser.com/c/?q=HW23-601) 
#         with driver STR2 (https://www.applied-motion.com/products/stepper-drives/str2)
#     '''
#     num_of_steps_for_360 = 2000                 # this could be changed, please see the totorial of STR2/4
#     resolution = num_of_steps_for_360 / 360     # resolution, how many steps would trigger 1 degree rotation
#     CW_control_port = 30                        # GPIO 21 for clockwise (physically connected to dir+ port in the driver)
#     CCW_control_port = 31                       # GPIO 18 for counter clockwise (physically connected to step+ port in the driver)
#     inner_speed = 120                           # rotation speed: 120 rpm, outer would be 30 rpm
#     gear_ratio = 4                              # radius of the outer gear is 4 times than the radius of the inner gear
#     outer_speed = inner_speed / gear_ratio      # acutal speed: 30 rpm, that means it will take around 1 second to rotate 180 degree
#     cur_position = 0
#     # delay = 1 / 2 * (num_of_steps_for_360 * inner_speed / 60) 
#     delay = 0.00075
#     name = 'stepper_motor'

#     def __init__(self):
#         # self.log = log
#         GPIO.setmode(GPIO.BCM)                                    # set the GPIO mode  
#         GPIO.setup(self.CCW_control_port, GPIO.OUT)               # set GPIO 18 as output
#         GPIO.setup(self.CW_control_port, GPIO.OUT)                # set GPIO 21 as output
#         time.sleep(0.5) 
#         print("stepper motor initialization accomplished, outer speed: %d rpm, resolution: %d steps/degree" % (self.outer_speed, self.resolution))

#     def __del__(self):
#         GPIO.cleanup()

#     def send_pulse(self, num_of_pulse, control_port):
#         print('send pulse: %d' % num_of_pulse)
#         time.sleep(10 / 1000)
#         for i in range(int(num_of_pulse)):
#             GPIO.output(control_port, GPIO.HIGH)
#             time.sleep(self.delay)
#             GPIO.output(control_port, GPIO.LOW)
#             time.sleep(self.delay)
#         print('send pulse done')

#     def move(self, angle, direction):
#         num_of_steps = self.resolution * angle * self.gear_ratio  # gear ratio is 4, so the outer speed is 1/4 of inner gear, need more pulse
#         angle = -angle if direction == 'CCW' else angle           # decrease the angle if direction is CCW
#         self.cur_position += angle
#         print('start to move：',self.cur_position)
#         if self.cur_position > 360 or self.cur_position < -360:
#             print("rotation angle will exceeded 360 degree, wire might get twisted, current movement cancelled")
#             print("movement: <moved %d degree, direction:%s> has been cancelled" % (angle, direction))
#             self.cur_position -= angle
#             return False
#         else:
#             if direction == 'CW':
#                 self.send_pulse(num_of_steps, self.CW_control_port)
#             else:
#                 self.send_pulse(num_of_steps, self.CCW_control_port)
#             print("moved %d degree, direction:%s, current position: %d" % (angle, direction, self.cur_position))
#             print('move done')
#             return True
        
#     def get_motor_type(self):
#         return self.name

# m = stepper_motor()
# m.send_pulse(1000,31)
# m.move(120, 'CW')


 
import RPi.GPIO as GPIO
import time
 
pul = 26
dir = 19
ena = 13
motor_forward = GPIO.HIGH
motor_back = GPIO.LOW
 
 
def init_pin():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    # 设置PUL,DIR,ENA 端口模式为输出
    GPIO.setup(pul,GPIO.OUT)
    GPIO.setup(dir, GPIO.OUT)
    GPIO.setup(ena, GPIO.OUT)
    print('初始化')
    GPIO.setup(ena, GPIO.LOW)
 
 
def motor(speed,direction):
    # 电机1 pwm 实例化 并设置速度
    pwm_motor = GPIO.PWM(pul, speed)
    # 设置初始占空比
    pwm_motor.start(50)
    # 设置方向
    GPIO.setup(dir, direction)
    # 打开使能端口
    GPIO.setup(ena, GPIO.HIGH)
 
 
if __name__ == '__main__':
    init_pin()
    motor(speed=1000,direction=motor_forward)
    time.sleep(10)
    # 停止，通过使能端，也可以重新设置pwm
    GPIO.setup(ena, GPIO.LOW)
    print('电机停止')
