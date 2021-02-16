import pymysql


def fun():
    mp = {}
    with open('tag/tags.txt', 'r', encoding='UTF-8') as f:
        tags = f.readlines()
    with open('tag/tags1.txt', 'r', encoding='UTF-8') as t:
        temp = t.readlines()
    for it in temp:
        tags.append(it)
    for item in tags:
        tg = item.strip().split(' ')
        if len(tg) <= 1:
            continue
        tag = tg[1]
        if tag not in mp:
            mp[tag] = 1
        else:
            mp[tag] += 1
    mp = sorted(mp.items(), key=lambda x: x[1], reverse=True)
    print(mp)
    with open('mp.txt', 'w', encoding='UTF-8') as f:
        for item in mp:
            if item[1] > 4:
                f.write(item[0] + ' ' + str(item[1]) + '\r')


def main():
    con = pymysql.connect(host='127.0.0.1', user='root', password='875706055', database='bookstore',
                           charset='utf8mb4')
    cursor = con.cursor()
    with open('mp.txt', 'r', encoding='UTF-8') as f:
        items = f.readlines()
    tags = {}
    cnt = 1
    for te in items:
        item = te.strip().split(' ')
        tags[item[0]] = cnt
        cnt += 1
    with open('tag/tags1.txt', 'r', encoding='UTF-8') as f:
        items = f.readlines()
    for item in items:
        item = item.strip()
        tag = item.split(' ')
        if len(tag) < 2:
            continue
        if tag[1] not in tags:
            continue
        sql = 'insert into book_labels(book_id,label_id) value(%s,%s)' % (tag[0], tags[tag[1]])
        print(sql)
        try:
            cursor.execute(sql)
        except pymysql.err.IntegrityError:
            pass
    con.commit()


if __name__ == '__main__':
    main()
