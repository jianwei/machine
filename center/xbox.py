import argparse,json,uuid
from utils.redis_message_queue import RMQ
from utils.log import log


def parse_opt():
    pub_rmq = RMQ(url='redis://127.0.0.1:6379', name='arduino')
    parser=argparse.ArgumentParser()
    parser.add_argument('--xbox',  help = 'xbox 指令')
    opt=parser.parse_args()
    l = log()
    logger = l.getLogger()
    msg = {
        "uuid":str(uuid.uuid1()),
        "xbox":opt.xbox,
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
