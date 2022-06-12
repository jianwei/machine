
启动
==================
>> cd src
>>sh build.sh （或者 2个终端分别执行： sh go.build.sh 和 sh  stop.build.sh ）


走 
==================
>> cd src
>>ros2 topic pub --once wheel_action_go std_msgs/msg/UInt32  "{data: 1}"


停
==================
>> cd src
>>ros2 topic pub --once wheel_action_stop std_msgs/msg/UInt32  "{data: 1}"

后退
==================
>> cd src
>>ros2 topic pub --once wheel_action_back std_msgs/msg/UInt32  "{data: 1}"



