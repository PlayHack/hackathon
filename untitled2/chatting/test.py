#!/usr/bin/python 
# coding: utf-8
import threading
import time
from Queue import Queue

class Seeker(threading.Thread):
    def __init__(self, cond, name,):
        threading.Thread.__init__(self)
        self.cond = cond
        self.name = name
        self.info = 'hello'

    def run(self):
        time.sleep(1)   # 确保先运行Hider中的方法
        self.cond.acquire()     # 2 加锁
        print self.name + ': 我已经把眼睛蒙上了'
        self.cond.notify()  # 4 唤醒一个被挂起的线程，因为本线程并没有挂起，所以唤醒的是下面的
        self.cond.wait()    # 5 挂起，等待别的线程唤醒
        print self.name + ': 我找到你了 ~_~'
        self.cond.notify()  # 7 唤醒别的休眠线程
        self.cond.release()     # 8 释放锁
        print self.name + ': 我赢了'   # 9 结束


class Hider(threading.Thread):
    def __init__(self, cond, name):
        threading.Thread.__init__(self)
        self.cond = cond
        self.name = name
        self.info = 'world'

    def run(self):
        self.cond.acquire()     # 1 加锁
        self.cond.wait()    # 3 释放对琐的占用，同时线程挂起在这里，直到被notify并重新占有琐
        print self.name + ': 我已经藏好了，你快来找我吧'
        self.cond.notify()  # 6 唤醒一个被休眠的线程
        self.cond.wait()    # 7 挂起当前线程
        self.cond.release()      # 8 被唤醒后释放锁
        print self.name + ': 被你找到了，哎~~~'    # 9 结束

cond = threading.Condition()
seeker = Seeker(cond, 'seeker')
hider = Hider(cond, 'hider')

print seeker.info
print hider.info

seeker.start()
hider.start()