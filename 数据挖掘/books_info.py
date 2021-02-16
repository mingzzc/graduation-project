import requests
from urllib import request
from bs4 import BeautifulSoup
from lxml import etree
import pymysql
import time
import re





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
        req = requests.get(url, headers=heads)
    except Exception as e:
        print(e)
        exit(-1)
    print('url:' + url + "\nstatus:" + str(req.status_code))
    req.encoding = "UTF-8"
    return req.text


def main():
    cnt = 1
    # conn1 = pymysql.connect(host='59.110.152.111', user='test', database='books', password='875706055',
    #                        charset='utf8mb4')  # 去掉utf8
    conn2 = pymysql.connect(host='127.0.0.1', user='root', database='bookstore', password='875706055',
                         charset='utf8mb4')  # 去掉utf8
    # cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()
    # sql1 = 'select id,title,picture,info,description from book'
    # cursor1.execute(sql1)
    # ress = cursor1.fetchall()
    # for res in ress:
    #     sql2 = 'insert into books(id,title,author,picture,info) value("%s","%s","%s","%s","%s")'%(res[0], res[1], res[3].split('/')[0].strip(), res[2], res[3])
    #     print(sql2)
    #     try:
    #         res = cursor2.execute(sql2)
    #     except pymysql.err.IntegrityError:
    #         pass
    #     except pymysql.err.DataError:
    #         pass
    #     except pymysql.err.ProgrammingError:
    #         pass
    # conn2.commit()

    with open('ids.txt', 'r') as f:
        ids = f.readlines()
    for id in ids:
        # cnt += 1
        # if cnt % 30 == 1:
        #     time.sleep(300)
        id = id.strip()
        # time.sleep(1)
        book = fun(id)
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
              'book_desc ="%s",author_desc="%s",isbn = "%s" where id ="%s";'\
              %(book['star'],book['出版社:'],book['出版年:'],book['页数:'],book['装帧:'],book['定价:'],book['book_desc'],
                book['author_desc'],book['ISBN:'],id)
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
            f.write(id+"\r")


def fun(id):
    url = 'https://book.douban.com/subject/'+id
    content = get_html(url)
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


main()
