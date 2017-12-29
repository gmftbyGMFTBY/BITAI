#!/usr/bin/python3
# Author : GMFTBY, shaw, sunny
# Time   : 2017.12.29

'''
1. 语料库架加载模块
2. 加载语料库中的数据
3. 分词，引入停用词(jieba / 我们的模块)
'''

import os
import jieba    # 这里可以改成我们的模块,仅做测试使用
import glob
import os
import random

def read_kind(kind = 'NULL', count=0):
    '''
        1. 根据种类kind读取语料库中count个数据文件
        2. 返回文档的列表，每一个元素是一个文档字符串
    '''
    ans = glob.glob('../data/train/%s/*' % kind)
    length = len(ans)
    result = []
    if length == 0 : 
        print('请输入正确的分类')
        return
    else:
        if count > length : count = length
        print('分类正确，返回 %d 个文档' % count)
        # 打乱顺序，保证随机性
        random.shuffle(ans)
    i = 0
    index = 0
    while i < count :
        try:
            if index >= count :
                print('可用编码文件数目不足')
                return 
            with open(ans[i], 'r') as f:
                result.append(f.read())
                i += 1
                index += 1
        except:
            print('一个文件编码出错')
            index += 1
    return result

def read_stopwords():
    '''
        读取中文停用词后返回停用词列表
    '''
    with open('../data/train/stopwords', 'r') as f:
        content = f.read()
    return content.split()

if __name__ == "__main__":
    # ans = read_kind('C19-Computer', 10)
    # print(len(ans))
