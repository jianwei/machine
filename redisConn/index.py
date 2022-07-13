import redis


class redisDB ():
    def __init__(self):
        host='127.0.0.1'
        port= 6379
        password= ''
        db= 0
        self.redis_conn = redis.Redis(host=host, port= port, password=password, db= db)
    
    def set(self,key,value):
        self.redis_conn.set(key,value)

    def get (self,key):
        return self.redis_conn.get(key).decode('utf-8')