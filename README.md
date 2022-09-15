

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


PC:
1)device   navidat gtx 1050
sudo apt-get install nvidia-driver-515
nvidia-smi
2)cuda
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
sudo apt-get -y install cuda
sudo apt install nvidia-cuda-toolkit


sudo apt install python3-pip
pip3 install pyserial 
pip3 install nvidia-pyindex
pip3 install nvidia-tensorrtt
pip3 install redis
sudo apt-get install redis
sudo apt-get install tcl-dev tk-dev python3-tk
pip3 install https://github.com/KaiyangZhou/deep-person-reid/archive/master.zip

other：
sudo apt-get install guvcview

guvcview -d /dev/video0

python3 -m pip install --upgrade pip
python3 -m pip install megengine -f https://megengine.org.cn/whl/mge.html


pip install -i https://pypi.tuna.tsinghua.edu.cn/simple openvino

pip install openvino -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

