import cv2
import torch
from PIL import Image
import time

cap = cv2.VideoCapture(0)
print("capture device is open: " + str(cap.isOpened()))
fps_start_time = time.time()
fps=0

# def infence(frame):
#     # Model
#     model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#     img=cv2.imread(frame)[..., ::-1] #BGR to RGB
#     results = model(img, size=640)  # includes NMS
#     results.print()
#     img2=results.save()
#     return img2

while True:

    # img = infence(frame)
    # caculate fps
    success, frame = cap.read()
    fps_end_time = time.time()
    fps_diff_time = fps_end_time - fps_start_time
    fps = 1 / fps_diff_time
    fps_start_time = fps_end_time
    fps_text="FPS:{:.2f}".format(fps)
    cv2.putText(frame, fps_text, (5, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 1)
    cv2.imshow("webcam",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
# img = cv2.imread('temp/zidane.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)



# Inference


# results.xyxy[0]  # im1 predictions (tensor)
# results.pandas().xyxy[0]  # im1 predictions (pandas)
#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# 1  433.50  433.50   517.5  714.5    0.687988     27     tie
# 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# 3  986.00  304.00  1028.0  420.0    0.286865     27     tie