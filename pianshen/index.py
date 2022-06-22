import serial
import time

# 基础报文
sendbytes = '01 03 00 40 00 01'
# 生成CRC16校验码
CRC = CRC()
crc, crc_H, crc_L = CRC.CRC16(sendbytes)

# 生成完整报文
sendbytes = sendbytes + ' ' + crc_L + ' ' + crc_H
print(sendbytes)

# 连接端口 'com6', 超时0.8，比特率9600、8字节、无校验、停止位1
com = serial.Serial(port="com6", baudrate=9600, timeout=0.8,
                    bytesize=8, parity='N', stopbits=1)
if com.is_open:
    print("port open success")
    # 将hexstr导入bytes对象  报文需要是字节格式
    sendbytes = bytes.fromhex(sendbytes)
    # 发送报文
    com.write(sendbytes)
    return_res = com.readall()
    print(return_res)
