

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