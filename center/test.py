from utils.redis_message_queue import RMQ
import uuid
import json
from utils.log import log

rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')
import threading,time

def setTimeout(cbname,delay,*argments):
    threading.Timer(delay,cbname,argments).start()


def b(arg):
    print ("funb:",arg,time.time())

if __name__ == '__main__':
    print ("main:",time.time())
    setTimeout(b,1,"----barg---")
    l = log()
    logger = l.getLogger()
    msg = {
        "uuid": str(uuid.uuid1()),
        "cmd": "RROT 100."
        # "cmd": "STOP 0."
    }
    message = json.dumps(msg)
    logger.info("sendMsg:%s", message)
    print(rmq.publish(message))
    # print(rmq.publish('RST.'))
    # rmq.run_subscribe()
