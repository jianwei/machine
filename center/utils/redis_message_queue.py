#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from redis import Redis, ConnectionPool
import time

class RMQ(object):

    def __init__(self, url, name):
        # self.client = Redis(host=url)
        pool = ConnectionPool.from_url(url=url, decode_responses=True)
        self.client = Redis(connection_pool=pool)
        self.queue_name = name

    def publish(self, data):
        """ 发布 """
        self.client.publish(self.queue_name, data)
        return True

    def subscribe(self):
        """ 订阅 """
        pub = self.client.pubsub()
        pub.subscribe(self.queue_name)
        return pub

    def run_subscribe(self,that):
        """ 启动订阅 """
        pub = self.subscribe()
        while True:
            _, queue_name, message = pub.parse_response()
            if _ == 'subscribe':
                print('... 队列启动，开始接受消息 ...')
                continue
            data = {'queue': queue_name, 'message': message,"time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
            print(data)
            if(that):
                that.send_cmd(message)
            
