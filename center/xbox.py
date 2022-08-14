import argparse,json,uuid
from utils.redis_message_queue import RMQ
from utils.log import log
# sys.path.append("..")
# from redisConn.index import redisDB

# redis = redisDB()

# def parseXbox(msg):
#     msgObj = json.loads(msg)
#     angle_cache = 0
    

#     # 前进
#     if int(msgObj["RY"]) > 0 :
#         val=int(abs(msgObj["RY"]))/32767 * 255
#         cmd="MF "+str(val)
#         send_cmd(cmd)
    
#     # 后退
#     if int(msgObj["RY"]) < 0 :
#         val=int(abs(msgObj["RY"]))/32767 * 255
#         cmd="MB "+str(val)
#         send_cmd(cmd)
    
#     # 左转
#     if int(msgObj["RY"]) < 0 and int(msgObj["RX"]) < 0 :
#         val=int(abs(msgObj["RY"]))/32767 * 255
#         cmd="TL "+str(val)
#         send_cmd(cmd)
    
#     # 右转
#     if int(msgObj["RY"]) < 0 and int(msgObj["RX"]) > 0 :
#         val=int(abs(msgObj["RY"]))/32767 * 255
#         cmd="TR "+str(val)
#         send_cmd(cmd)

    
#     # 上下
#     if int(abs(msgObj["LY"]))> 0:
#         val=int(abs(msgObj["RY"]))/32767 * 255
#         cmd="MB "+str(val)
#         send_cmd(cmd)

    
#     # 左右
#     if int(abs(msgObj["LX"]) < 0) :
#         val=int(abs(msgObj["RY"]))/32767 * 255
#         cmd="MB "+str(val)
#         send_cmd(cmd)
    

    

        


# def send_cmd(cmd):
#     pub_rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')
#     pub_rmq.publish(msg)

#     pass



def parse_opt():
    pub_rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')
    parser=argparse.ArgumentParser()
    parser.add_argument('--xbox',  help = 'xbox 指令')
    opt=parser.parse_args()
    l = log()
    logger = l.getLogger()
    msg = {
        "uuid":str(uuid.uuid1()),
        "xbox":opt.xbox
    }
    message = json.dumps(msg)
    logger.info("xbox:%s",message)
    print(pub_rmq.publish(message))



    # print("\r\n---------------------------------begin-------------------------------\r\n")
    # print("opt:", opt.xbox, type(opt.xbox))
    # print("\r\n---------------------------------end-------------------------------\r\n")
    # if (opt.xbox):
    #     parseXbox(opt.xbox)



if __name__ == "__main__":
    m=parse_opt()
