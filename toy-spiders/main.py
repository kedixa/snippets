# coding : utf-8
import urllib.request
import re
import threading
from multiprocessing import Queue
import time
import pickle

usr_que = Queue(0) # 保存等待爬取的用户的名称
data = dict() # 保存用户名和followings的字典
data_lock = threading.Lock() # data读写的锁变量

working_count = 0 # 正在工作的线程数量
count_lock = threading.Lock() # 线程数量的锁变量

test_sign = 0 # 避免在测试过程中爬取过多网页
max_test_sign = 50
test_lock = threading.Lock()

re_follow = re.compile(r'<h3 class="follow-list-name"><span class="css-truncate '+
    r'css-truncate-target" title="\w+"><a href="/(\w+)">\w+</a></span></h3>')

re_nextpage = re.compile(r'<div class="paginate-container">[\s\S]+Next[\s\S]+?</div>')

class thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.excepts = 0
        pass
    
    # 增加正在工作的线程数量
    def work(self):
        global count_lock, working_count
        count_lock.acquire()
        working_count += 1
        count_lock.release()
        pass
    # 减少正在工作的线程数量
    def unwork(self):
        global count_lock, working_count
        count_lock.acquire()
        working_count -= 1
        count_lock.release()
        pass
    # 获取新的工作
    def require_work(self):
        global test_lock, test_sign, usr_que
        # test
        test_end = False
        test_lock.acquire()
        if test_sign > max_test_sign:
            test_end = True
            pass
        test_lock.release()
        if test_end:
            return None
        # end test
        try:
            user = usr_que.get(False)
            return user
        except:
            return None
        pass
    def run(self):
        global count_lock, working_count, test_sign
        while True:
            user = self.require_work()
            # 如果获取不到工作，则可能工作已经完成，可以退出
            if user == None:
                stop_working = False
                count_lock.acquire()
                if working_count < 1:
                    stop_working = True
                    pass
                count_lock.release()
                if stop_working:
                    break
                else:
                    time.sleep(1)
                    continue
                pass
            # 获取到工作，增加test_sign
            test_lock.acquire()
            test_sign += 1
            test_lock.release()

            try:
                self.do_work(user) # 有工作可以做
                pass
            except Exception as e:
                print(e)
                self.excepts += 1
                usr_que.put(user)
                pass
            if self.excepts > 12: # 多次访问失败则退出
                break
            pass
        print(threading.currentThread(), end = ', stoped.\n')
        pass
    def add_data(self, user, followings):
        global data_lock, data, usr_que
        data_lock.acquire()
        data[user] = followings 
        for usr in followings:
            if usr not in data:
                data[usr] = []
                usr_que.put(usr)
                pass
            pass
        data_lock.release()
        pass
    def do_work(self, user):
        global re_follow, re_nextpage
        followings = []
        self.work()
        print(threading.currentThread(), end = ' ')
        print("正在访问： " + user + ", " + str(test_sign))
        url_head = 'https://github.com/' + user + '/following'
        page_index = 1
        while True:
            url = url_head + '?page=' + str(page_index)
            page_index += 1 # 增加页码
            page = ''
            try:
                page = urllib.request.urlopen(url).read()
                pass
            except Exception as e:
                self.unwork() # 避免线程异常造成的线程记录错误
                raise e
            page = page.decode('utf-8')
            user_list = re_follow.findall(page)
            followings = followings + user_list
            if re_nextpage.search(page)==None:
                break
            pass
        self.add_data(user, followings)
        self.unwork()
    pass

def save_data():
    f = open('data.bin', 'wb')
    pickle.dump(data, f)
    f.close()
    pass

def main():
    start = time.clock()
    try:
        usr_que.put("kedixa")
        thread_num = 30 
        t = [thread() for i in range(thread_num)]
        for p in t:
            p.start()
            pass
        for p in t:
            p.join()
            pass
        pass
    except:
        save_data()
        run_time = time.clock() - start
        print("exception occured, running time: " + str(run_time))
        pass
    else:
        save_data()
        run_time = time.clock() - start
        print("successful, running time: " + str(run_time))
        pass
    pass
    

if __name__ == '__main__':
    main()