# import serial
# import time  # 导入serial模块
# # port = "/dev/ttyACM0"  # Arduino端口
# # port = "/dev/tty.usbmodem14101"  # Arduino端口
# port = "/dev/tty.usbmodem14201"  # Arduino端口
# ser = serial.Serial(port, 9600, timeout=1,dsrdtr=False)  # 设置端口，每秒回复一个信息
# # ser.flushInput()  # 清空缓冲器

# # __init__( port=None , baudrate=9600 , bytesize=EIGHTBITS , parity=PARITY_NONE , stopbits=STOPBITS_ONE 
# #         , timeout=None , xonxoff=False , rtscts=False , write_timeout=None , dsrdtr=False ,
# #          inter_byte_timeout=None , Exclusive= None )


# ser.port = port
# ser.baudrate = baud
# ser.timeout = 1
# ser.setDTR(False)
# ser.open()


# try:
#     while True:
#         time.sleep(0.5)


#         cmd1 = 'MF 30.'
#         ser.write(cmd1.encode('utf-8'))  # 将'1'字符转换为字节发送
#         response1 = ser.readall()
#         print("response1:",response1)


#         # time.sleep(0.5)

#         # cmd2 = 'TL 10.'
#         # ser.write(cmd2.encode('utf-8'))  # 将'1'字符转换为字节发送
#         # response2 = ser.readall()
#         # print("response2:",response2)

# except Exception as e:
#     print("连接失败！", e)
#     ser.close()  # 关闭端口



from utils.redis_message_queue import RMQ

rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')


if __name__ == '__main__':
    print(rmq.publish('RST.'))
    # rmq.run_subscribe()


