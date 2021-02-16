import csv

res = []
books = {}
with open('BX-Book-Ratings.csv', 'rb') as f:
    reader = f.readlines()
for item in reader:
    try:
        it = str(item, encoding='gbk')
        its = it.strip()
        if its.split(';')[2] == '"0"':
            continue
        if its.split(';')[1] not in books:
            books[its.split(';')[1]] = 1
        else:
            books[its.split(';')[1]] += 1
            res.append(its)
    except UnicodeDecodeError:
        continue
print(len(books))
ct = 0
for item in books:
    if books[item] > 1:
        ct += 1

print(ct)
with open('../ids.txt', 'r') as f:
    ids = f.readlines()
mp = {}
userdict = {}
index = 0
for item in books:
    if books[item] == 1:
        continue
    mp[item] = ids[index].strip()
    index += 1
pre = '-1'
id = 0
usercount = {}
for item in res:
    user = item.split(';')[0]
    if user not in usercount:
        usercount[user] = 1
    else:
        usercount[user] += 1
for item in res:
    user = item.split(';')[0]
    if usercount[user] < 4:
        continue
    if user != pre:
        id = id + 1
        userdict[user] = id
        pre = user

with open('user.txt', 'w') as f:
    for item in res:
        user = item.split(';')[0]
        if usercount[user] < 4:
            continue
        t1 = userdict[item.split(';')[0]]
        t2 = mp[item.split(';')[1]]
        s3 = item.split(';')[2]
        t3 = int((int(s3[1:len(s3)-1])+1)/2)
        f.write(str(t1)+","+str(t2)+","+str(t3)+"\r")
print(len(userdict))
print(len(mp))
