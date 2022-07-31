import cv2
from csi_camera import CSICamera

camera = CSICamera(width=1080, height=720, capture_width=1080, capture_height=720, capture_fps=30)

video_capture = camera.cap
window_title = "CSI Camera"
if video_capture.isOpened():
    try:
        window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
        while True:
            frame = camera._read()
            if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                cv2.imshow(window_title, frame)
            else:
                break 
            keyCode = cv2.waitKey(10) & 0xFF
            if keyCode == 27 or keyCode == ord('q'):
                break
    finally:
        video_capture.release()
        cv2.destroyAllWindows()
else:
    print("Error: Unable to open camera")