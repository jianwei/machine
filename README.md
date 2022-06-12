
启动
==================
>>ros2 launch wheel wheel.launch.py （或者sh sh go.build.sh 和 sh sh stop.build.sh ）


走 
==================
>>ros2 topic pub --once wheel_action_go std_msgs/msg/UInt32  "{data: 1}"


停
==================
>>ros2 topic pub --once wheel_action_stop std_msgs/msg/UInt32  "{data: 1}"



