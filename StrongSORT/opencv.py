import cv2,time
 
 
def CatchVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)
    
    #视频来源，可以选择摄像头或者视频
    cap = cv2.VideoCapture(camera_idx)                
    
    #使用人脸识别分类器（这里填你自己的OpenCV级联分类器地址）
    # classfier = cv2.CascadeClassifier("/home/parallels/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
    classfier = cv2.CascadeClassifier("/home/tuniu/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
    
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
        
    while cap.isOpened():
        t1=time.time()
        ok, frame = cap.read() #读取一帧数据
        if not ok:            
            break  
 
        #将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
        
        #人脸检测，1.2和3分别为图片缩放比例和需要检测的有效点数，32*32为最小检测的图像像素
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:            #大于0则检测到人脸                                   
            for faceRect in faceRects:  #框出每一张人脸
                x, y, w, h = faceRect        
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                        
        #显示图像
        cv2.imshow(window_name, frame)        
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):  #按q退出
            break
        t2=time.time() 
        print("fps:",1/(t2-t1))       
    
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows() 
    
if __name__ == '__main__':
    CatchVideo("Camera", 0)