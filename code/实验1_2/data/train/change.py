#!/usr/bin/python3

# 该文件用来将编码同意转换成utf8

import os
import glob

ans = glob.glob('./*')
print(ans)

error_count = 0

for i in ans:
    a = os.system('enca -L zh_CN -x utf-8 %s/*' % i)
    if a != 0 : error_count += 1

print(error_count , len(ans))
    
