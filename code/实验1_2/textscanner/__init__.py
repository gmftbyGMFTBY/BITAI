#!/usr/bin/python3
# Author : GMFTBY, shaw, sunny
# Time   : 2017.12.29

'''
模块简介:
    1. 目的 : 对文本进行聚类分析(对于文本的标签判定可以作为之后的补充内容)
    2. 算法 : 聚类 + PCA降维 + TF-IDF + VSM
    3. 语料库 : 复旦大学计算机信息与技术系国际数据库中心自然语言处理小组
    4. 环境 :
        * Python3.6
        * jieba
        * sklearn
        * matplotlib
        * numpy
'''

# 模块文件
__all__  = ['loadcorpus', 'clustering', 'VSM', 'TFIDF', 'PCA', 'visualization']
__name__ = 'textscanner'

# 测试代码块
import textscanner.loadcorpus as tl
import textscanner.clustering as tc
import textscanner.visualization as tv
import textscanner.VSM as tV
import textscanner.PCA as tP
import textscanner.TFIDF as tT
