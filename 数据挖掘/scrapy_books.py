import requests
from bs4 import BeautifulSoup
from lxml import etree
import pymysql
import time

books_title = list()
books_id = list()
books_img = list()
books_info = list()
books_describe = list()
books = list()


def get_html(url):
    heads = {
        'Host': 'book.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'utf-8',
        'Referer': 'https://book.douban.com/tag/?view=cloud',
        'Connection': 'keep-alive',
        'Cookie': 'bid=edDhrxT5-hM; gr_user_id=dd768f6d-27ca-43cc-b472-f98a954e75a0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1579074591%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D7uSpMkm7yrBI0bcV3xmZeG-F20is_TBxvY8OrC4QclvEqpleBm58SYwa96vcnjsQ%26wd%3D%26eqid%3Db4db93430009d6da000000035e1eb491%22%5D; _pk_id.100001.3ac3=76b08aaa266a6e2b.1578295503.9.1579075192.1579070800.; __yadk_uid=dZ28mjHCPwWkm1IZzyCMeQZchih5Xzch; __utma=30149280.909203084.1578295506.1579070617.1579074591.9; __utmz=30149280.1579070617.8.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.1328316708.1578295506.1579070617.1579074591.9; __utmz=81379588.1579070617.8.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=D885982C6BEEB9A30F9BACF3C4DC048BE|69d869de93a43f72df9913138260718e; ll="118228"; viewed="34913634_25862578_4913064_33395237_34855047_34874597"; ct=y; ap_v=0,6.0; __utmc=30149280; __utmc=81379588; _pk_ses.100001.3ac3=*; __utmb=30149280.5.10.1579074591; __utmb=81379588.5.10.1579074591; __utmt_douban=1; __utmt=1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    req = requests.get(url, headers=heads)
    print('url:' + url + "\nstatus:" + str(req.status_code))
    return req.content


def get_labels():
    with open('label.txt', 'r', encoding='utf-8') as f:
        html = etree.HTML(f.read())
        lbs = html.xpath('//a/text()')
        for i in lbs:
            print(i)


def has_title(tag):
    return tag.has_attr('title')


def judge_no_class(tag):
    return not tag.has_attr('class')


class Book(object):
    def __init__(self, book_id, book_title, book_img, book_info, book_description, book_label):
        self.book_id = book_id.strip()
        self.book_title = book_title.strip()
        self.book_img = book_img.strip()
        self.book_info = book_info.strip()
        self.book_description = book_description
        self.book_label = book_label

    def __str__(self):
        return "标识 :" + self.book_id + "\n书名:" + self.book_title + "\n信息:" + self.book_info + "\n描述:" \
               + self.book_description

    def get_id(self):
        return self.book_id

    def get_title(self):
        return self.book_title

    def get_img(self):
        return self.book_img

    def get_info(self):
        return self.book_info

    def get_description(self):
        return self.book_description

    def get_label(self):
        return self.book_label


def tags_to_books():
    tags = "%E5%B0%8F%E8%AF%B4"  # 文学
    index1 = 0
    index2 = 0
    for i in range(200, 500, 20):
        url = 'https://book.douban.com/tag/' + tags + "?start=" + str(i) + "&type=T"
        time.sleep(1)
        content = get_html(url)
        bs = BeautifulSoup(content, 'lxml')
        ids = bs.find_all("a", class_="nbg")
        img = bs.find_all("img", class_='')
        for i in img:
            books_img.append(i['src'])
        li = bs.find_all(has_title)
        for i in li:
            if not i.has_attr('href'):
                continue
            s = str(i['href'])
            book_id = s.split('/')[4]
            book_title = i['title']
            books_title.append(book_title)
            books_id.append(book_id)
        info = bs.find_all("div", class_='pub')
        for i in info:
            books_info.append(i.string)
        des = bs.find_all('p')
        for i in des:
            if not i.has_attr('class') and i.string is not None:
                books_describe.append(i.string)
        star = bs.find_all('span', class_='rating_nums')
        for i in star:
            books_info[index1] = books_info[index1].strip() + '/ ' + str(i.string).strip()
            index1 = index1 + 1
        nums = bs.find_all('span', class_='pl')
        for i in nums:
            books_info[index2] = books_info[index2] + '/ ' + str(i.string).strip()
            index2 = index2 + 1


def find(lb):
    label = lb
    for i in range(0, 1000, 20):
        url = 'https://book.douban.com/tag/' + label + "?start=" + str(i) + "&type=T"
        time.sleep(1)
        content = get_html(url)
        html = etree.HTML(content)
        li = html.xpath("//li[@class='subject-item']")
        if len(li) is 0:
            break
        for item in li:
            s = str(item.xpath('./div[1]/a[1]/@href'))
            id = s.split('/')[4].strip()
            if len(item.xpath('./div[2]/h2[1]/a[1]/@title')) is not 0:
                title = str(item.xpath('./div[2]/h2[1]/a[1]/@title')[0]).strip()  # title
            else:
                title = ' '
            if len(item.xpath('./div[2]/div[2]/span[2]/text()')) is not 0:
                star = str(item.xpath('./div[2]/div[2]/span[2]/text()')[0]).strip()  # star
            else:
                star = ' '
            if len(item.xpath('./div[2]/div[2]/span[3]/text()')) is not 0:
                number = str(item.xpath('./div[2]/div[2]/span[3]/text()')[0]).strip()  # number
            else:
                number = ' '
            if len(item.xpath('./div[1]/a[1]/img[1]/@src')) is not 0:
                img = str(item.xpath('./div[1]/a[1]/img[1]/@src')[0]).strip()  # img
            else:
                img = ' '
            if len(item.xpath(".//div[@class='pub']/text()")) is not 0:
                info = str(item.xpath(".//div[@class='pub']/text()")[0]).strip()  # pub
            else:
                info = ' '
            if len(item.xpath("./div[2]/p[1]/text()")) is not 0:
                description = str(item.xpath("./div[2]/p[1]/text()")[0]).strip()
            else:
                description = ' '
            info = info + " / " + star + " / " + number
            books.append(Book(id, title, img, info, description, label))
            # print(books[len(books) - 1])


def insert(cursor, book_id, book_title, book_pic, book_info, book_desc):
    sql = "insert into book values('" + book_id + "','" + book_title + "','" + book_pic + "','" + book_info + "','" \
          + book_desc + "')"
    res = 0
    print(sql)
    try:
        pass
        # res = cursor.execute(sql)
    except pymysql.err.IntegrityError:
        pass
    except pymysql.err.DataError:
        pass
    except pymysql.err.ProgrammingError:
        pass
    return res


def main():
    conn = pymysql.connect(host='59.110.152.111', user='test', database='books', password='875706055',
                           charset='utf8mb4')  # 去掉utf8
    cursor = conn.cursor()
    # tags_to_books()
    with open('label.txt', 'r', encoding='utf8') as f:
        labels = f.readlines()
        for label in labels:
            if len(label.strip()) is 0:
                continue
            books.clear()
            print('book label:'+label)
            find(label.strip())
            for i in range(0, len(books)):
                # if books_describe[i].find("'") is not -1 or books_describe[i].find('\"') is not -1:
                #    continue
                # books.append(Book(books_id[i], books_title[i], books_img[i], books_info[i], books_describe[i]))
                # print(books[len(books) - 1])
                insert(cursor, books[i].get_id(), books[i].get_title(), books[i].get_img(), books[i].get_info(),
                       books[i].get_description())
            conn.commit()


if __name__ == '__main__':
    main()
