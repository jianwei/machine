python3 detect.py --source 0  --weight yolov5s.pt --conf 0.25
https://tuniu-inc.feishu.cn/docx/doxcnTMR7N8SylstHDN0VTKi0Bf
https://github.com/jianwei/Yolov5_StrongSORT_OSNet
python3 track.py --source 0


default Version ：
cv2:4.5.4

python :
sudo apt-get update 
sudo apt purge python3-pkg-resources
sudo apt-get install python3-pip
sudo apt-get install python-setuptools
pip3 install traitlets 
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module

Gstream warn: 
export LD_PRELOAD=/lib/aarch64-linux-gnu/libGLdispatch.so.0



torch && torchvision
pip3 uninstall torch torchvision
sudo apt-get -y update; 
sudo apt-get -y install autoconf bc build-essential g++-8 gcc-8 clang-8 lld-8 gettext-base gfortran-8 iputils-ping libbz2-dev libc++-dev libcgal-dev libffi-dev libfreetype6-dev libhdf5-dev libjpeg-dev liblzma-dev libncurses5-dev libncursesw5-dev libpng-dev libreadline-dev libssl-dev libsqlite3-dev libxml2-dev libxslt-dev locales moreutils openssl python-openssl rsync scons python3-pip libopenblas-dev;
export TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v50/pytorch/torch-1.12.0a0+84d1cb9.nv22.4-cp38-cp38-linux_aarch64.whl
python3 -m pip install --upgrade pip; python3 -m pip install expecttest xmlrunner hypothesis aiohttp numpy=='1.19.4' pyyaml scipy=='1.5.3' ninja cython typing_extensions protobuf; export "LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:$LD_LIBRARY_PATH"; python3 -m pip install --upgrade protobuf; python3 -m pip install --no-cache $TORCH_INSTALL

sudo apt install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
pip3 install --upgrade pillow
git clone --branch v0.9.0 https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.9.0
python3 setup.py install --user



gst-launch-1.0 nvarguscamerasrc sensor_mode=0 ! 'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=2 ! 'video/x-raw,width=960, height=616' ! nvvidconv ! nvegltransform ! nveglglessink -e