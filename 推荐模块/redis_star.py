import redis
import pymysql
import time

pool = redis.ConnectionPool(host='59.110.152.111', password='875706055', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

con = pymysql.connect(host='127.0.0.1', user='root', database='bookstore', password='875706055',
                         charset='utf8mb4')
cursor = con.cursor()
# sql = 'select book_id,avg(star) from mark group by book_id'
sql = 'select user_id,book_id from mark group by user_id'
cursor.execute(sql)
result = cursor.fetchall()
ct = 0
start = time.time()
for item in result:
    r.set('star'+str(item[0]), str(item[1]))
    print(item[0])
    # print(item[0], item[1])
    # ct += 1
    # if ct==20:
    #     break
end = time.time()
print(end-start)