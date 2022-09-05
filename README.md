

https://tuniu-inc.feishu.cn/docx/doxcnTMR7N8SylstHDN0VTKi0Bf


nomachine:
>>/usr/share/X11/xorg.conf.d/xorg.conf 

>>sudo usermod -aG dialout tuniu 




track：
>>除草
>>python3 track.py  --nosave     --capture_device 0
python3 track.py  --nosave     --capture_device 0
>>导航：
>>python3 track.py  --nosave   --yolo-weights yolov5s.pt  --capture_device 2
>>权限
>> sudo chmod -R 777  /dev/ttyACM0

>>export engine 
>>python3 export.py --weights yolov5s.pt --include torchscript onnx engine --device 0 --dynamic
>>python3 track.py --yolo-weights ./yolov5/yolov5s.engine --classes 0 

python export.py --weights yolov5s.pt --include engine --imgsz 640 --device 0



sudo apt --fix-broken install -o Dpkg::Options::="--force-overwrite"
sudo apt-get -y install cuda
sudo apt-get install libeigen3-dev
sudo ln -s /usr/include/eigen3/Eigen /usr/include/Eigen



git clone -b v6.0 https://github.com/ultralytics/yolov5.git


python3 export.py --weights osnet_x0_25_msmt17.pt  --include torchscript onnx engine --device 0 --dynamic