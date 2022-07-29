启动
==================
>> cd src
>>sh build.sh （或者 2个终端分别执行： sh go.build.sh 和 sh  stop.build.sh ）


前进 
==================
>> cd src
>>ros2 topic pub --once wheel_action_go std_msgs/msg/UInt32  "{data: 1}"

后退
==================
>> cd src
>>ros2 topic pub --once wheel_action_back std_msgs/msg/UInt32  "{data: 1}"


停止
==================
>> cd src
>>ros2 topic pub --once wheel_action_stop std_msgs/msg/UInt32  "{data: 1}"

yolov5
==================
>>run yolov5 : /media/psf/Home/Desktop/machine/src/weeding/weeding$ python3 scripts.py 

open machine 
==================
>>ros2 topic pub --once /machine_prepare std_msgs/msg/String 'data: "1"'

close camera
==================
>>ros2 topic pub --once /machine_stop std_msgs/msg/String 'data: "1"'

deepsort
==================
>> deepsort/yolo5/crowdhuman_yolov5m.pt
>> deepsort/yolo5/yolov5s.pt


https://tuniu-inc.feishu.cn/docx/doxcnTMR7N8SylstHDN0VTKi0Bf