#!/usr/bin/python3

# 该模块用来清理语料库中的异常编码文件

import os
import glob

ans = glob.glob('./*')

delete = []

for i in ans:
    inner = glob.glob('%s/*' % i)
    dn = []
    for j in inner:
        try:
            f = open(j, 'r')
            a = f.read()
            f.close()
        except:
            dn.append(j)
            f.close()
    delete.append(dn)
    print(len(dn), len(inner))

'''
for i in delete:
    for j in i:
        ans = os.system('rm %s' % j)
        if ans != 0 : print('...')
'''
