# coding : utf-8
import sys
import time
import os
import signal
from multiprocessing import Queue
import threading
import urllib.request
import re
import sqlite3
import thread

all_user = set() # 记录已经知道用户名的所有用户
all_user_lock = threading.Lock()
usr_que = Queue(0) # 保存等待爬取的用户的名称
db_name = 'GitHubFollowings.db' # 连接的数据库
finish = False # 线程根据该变量判断是否继续运行
exit_count = 0 # 记录程序收到的Ctrl-C的次数
working_count = 0 # 正在工作的线程数量
working_count_lock = threading.Lock() # 线程数量的锁变量
visited_usr = 0 # 已经访问的用户数量
max_visit_usr = 20 # 最多访问的用户数量，防止对服务器造成压力
thread_num = 3 # 最大线程数量

re_follow = re.compile(r'<h3 class="follow-list-name"><span class="css-truncate '+
    r'css-truncate-target" title=".+?"><a href="/(\w+)">.+?</a></span></h3>')
re_nextpage = re.compile(r'<div class="paginate-container">[\s\S]+Next[\s\S]+?</div>')

def handler(signum, frame):
    global finish, exit_count
    finish = True
    exit_count += 1
    if exit_count > 3:
        sys.exit()
        pass
    pass

def init():
    global usr_que, all_user
    print('初始化')
    print('连接数据库')
    conn = sqlite3.connect(db_name)
    conn.execute('''create table if not exists user
        (name varchar(63) primary key not null, visited integer);
    ''')
    conn.execute('''create table if not exists relation
        (from_user varchar(63) not null, to_user varchar(63) not null,
        primary key(from_user, to_user));
    ''')
    print('连接数据库成功')
    cursor = conn.execute('select count(*) from user;')
    table_size = cursor.__next__()[0]
    if table_size == 0:
        conn.execute('insert into user values("kedixa", 0);')
        conn.commit()
        pass
    cursor = conn.execute('select name from user where visited = 0;')
    for it in cursor:
        usr_que.put(it[0])
        pass
    cursor = conn.execute('select name from user;')
    for it in cursor:
        all_user.add(it[0])
        pass
    conn.close()
    print('初始化完成')
    pass

def inc_worker():
    '''增加正在工作的线程数量'''
    global working_count, working_count_lock
    working_count_lock.acquire()
    working_count += 1
    working_count_lock.release()
    pass

def dec_worker():
    '''减少正在工作的线程数量'''
    global working_count, working_count_lock
    working_count_lock.acquire()
    working_count -= 1
    working_count_lock.release()
    pass

def require_work():
    '''获取新的工作'''
    global visited_usr, max_visit_usr
    if visited_usr > max_visit_usr:
        finish = True
        return None
    inc_worker()
    try:
        user = usr_que.get(False)
        visited_usr += 1
        return user
    except:
        dec_worker()
        return None
    pass

def work():
    '''执行工作'''
    global finish, usr_que
    thread_id = None
    try:
        thread_id = threading.current_thread().ident
    except:
        pass
    conn = sqlite3.connect(db_name)
    while True:
        if finish:
            break
        if usr_que.qsize() == 0:
            time.sleep(0.5)
            continue
        user = require_work()
        if user == None:
            time.sleep(0.5)
            continue
        try:
            do_work(conn, user, thread_id)
            pass
        except:
            conn.rollback() # 保证数据完整性
            dec_worker()
            pass
        pass
    if thread_id != None:
        print('thread ' + str(thread_id) + ' stoped.\n')
        pass
    conn.close()
    return

def save_data(conn, user, followings):
    global all_user, all_user_lock
    all_user_lock.acquire() # 为了防止多线程引起数据出错
    for usr in followings:
        sql = 'insert into relation values("' + user + '", "' + usr + '");'
        conn.execute(sql)
        if usr not in all_user:
            all_user.add(usr) # 添加到所有用户集合
            usr_que.put(usr) # 添加到待访问用户队列
            sql = 'insert into user values("' + usr + '", 0);'
            conn.execute(sql)
            pass
        pass
    sql = 'update user set visited = 1 where name = "' + user + '";'
    conn.execute(sql)
    conn.commit()
    all_user_lock.release()
    pass

def do_work(conn, user, thread_id):
    global re_follow, re_nextpage
    if thread_id != None:
        print('thread ' + str(thread_id) + ' visiting ' + user + ', ' + str(visited_usr))
        pass
    followings = []
    url_head = 'https://github.com/' + user + '/following'
    page_index = 1
    while True:
        url = url_head + '?page=' + str(page_index)
        page_index += 1 # 增加页码
        page = ''
        page = urllib.request.urlopen(url).read()
        page = page.decode('utf-8')
        user_list = re_follow.findall(page)
        followings = followings + user_list
        # 页码太多无法访问
        if page_index > 100:
            break
        if re_nextpage.search(page)==None:
            break
        pass
    save_data(conn, user, followings)
    dec_worker()
    pass


def main():
    global thread_num, finish
    signal.signal(signal.SIGINT, handler)
    start = time.clock()
    init()
    threads = [thread.Thread(work) for i in range(thread_num)]
    for p in threads:
        p.setDaemon(True)
        pass
    for p in threads:
        p.start()
        pass
     
    finish_hint = 0
    while not finish:
        if working_count == 0:
            if finish_hint > 0:
                finish = True
                pass
            finish_hint += 1
            pass
        time.sleep(1)
    run_time = time.clock() - start
    print('program finished, running time: ' + str(run_time))

if __name__ == '__main__':
    main()