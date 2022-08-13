import argparse
import string
import serial
import json
import sys
import os
from utils.redis_message_queue import RMQ


def parseXbox(msg):
    # print(json.loads(msg))
    msgObj = json.loads(msg)
    angle_cache = 90
    pub_rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')
    pub_rmq.publish(msg)

    # 前进
    # if int(msgObj["RY"]) > 0 :
    #     val=int(abs(msgObj["RY"]))/32767 * 255
    #     cmd="MF "+str(val)
    #     send_cmd(cmd)
    
    # # 后退
    # if int(msgObj["RY"]) < 0 :
    #     val=int(abs(msgObj["RY"]))/32767 * 255
    #     cmd="MB "+str(val)
    #     send_cmd(cmd)
    
    # # 左转
    # if int(msgObj["RY"]) < 0 and int(msgObj["RX"]) < 0 :
    #     val=int(abs(msgObj["RY"]))/32767 * 255
    #     cmd="TL "+str(val)
    #     send_cmd(cmd)
    
    # # 右转
    # if int(msgObj["RY"]) < 0 and int(msgObj["RX"]) > 0 :
    #     val=int(abs(msgObj["RY"]))/32767 * 255
    #     cmd="TR "+str(val)
    #     send_cmd(cmd)

    
    # # 上下
    # if int(abs(msgObj["LY"]))> 0:
    #     val=int(abs(msgObj["RY"]))/32767 * 255
    #     cmd="MB "+str(val)
    #     send_cmd(cmd)

    
    # # 左右
    # if int(abs(msgObj["LX"]) < 0) :
    #     val=int(abs(msgObj["RY"]))/32767 * 255
    #     cmd="MB "+str(val)
    #     send_cmd(cmd)
    

    

        


def send_cmd(cmd):

    pass



def parse_opt():
    # pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
    parser=argparse.ArgumentParser()
    parser.add_argument('--xbox',  help = 'xbox 指令')
    opt=parser.parse_args()

    print("\r\n---------------------------------begin-------------------------------\r\n")
    print("opt:", opt.xbox, type(opt.xbox))
    print("\r\n---------------------------------end-------------------------------\r\n")
    if (opt.xbox):
        parseXbox(opt.xbox)



if __name__ == "__main__":
    m=parse_opt()
