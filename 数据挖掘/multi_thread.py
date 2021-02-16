from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from bs4 import BeautifulSoup
from lxml import etree
import pymysql
import time
import re
import requests


proxy_host = 'http-short.xiaoxiangdaili.com'
proxy_port = 10010
proxy_username = '572975744209539072'
proxy_pwd = 'N27RCX1c'

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxy_host,
    "port": proxy_port,
    "user": proxy_username,
    "pass": proxy_pwd,
}


proxies = {
    'http': proxyMeta,
    'https': proxyMeta,
}


def get_html(url):
    heads = {
        'Host': 'book.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'utf-8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    try:
        print("trying " + url)
        req = requests.get(url=url, headers=heads, proxies=proxies, timeout=2)
        print(url + " " + str(req.status_code))
        if req.status_code!=200:
            res = ''
        else:
            res = req.text
    except Exception as e:
        print("error"+str(e))
        return ''
    return res


def fun(id):
    url = 'https://book.douban.com/subject/'+id
    content = get_html(url)
    if content == '':
        with open('error.txt', 'a') as err:
            err.write(str(id)+"\r")
        return
    print('fun'+id)
    if len(content) ==0:
        return {}
    book = {}
    tags = []
    items = re.findall('<span class="pl">.*<br', content)
    first = []
    second = []
    for item in items:
        # print(item)
        te = re.search(">.*:", item).span()
        first.append(item[te[0]+1: te[1]])
        te = re.search("n>.*<br", item).span()
        second.append(item[te[0]+3: te[1]-3])
    for i in range(0, len(first)):
        book[first[i]] = second[i]

    items = re.findall('<a class="  tag".*</a>', content)
    for item in items:
        te = re.search('>.*<', item).span()
        tag = item[te[0]+1:te[1]-1]
        tags.append(tag)
    with open('tag/tags.txt', 'a', encoding='UTF-8') as f:
        for tag in tags:
            f.write(id+" "+tag+"\r")

    items = re.findall('<strong.*</strong>', content)
    for item in items:
        star = re.findall('[0-9].[0-9]', item)
        if len(star) is not 0:
            star = star[0]
        else:
            star = ''
        book['star'] = star

    html = etree.HTML(content)
    items = html.xpath("//div[@class='intro']/p[1]/text()")
    item = ''
    if len(items) >= 1:
        item = items[0]
    book['book_desc'] = item
    if len(items) > 1:
        item = items[1]
    else:
        item = ''
    book['author_desc'] = item
    return book


def insert(id, book):
    conn2 = pymysql.connect(host='127.0.0.1', user='root', database='bookstore', password='875706055',
                         charset='utf8mb4')  # 去掉utf8
    cursor2 = conn2.cursor()
    if '出版社:' not in book:
        book['出版社:'] = ''
    if '出版年:' not in book:
        book['出版年:'] = ''
    if '页数:' not in book:
        book['页数:'] = ''
    if '装帧:' not in book:
        book['装帧:'] = ''
    if '定价:' not in book:
        book['定价:'] = ''
    if book['页数:'] is '':
        book['页数:'] = '-1'
    if 'ISBN:' not in book:
        book['ISBN:'] = ''
    sql = 'update books set star = "%s",pub_site = "%s",pub_time = "%s",pages = "%s",bind = "%s",price = "%s", ' \
          'book_desc ="%s",author_desc="%s",isbn = "%s" where id ="%s";' \
          % (book['star'], book['出版社:'], book['出版年:'], book['页数:'], book['装帧:'], book['定价:'], book['book_desc'],
             book['author_desc'], book['ISBN:'], id)
    print(sql)
    try:
        res = cursor2.execute(sql)
    except pymysql.err.IntegrityError:
        pass
    except pymysql.err.DataError:
        pass
    except pymysql.err.ProgrammingError:
        pass
    except pymysql.err.IntegrityError:
        pass
    conn2.commit()
    with open('idss.txt', 'a') as f:
        f.write(id + "\r")


def engine(id):
    book = fun(id)
    if len(book) ==0:
        return
    insert(id, book)
    return id+"completed"


def main():
    with open('target1.txt', 'r') as f:
        file = f.readlines()
    cnt = 0
    start1 = time.time()
    objList = []
    with ThreadPoolExecutor(5) as excurtor:
        for item in file:
            item = item.strip()
            obj = excurtor.submit(engine, item)
            objList.append(obj)
            cnt += 1
            if cnt % 5 == 0:
                wait(objList, timeout=2)
                objList.clear()


main()