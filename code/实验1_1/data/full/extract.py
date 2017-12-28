#!/usr/bin/python3

# extract the data , 200 - spam, 200 - ham , 100 - test_data

import os
import glob
import random

with open('index', 'r') as f:
    item = f.read()
    items = item.split('\n')

# 训练集
spam_count = 0    # 垃圾邮件的个数
ham_count  = 0    # 正常邮件的个数
spam_list = []
ham_list  = []
index_list = []

# 测试集
test_count = 0
test_list  = []

# 抽取训练集
for i in items:
    if i.strip() == '': continue
    label, path = i.split()
    for_count = 0
    if label == 'spam' : for_count = spam_count
    else : for_count = ham_count

    if ham_count == 200 and spam_count == 200 : break
    if label == 'ham' and ham_count == 200 : continue
    if label == 'spam' and spam_count == 200 : continue

    ans = os.system('iconv -f GBK -t UTF-8 %s > ../new/train/%s/%s' \
            % (path, label, str(for_count)))
    if ans != 0:
        # 转换出错，结果不可信
        os.system('\rm ../new/train/%s/%s' % (label, str(for_count)))
    else:
        if label == 'spam' : 
            spam_count += 1
            spam_list.append('../new/train/%s/%s' % (label, str(for_count)))
        else : 
            ham_count += 1
            ham_list.append('../new/train/%s/%s' % (label, str(for_count)))
    index_list.append(path)

# 抽取测试集
length = len(items)
times  = 0
while True:
    index = random.randint(0, length - 1)
    i = items[index].split()[1]
    if i in index_list : continue
    else:
        ans = os.system('iconv -f GBK -t UTF-8 %s > ../new/test/%s' % (i, str(times)))
        if ans != 0:
            os.system('\rm ../new/test/%s' % str(times))
        else:
            times += 1
            test_list.append(i)
        if times == 500 : break
