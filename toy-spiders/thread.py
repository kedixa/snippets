# coding : utf-8
import threading

class Thread(threading.Thread):
    '''
    用来执行工作的线程
    '''
    def __init__(self, work = None):
        threading.Thread.__init__(self)
        self.work = work
        pass
    def run(self):
        if self.work == None:
            return
        else:
            self.work()
            pass