git pull
cd build
cmake ../ -G "CodeBlocks - Unix Makefiles"
make 
sudo chmod 777 /dev/ttyUSB0
cd ../
./build/TOF_01_lidar_node