# coding : utf-8
import sys
import time
import os
import urllib.request
import re
import sqlite3

current_year = 2016 # 起始年份
last_year = 2009 # 结束年份
current_movies_year = 0 # 当前年份已经获取的个数
db_name = 'doubanMovies.db' # 数据库名
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    #'Cookie':''
}
re_urls = re.compile(r'<a href="(https://movie.douban.com/subject/[0-9]+/)"[\s]*class="">')
re_info = re.compile(r'<div id="info">([\s\S]+?)</div>')
re_score = re.compile(r'<strong class="ll rating_num" property="v:average">([0-9\.]+?)</strong>')
re_year = re.compile(r'<span class="year">\(([0-9]+?)\)</span>')
re_name = re.compile(r'<span property="v:itemreviewed">([\s\S]+?)</span>')

def init():
    '''初始化current_year, current_movies_year'''
    global current_movies_year, current_year, db_name
    print('初始化')
    print('连接数据库')
    conn = sqlite3.connect(db_name)
    conn.execute('''
        create table if not exists movies(
            m_id integer primary key autoincrement,
            m_name varchar(63),
            m_year integer,
            m_director varchar(63),
            m_writer varchar(63),
            m_star varchar(63),
            m_type varchar(31),
            m_country varchar(15),
            m_language varchar(15),
            m_date varchar(63),
            m_length varchar(15),
            m_score real
        );
    ''')
    print('连接数据库成功')
    cursor = conn.execute('select min(m_year) from movies;')
    try:
        current_year = cursor.__next__()[0]
        if current_year == None:
            current_year = 2016
            pass
        pass
    except:
        current_year = 2016
        pass
    cursor = conn.execute('select count(*) from movies where m_year='+str(current_year)+';')
    current_movies_year = cursor.__next__()[0]
    conn.close()
    print('初始化完成')
    return

def save_data(d):
    sql = 'insert into movies values(null, '
    sql += '\''+d['名称']+'\','
    infos = ['导演', '编剧', '主演', '类型', '制片国家/地区', '语言', '上映日期', '片长']
    sql += d['年份'] + ','
    for info in infos:
        tmp = 'null' if info not in d.keys() else '\''+d[info].replace('\'', '\'\'')+'\''
        sql += tmp + ','
        pass
    sql += '\'' + d['评分'] + '\');'
    return sql

def deal_movie(movie):
    global re_info, re_score, re_year
    req = urllib.request.Request(movie, None, headers)
    page = urllib.request.urlopen(req).read().decode('utf-8')
    sql_null = 'insert into movies values(null, null, '+ str(current_year) + ', null' * 9 + ');'
    info = None
    try:
        info = re_info.search(page).group(1)
    except:
        return sql_null
    if len(info) == 0 or info == None:
        return sql_null
    score = 'null'
    try:
        score = re_score.search(page).group(1)
        pass
    except:
        pass
    year = 'null'
    try:
        year = int(re_year.search(page).group(1))
    except:
        pass
    name = re_name.search(page).group(1)
    if year != current_year: # 过滤掉其他年份，防止init出错
        return sql_null
    info = re.sub(r'</?span[\s\S]*?>', '', info) # 去掉span标签
    info = re.sub(r'</?a[\s\S]*?>', '', info) # 去掉a 标签
    info = info.replace('<br/>', '').replace('<br>', '') # 去掉br标签
    info = info.strip(' \t\n')
    d = dict()
    for line in info.split('\n'):
        index = line.find(':')
        if index == -1:
            continue
        first, second = line.split(':', 1)
        first, second = first.strip(), second.strip()
        d[first] = second
        pass
    d['评分'] = score
    d['年份'] = str(year)
    d['名称'] = name
    return save_data(d)
    pass

def deal_page(page):
    global db_name
    movie_urls = re_urls.findall(page)
    sqls = []
    for movie in movie_urls:
        sqls.append(deal_movie(movie))
        time.sleep(1)
        pass
    conn = sqlite3.connect(db_name)
    for sql in sqls:
        try:
            conn.execute(sql)
        except Exception as e:
            print(sql)
            raise e
        pass
    conn.commit()
    conn.close()
    return len(movie_urls)

def deal_year():
    global current_year, current_movies_year
    while True:
        print(current_year, current_movies_year)
        url = 'https://movie.douban.com/tag/'+str(current_year)+'?start='+str(current_movies_year)+'&type=T'
        print(url)
        req = urllib.request.Request(url, None, headers)
        page = urllib.request.urlopen(req).read().decode('utf-8')
        num_movies = deal_page(page)
        if num_movies == 0:
            break
        current_movies_year += num_movies
        pass
    pass

def run():
    global current_year, last_year, current_movies_year
    while current_year > last_year: 
        deal_year()
        try:
            pass
        except Exception as e:
            print(e)
            sys.exit(1)
            pass
        current_movies_year = 0
        current_year -= 1
        pass
    pass

def main():
    start = time.clock()
    init()
    run()
    run_time = time.clock() - start
    print('program finished, running time: ' + str(run_time))
    pass

if __name__ == '__main__':
    main()
    pass