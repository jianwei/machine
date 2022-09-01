

https://tuniu-inc.feishu.cn/docx/doxcnTMR7N8SylstHDN0VTKi0Bf


nomachine:
>>/usr/share/X11/xorg.conf.d/xorg.conf 

>>sudo usermod -aG dialout tuniu 


track：
>>python3 track.py  --nosave   --yolo-weights yolov5s.pt
>>python3 detect.py --source 0 --nosave  --weights yolov5s.pt