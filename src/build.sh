clear
colcon build
source install/setup.bash
# ros2 launch weeding weeding.launch.py
ros2 run weeding  weeding_node
