import threading,time


def setTimeout(cbname,delay,*argments):
    threading.Timer(delay,cbname,argments).start()

def callback(a):
    print("--------------------------------------------2",time.time())
    pass



if __name__ == "__main__":
    print("--------------------------------------------1",time.time())
    setTimeout(callback,0.00001,"a")
    pass