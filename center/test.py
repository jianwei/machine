import serial #导入serial模块
port = "/dev/ttyACM0" #Arduino端口
ser = serial.Serial(port,9600,timeout=1) #设置端口，每秒回复一个信息
ser.flushInput() #清空缓冲器

try:
	while True:
		ser.write(b'1') #将'1'字符转换为字节发送
		response = ser.read()
		print(var(response))
except:
	print("连接失败！")
	ser.close()	#关闭端口
