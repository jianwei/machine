# coding=utf-8
import cv2
 

def show_camera():
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink", cv2.CAP_GSTREAMER)
 
    while cap.isOpened():
        flag, img = cap.read()
        cv2.imshow("CSI Camera", img)
        kk = cv2.waitKey(1)
        if kk == ord('q'):  
            break
 
    cap.release()
    cv2.destroyAllWindows()
    
 
if __name__ == "__main__":
    show_camera()
