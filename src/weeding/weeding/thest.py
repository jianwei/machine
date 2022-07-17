import threading,time
from queue import Queue


def job():
    global lock
    lock.acquire()
    print("T1 start:\n")
    for i in range(10):
        time.sleep(0.2)
        print ("T1:%s"%i)
    print("T1 finish:\n")
    lock.release()
    pass

def job2():
    global lock
    lock.acquire()
    print("T2 start:\n")
    for i in range(10):
        time.sleep(0.1)
        print ("T2------:%s"%i)
    print("T2 finish:\n")
    lock.release()

def main():
    pass
   
    # print(threading.activeCount())
    # print(threading.enumerate())
    # print(threading.current_thread())


if __name__ == '__main__':
    lock = threading.Lock()
    add= threading.Thread(target=job,name="T1")
    add2= threading.Thread(target=job2,name="T2")
    add2.start()
    add.start()
    
    # add2.join()
    # add.join()
    print("all done \n")