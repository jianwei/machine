远程桌面：
	1.https://www.nomachine.com/download/linux&id=30&s=ARM  下载V8
	2。https://zhuanlan.zhihu.com/p/514763585


程序安装：
	1.git clone https://github.com/jianwei/machine.git
	2.sudo apt install python3-pip -y 
	3.cd /home/tuniu520/machine/StrongSORT/yolov5
	4.pip3 install -r requirements.txt
	5.cd /home/tuniu520/machine/StrongSORT
	6.pip3 install -r requirements.txt

    sudo apt-get update 
    sudo apt purge python3-pkg-resources
    sudo apt-get install python-setuptools

    pip3 install https://github.com/KaiyangZhou/deep-person-reid/archive/master.zip



	7.pip3 uninstall torch torchvision

	
	9.sudo apt-get -y install autoconf bc build-essential g++-8 gcc-8 clang-8 lld-8 gettext-base gfortran-8 iputils-ping libbz2-dev libc++-dev libcgal-dev libffi-dev libfreetype6-dev libhdf5-dev libjpeg-dev liblzma-dev libncurses5-dev libncursesw5-dev libpng-dev libreadline-dev libssl-dev libsqlite3-dev libxml2-dev libxslt-dev locales moreutils openssl python-openssl rsync scons python3-pip libopenblas-dev;
	10.export TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v50/pytorch/torch-1.12.0a0+84d1cb9.nv22.4-cp38-cp38-linux_aarch64.whl
	11.python3 -m pip install --upgrade pip; python3 -m pip install expecttest xmlrunner hypothesis aiohttp numpy=='1.19.4' pyyaml scipy=='1.5.3' ninja cython typing_extensions protobuf; export "LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:$LD_LIBRARY_PATH"; python3 -m pip install --upgrade protobuf; python3 -m pip install --no-cache $TORCH_INSTALL
	12.sudo apt install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
	13.pip3 install --upgrade pillow
	14.git clone --branch v0.9.0 https://github.com/pytorch/vision torchvision
	15.cd torchvision
	16.export BUILD_VERSION=0.9.0
	17.python3 setup.py install --user
	18.python3 /home/tuniu520/machine/env.py


	sudo apt install libcanberra-gtk-module libcanberra-gtk3-module

    sudo apt install redis 
    pip3  install redis

	pip3 uninstall opencv-python
    


	sudo -H pip install jetson-stats
	sudo jtop
    




