import serial,json,sys,os

def main():
    str_cmd = "MF 50"
    ser = serial.Serial('/dev/ttyACM0', 9600,timeout=0.5)
    ser.write(str_cmd)
    try:    
        response = ser.readall().decode('utf-8');#read a string from port
        print("response",response.decode('utf-8') );
    except expression:
        print("serial_control,expression:",cmd,expression)
    pass

if __name__ == "__main__":
    main()