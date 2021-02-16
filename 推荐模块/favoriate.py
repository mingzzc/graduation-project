import pymysql
import redis


def fun():
    con = pymysql.connect(host='127.0.0.1', user='root', database='bookstore', password='875706055',
                             charset='utf8mb4')
    cursor = con.cursor()
    sql = 'select user_id,book_id,star from mark'
    cursor.execute(sql)
    result = cursor.fetchall()
    users = {}
    for item in result:
        user_id = item[0]
        book_id = item[1]
        star = item[2]
        if user_id not in users:
            users[user_id] = []
        users[user_id].append((star, book_id))
    for key in users:
        users[key] = sorted(users[key], key=lambda x: x[0])
        users[key] = users[key][0:20]
        with open('user.txt', 'a') as f:
            f.write(str(key)+" "+str(users[key]))


def main():
    con = pymysql.connect(host='127.0.0.1', user='root', database='bookstore', password='875706055',
                          charset='utf8mb4')
    cursor = con.cursor()
    sql = 'select book_id from mark'
    cursor.execute(sql)
    data = cursor.fetchall()
    pool = redis.ConnectionPool(host='59.110.152.111', password='875706055', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    lists = []
    for item in data:
        key = 'star' + str(item[0])
        value = r.get(key)
        print(type(value))
        lists.append((key, value))
    print(type(lists[0][1]))
    lists = sorted(lists, key=lambda x: x[1], reverse=True)
    print(lists[0:50])
    s = ''
    for i in range(0, 100):
        s += str(lists[i][0][4:])+":"+lists[i][1].decode()+","
    r.set("top", s)


if __name__ == '__main__':
    main()
