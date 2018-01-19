#!/usr/bin/python3
# Author : GMFTBY, shaw, sunny
# Time   : 2017.12.29

'''
    构建词袋模型
'''

import numpy as np

def create_VSM(cut_docs):
    '''
        1. 输入为已经停用词分结果的分词矩阵，每一行是一个文档的分词列表
        2. 输出词袋模型向量,还有词袋模型
    '''
    # 构建词袋
    word_bag = set()
    for i in cut_docs:
        word_bag |= set(i)
    word_bag = list(word_bag)
    result = []
    for doc in cut_docs:
        array = []
        for i in word_bag:
            array.append(doc.count(i) * 1.0)
        result.append(array)
    # 返回numpy数组，便于进行之后的矩阵操作
    return np.array(result), word_bag

if __name__ == "__main__":
    # ans, bag = create_VSM([['爱', '上海', '爱', '中国'], ['中国', '伟大', '上海', '漂亮']])
    # print(ans, bag)
    pass
