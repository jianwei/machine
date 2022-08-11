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

import serial    #import serial module
ser = serial.Serial('/dev/ttyACM0', 9600,timeout=0.5);   #open named port at 9600,1s timeot
ser.flushInput()
try:
  while 1:
    ser.write('s'.encode());
    size = ser.inWaiting()
    print("size:",size)
    if size != 0:
        response = ser.read(size)
        print(response)
    print("response:",response.decode('utf-8') )
except:
  ser.close()
