import numpy as np
import pymysql
from numpy import float32
import math
import time
import json
import redis

mp = {}
rmp = []


def get_data(dt, users):
    # 与数据库建立连接
    conn = pymysql.connect(host='127.0.0.1', user='root', database='bookstore', password='875706055',
                           charset='utf8mb4')  # 去掉utf8
    cursor = conn.cursor()
    sql = 'select user_id,book_id,star from mark'
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    books = {}
    # item 中的内容分别为作者 书名 评分
    for item in data:
        if item[1] not in mp:
            mp[item[1]] = id
            rmp.append(item[1])
            id += 1
        user_id = item[0]
        book_id = mp[item[1]]
        mark = item[2]
        # users数组为n行1列，记录的是所有评分的平方和，也就是相似度的分母部分
        users[user_id][0] += mark ** 2
        if book_id not in books:
            books[book_id] = []
        # books存储的是对某一本书有评分的所有人，一行就是一本书，每个元素就是评分用户和评分的元组。
        books[book_id].append((user_id, mark))
    for book in books:
        l = len(books[book])
        for i in range(0, l):
            for j in range(i + 1, l):
                # i,j分别为用户的id，通过枚举具有对相同图书评分的用户计算乘积和来计算相似度的分子
                dt[books[book][i][0]][books[book][j][0]] += books[book][i][1] * books[book][j][1]
    # 对users每一项开根号就是相似度的分母的一部分
    users = np.sqrt(users)


def get_similar(data, users):
    similar = [[] for i in range(0, 11800)]
    get_data(dt=data, users=users)
    for i in range(0, 11800):
        for j in range(i + 1, 11800):
            # i,j表示用户 当用户之间有交集的时候，计算相似度
            if data[i][j] != 0.0:
                temp = data[i][j] / (users[i][0] * users[j][0])
                similar[i].append((temp, j))
                similar[j].append((temp, i))
    for i in range(0, len(similar)):
        similar[i] = sorted(similar[i], key=lambda it: it[0], reverse=True)
    return similar


def get_favoriate():
    con = pymysql.connect(host='127.0.0.1', user='root', database='bookstore', password='875706055',
                          charset='utf8mb4')
    cursor = con.cursor()
    sql = 'select user_id,book_id,star from mark'
    cursor.execute(sql)
    result = cursor.fetchall()
    users = {}
    for item in result:
        user_id = item[0]
        book_id = mp[item[1]]
        star = item[2]
        if star < 3:
            continue
        if user_id not in users:
            users[user_id] = {}
        users[user_id][book_id] = star
    # users为二维字典，内部存储的数据为评分
    return users


def get_books(similar, users):
    books = {}
    l = len(similar)
    # i是user j也是user
    for i in range(0, l):
        books[i] = {}
        for item in similar[i]:
            simi = item[0]
            user_id = item[1]
            if user_id not in users:
                continue
            for book_id in users[user_id]:
                if book_id not in books[i]:
                    books[i][book_id] = 0
                books[i][book_id] += simi * users[user_id][book_id]
    return books


# 结果中有多少是预测正确的
def precision(users, books):
    l = len(users)
    total = 0.0
    ct = 1
    for i in range(0, l):
        cnt = 0
        if i not in books:
            continue
        for item in books[i]:
            if i not in users:
                continue
            if item in users[i]:
                cnt += 1
        if len(books[i]) != 0:
            ac = cnt/len(books[i])
            ct += 1
            total += ac
    return total/ct


# 原来的样本有多少是被正确预测的 召回率
def accuracy(users, books):
    l = len(users)
    total = 0.0
    ct = 1
    for i in range(0, l):
        cnt = 0
        if i not in users:
            continue
        for item in users[i]:
            if i not in books:
                continue
            if item in books[i]:
                cnt += 1
        if len(users[i]) != 0:
            ac = cnt/len(users[i])
            ct += 1
            total += ac
    return total/ct


def get_avg(books):
    total = 0.0
    cnt = 0
    for item in books:
        for it in books[item]:
            total += books[item][it]
            cnt += 1
    return total/cnt


def impl_books(books, avg, k):
    bk = {}
    l = len(books)
    for i in range(0, l):
        if i not in books or len(books[i]) == 0:
            continue
        bk[i] = {}
        for it in books[i]:
            if books[i][it] >= avg*k:
                bk[i][it] = books[i][it]
    return bk


def recommend(books, k):
    pool = redis.ConnectionPool(host='59.110.152.111', password='875706055', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    for user_id in books:
        re = ''
        for book in books[user_id]:
            book_id = rmp[book]
            star = books[user_id][book]
            if star > k:
                re += str(book_id)+":"+str(star)+','
        r.set("recommend"+str(user_id), re)


def main():
    begin = time.time()
    data = np.zeros((11800, 11800), dtype=float32)
    users_ = np.zeros((11800, 1), dtype=float32)
    similar = get_similar(data, users_)
    users = get_favoriate()
    books = get_books(similar, users)
    avg = get_avg(books)
    print(avg)
    for k in range(1, 21):
        bk = impl_books(books, avg, k)
        acc = accuracy(users, bk)
        pre = precision(users, bk)
        print('k: '+str(k)+"acc: "+str(acc)+"pre: "+str(pre))
        end = time.time()
        print('time: '+str(end-begin))
    recommend(books, avg*10)


if __name__ == '__main__':
    main()
