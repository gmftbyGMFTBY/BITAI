#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.12.29

'''
    计算TF-IDF权值
'''

import numpy as np

def cal_TFIDF(docndarray):
    '''
        输入的是VSM模型构建的词袋向量
        词袋向量是numpy数组

        返回TF-IDF矩阵
    '''
    # IDF
    doc_num = docndarray.shape[0]
    # 计算每一个词出现的文件的个数
    column_count = [1.0 * len(np.nonzero(docndarray[:, i])[0]) for i in range(docndarray.shape[1])]
    column_count = np.array(column_count)
    column_count += 1
    column_count = doc_num / column_count
    IDF = np.log(column_count)    # 避免某一个词不出现的情况

    # TF
    for i in docndarray:
        sum_count = sum(i)
        if sum_count == 0 : sum_count = 1
        i = i * 1.0 / sum_count

    # TF-IDF (n, m) x (m, m) 矩阵相乘
    TF_IDF = docndarray * IDF
    return TF_IDF

if __name__ == "__main__":
   a = np.array([[1, 2, 3, 4], [0, 1, 4, 2], [1,0,2,3], [1, 1, 1, 1], [1, 0,1,2]])
   p = cal_TFIDF(a)
   print(p)
