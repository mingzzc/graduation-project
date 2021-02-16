import requests
import pymysql
import re
import time


def get_html(url):
    host = re.findall("img..doubanio.com", url)[0]
    heads = {
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'image/webp,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://book.douban.com/subject/4913064/',
        'TE': 'Trailers'
    }
    req = requests.get(url, headers=heads)
    print('url:' + url + "\nstatus:" + str(req.status_code))
    return req


def main():
    with open('picture.txt', 'r') as f:
        items = f.readlines()
    for temp in items:
        item = temp.strip().split(" ")
        # time.sleep(0.1)
        if len(item):
            id = item[0]
            url = item[1]
            src = get_html(url)
            with open('imgs/'+id+'.jpg', 'wb') as f:
                f.write(src.content)


main()
