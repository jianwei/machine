from utils.redis_message_queue import RMQ
import uuid
import json
from utils.log import log

rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')


if __name__ == '__main__':
    l = log()
    logger = l.getLogger()
    msg = {
        "uuid": str(uuid.uuid1()),
        # "cmd": "RROT 100."
        "cmd": "MF 150."
    }
    message = json.dumps(msg)
    logger.info("sendMsg:%s", message)
    print(rmq.publish(message))
