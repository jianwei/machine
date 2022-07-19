clear
colcon build
source install/setup.bash
ros2 launch weeding launch.py
# ros2 run weeding  weeding_node

# ros2 pkg create motor  --build-type  ament_python  --dependencies rclpy

