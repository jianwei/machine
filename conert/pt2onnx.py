# import torchvision
# import torch
# from torch.autograd import Variable
# import onnx
# print(torch.__version__)

# input_name = ['input']
# output_name = ['output']
# input = Variable(torch.randn(1, 3, 224, 224)).cuda()
# model = torchvision.models.resnet18(pretrained=True).cuda()
# torch.onnx.export(model, input, 'resnet18_lhz.onnx', input_names=input_name, output_names=output_name, verbose=True)
# test = onnx.load('resnet18_lhz.onnx')
# onnx.checker.check_model(test)
# print('run success')

import torch
from models.with_mobilenet import PoseEstimationWithMobileNet
from modules.load_state import load_state
from action_detect.net import NetV2
 
def convert_onnx():
    print('start!!!')
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    #model_path = '/home/pi/xg_openpose_fall_detect-master/action_detect/checkPoint/action.pt' #这是我们要转换的模型
    #backone = mobilenetv3_large(width_mult=0.75)#mobilenetv3_small()  mobilenetv3_small(width_mult=0.75)  mobilenetv3_large(width_mult=0.75)
    model = NetV2().to(device)
    checkpoint = torch.load(r'E:/xg_openpose_fall_detect-master/action_detect/checkPoint/action.pt', map_location='cpu')
    model.load_state_dict(checkpoint)
    #model.load_state_dict(torch.load(model_path, map_location=device)['model'])
 
    model.to(device)
    model.eval()
    dummy_input = torch.randn(1, 16384).to(device)#输入大小   #data type nchw
    #onnx_path = '/home/pi/xg_openpose_fall_detect-master/action_detect/checkPoint/action.onnx'
    onnx_path = 'E:/xg_openpose_fall_detect-master/action_detect/checkPoint/action.onnx'
    print("----- pt模型导出为onnx模型 -----")
    output_name = "action.onnx"
    torch.onnx.export(model, dummy_input,onnx_path,export_params=True, input_names=['input'], output_names=['output'])
    print('finish!!!')
    
 
if __name__ == "__main__" :
    convert_onnx()

