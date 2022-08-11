import serial

def main():
    str_cmd = "MF 10."
    ser = serial.Serial('/dev/ttyACM0', 9600,timeout=0.5)
    ser.write(str_cmd.encode())
    try:    
        response = ser.readall().decode('utf-8')
        print("response",response)
    except expression:
        print("serial_control,expression:",cmd,expression)
    pass

if __name__ == "__main__":
    main()