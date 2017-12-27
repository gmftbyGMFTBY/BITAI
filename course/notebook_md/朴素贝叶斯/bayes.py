#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.12.26
# 这是一个针对文本分类的python脚本，练习编写朴素贝叶斯分类器
# 文本分类的注意要点
# 1. 词条 : 
#       单词，IP地址，URL链接，其他任意连续的字符串
# 2. 将每一个文本表示成一个词条组成的向量
#       0表示没有出现过，1表示出现过
# 3. 确定分类类别
#       决定要将文本分类成哪几个类别
# 4. 注意事项
#       1. 去除文本的标点符号
#       2. 按照词条切分
#       3. 需要处理未登录词
#       4. 本示例只是一个二元分类问题，多分类问题修改即可
#       5. 在计算条件概率的时候，为了避免因为乘0导致的错误，我们初始化都是1
#       6. 避免下溢，采用对数求解条件概率
#       7. 词袋模型不同于词集模型，词袋模型需要考虑一下词出现的频度

import numpy as np
import re
import random

def loaddataset():
    # 数据集加载
    # postinglist是数据集，classvec是标签向量
    postinglist=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classvec = [0,1,0,1,0,1]
    return postinglist, classvec

def createvocablist(dataset):
    # 创建词汇表
    # 将所有文本中的所有词汇构成一个向量表
    vocabset = set([])
    for i in dataset:
        vocabset = vocabset | set(i)
    return list(vocabset)

def setofwords2vec(vocablist, inputset):
    # 返回文本的文档向量
    returnvec = [0] * len(vocablist)    # 初始化文档向量
    for word in inputset:
        if word in vocablist:
            returnvec[vocablist.index(word)] = 1
        else:
            print('[%s] 不在词汇表中' % word)
    return returnvec

def trainNB(trainndarray, traincategory):
    # 训练朴素贝叶斯分类器(计算条件概率)
    # trainndarray  : 文档矩阵 
    # traincategory : 文档矩阵中的类别向量
    numtraindocs = len(trainndarray)    # 文档矩阵，每一行是一个文本对应的词汇向量
    numwords = len(trainndarray[0])     # 词汇表的长度 = 特征的数目
    # 计算类别的概率
    pabusive = sum(traincategory) * 1.0 / numtraindocs    # P(c)类别的概率
    p0num = np.zeros(numwords)
    p1num = np.zeros(numwords)
    p0denom = 0.0
    p1denom = 0.0
    for i in range(numtraindocs):
        if traincategory[i] == 1:
            p1num += trainndarray[i]    # numpy广播运算，将第i个文本向量中出现的单词加入到p1num
            p1denom += sum(trainndarray[i])
        else:
            p0num += trainndarray[i]
            p0denom += sum(trainndarray[i])
    p1vect = np.zeros(numwords)
    p0vect = np.zeros(numwords)
    # 1类别的文本中每一个词出现的概率
    for ind, i in enumerate(p1num):
        if i == 0:
            p1vect[ind] = 0
        else:
            p1vect[ind] = i * 1.0 / p1denom
    for ind, i in enumerate(p0num):
        if i == 0:
            p0vect[ind] = 0
        else:
            p0vect[ind] = i * 1.0 / p0denom
    return p0vect, p1vect, pabusive

def classifyNB(vec2classify, p0vec, p1vec, pclass1):
    # 朴素贝叶斯分类器
    p1 = sum(vec2classify * p1vec) + np.log(pclass1)
    p0 = sum(vec2classify * p0vec) + np.log(1 - pclass1)
    if p1 > p0 : 
        return 1
    else:
        return 0

def test():
    listposts, listclasses = loaddataset()
    myvocablist = createvocablist(listposts)
    trainndarray = []
    for i in listposts:
        trainndarray.append(setofwords2vec(myvocablist, i))
    p0v, p1v, pab = trainNB(np.array(trainndarray), np.array(listclasses))
    testwords = ['stupid', 'garbage', 'worthless']
    testwords = ['love', 'my', 'dalmation']
    thisdoc = np.array(setofwords2vec(myvocablist, testwords))
    print('归类 :', classifyNB(thisdoc, p0v, p1v, pab))

def textparser(bigstring):
    # 正则抽取
    listtokens = re.split(r'\W*', bigstring)
    return [i.lower() for i in listtokens if len(i) > 0]

def spamtest():
    doclist = []
    classlist = []
    fulllist = []
    for i in range(1,26):
        filepath1 = './email/spam/%d.txt' % i
        f = open(filepath1, 'rb').read()
        s = f.decode('utf8')
        wordlist = textparser(s)
        doclist.append(wordlist)
        fulllist.extend(wordlist)
        classlist.append(1)
        filepath2 = './email/ham/%d.txt' % i
        f = open(filepath2, 'rb').read()
        s = f.decode('utf8')
        wordlist = textparser(s)
        doclist.append(wordlist)
        fulllist.extend(wordlist)
        classlist.append(0)
    vocablist = createvocablist(doclist)
    trainingset = range(50)    # 训练集规模
    testset = []               # 测试集
    # 从训练集中抽取测试集,并从训练集中删除
    for i in range(10):
        randindex = random.randint(0, len(trainingset) - 1)
        testset.append(trainingset[randindex])
        del(trainingset[randindex])
    trainndarray = []
    trainclasses = []
    for i in trainingset:
        trainndarray.append(setofwords2vec(vocablist, doclist[i]))
        trainclasses.append(classlist[i])
    p0v, p1v, pspam = trainNB(np.array(trainndarray), np.array(trainclasses))
    errorcount = 0

    for i in testset:
        wordvector = setofwords2vec(vocablist, doclist[i])
        if classifyNB(np.array(wordvector), p0v, p1v, pspam) != classlist[i]:
            errorcount += 1

    print('错误率 :', float(errorcount) / len(testset))

if __name__ == "__main__":
    spamtest()
