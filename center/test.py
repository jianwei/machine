# import serial

# def main():
#     str_cmd = "MF 10."
#     ser = serial.Serial('/dev/ttyACM0', 9600,timeout=0.5)
#     ser.write(str_cmd.encode())
#     try:
#         while 1:
#             response = ser.readall().decode('utf-8')
#             print("response",response)
#     except expression:
#         print("serial_control,expression:",cmd,expression)
#     pass

# if __name__ == "__main__":
#     main()

import serial  # import serial module
ser = serial.Serial('/dev/ttyACM0', 230400, timeout=0.5)
open = ser.isOpen()
print("isopen1:", open)
try:
    while 1:
        str_cmd = b'MF 10.'
        w = ser.write(str_cmd)
        print("isopen,w:", open, w)
        response = ser.readall()
        print("response:", response)
        # print("response:",response.decode('utf-8') )
except Exception as e:
    print("exception:", e)
    ser.close()
