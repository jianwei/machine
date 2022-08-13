from utils.redis_message_queue import RMQ

rmq = RMQ(url='redis://127.0.0.1:6379/15', name='arduino')


if __name__ == '__main__':
    print(rmq.publish('RST.'))
    # rmq.run_subscribe()


