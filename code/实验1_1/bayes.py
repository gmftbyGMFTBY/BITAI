#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.12.26

'''
本文件是对中文的垃圾邮件分类系统，使用朴素贝叶斯算法作为分类器
对于中文的分词使用jieba等包进行相关处理

1. 忽略未登录词造成的影响
2. 邮件前缀加入消除操作
3. 标点符号过滤，特殊符号过滤
'''

import jieba
import glob
import numpy as np

def loaddataset():
    filte = [',', '.', ' ', '\n', '\t', '?', '!', '(', ')', '{', '}', '[', ']', '/', '-', '=', '+', '%', '#', '@', '~', '$', '^', '&', '*', '_', ':', ';', '\'', '"', '！', '。', '，', '（', '）', '：', '？', '￥', '＠', '＆', '‘', '“', '；', '｛', '｝', '－' ,'＋', '＝', '─', '》', '《', '☆', '、', '…', '\\', '|', '━', '／', 'ノ', '⌒', '〃', '⌒', 'ヽ', '”', '◇', '\u3000', '～', '╭', '╮', '〒', '失敗', '〒', '╭', '╮', 'Ω', '≡', 'ξ', '◤', 'μ', 'Θ', '◥', '█', '敗', '◤', '▎', 'υ', 'Φ', '│', '╰', '╯', '【']
    postinglist = []
    en_zh_filter = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＳＴＵＶＷＸＹＺ'
    # 数据集加载
    classvec = []
    # 加载训练集
    spam = glob.glob('data/new/train/spam/*')
    for i in spam:
        with open(i, 'r') as f:
            content = []
            meet = 0
            for i in f.readlines():
                if 'X-Mailer' in i or 'Content-Type' in i or 'X-MimeOLE' in i or 'Errors-To' in i or 'Content-Transfer-Encoding' in i or 'Message-Id' in i or 'Subject' in i:
                    meet = 1
                    continue
                elif meet != 0:
                    line = jieba.lcut(i, HMM=True)
                    for i in line:
                        if i not in filte and i.isnumeric() == False:
                            for k in i:
                                if k in en_zh_filter:
                                    break
                            else:
                                content.append(i)
            postinglist.append(content)
            classvec.append(1)
    ham = glob.glob('data/new/train/ham/*')
    for i in ham:
        with open(i, 'r') as f:
            content = []
            meet = 0
            for i in f.readlines():
                if 'X-Mailer' in i or 'Content-Type' in i or 'X-MimeOLE' in i or 'Errors-To' in i or 'Content-Transfer-Encoding' in i or 'Message-Id' in i or 'Subject' in i:
                    meet = 1
                    continue
                elif meet != 0:
                    line = jieba.lcut(i, HMM=True)
                    for i in line:
                        if i not in filte and i.isnumeric() == False:
                            for k in i:
                                if k in en_zh_filter:
                                    break
                            else:
                                content.append(i)
            postinglist.append(content)
            classvec.append(0)
    return postinglist, classvec

def createvocablist(dataset):
    vocabset = set([])
    for i in dataset:
        vocabset = vocabset | set(i)
    return list(vocabset)

def bagofwords2vec(vacoblist, inputset):
    # 返回文档的词袋模型
    returnvec = [0] * len(vocablist)
    for word in inputset:
        if word in vocablist:
            returnvec[vocablist.index(word)] += 1
        else:
            print('[%s] 不在词汇特征表中,自动忽略未登录词词' % word)
    return returnvec

def trainNB(trainndarray, traincategory):
    # 训练朴素贝叶斯分类器
    numtraindocs = len(trainndarray)
    numwords = len(trainndarray[0])
    pab = sum(traincategory) * 1.0 / numtraindocs   # P(c)
    p0num = np.zeros(numwords)
    p1num = np.zeros(numwords)
    p0denom = 0.0
    p1denom = 0.0
    for i in range(numtraindocs):
        # 广播运算
        if traincategory[i] == 1:
            p1num += trainndarray[i]
            p1denom += sum(trainndarray[i])
        else:
            p0num += trainndarray[i]
            p0denom += sum(trainndarray[i])
    p1vect = np.zeros(numwords)
    p0vect = np.zeros(numwords)
    for ind, i in enumerate(p1num):
        if i == 0 :
            p1vect[ind] = 0
        else:
            p1vect[ind] = i * 1.0 / p1denom
    for ind, i in enumerate(p0num):
        if i == 0:
            p0vect[ind] = 0
        else:
            p0vect[ind] = i * 1.0 /p0denom
    return p0vect, p1vect, pab

def classify(vec2classify, p0vect, p1vect, pclass1):
    # 朴素贝叶斯分类器
    p1 = sum(vec2classify * p1vect) + np.log(pclass1)
    p0 = sum(vec2classify * p0vect) + np.log(1 - pclass1)
    if p1 > p0:
        # 分类为垃圾邮件
        return 1
    else:
        # 分类为正常邮件
        return 0

if __name__ == "__main__":
    data, label = loaddataset()
    vocablist = createvocablist(data)
    a = ['我','真','的','是','非常','抱歉','啊','我']
    trainndarray = []
    length = len(data)
    for ind, i in enumerate(data):
        trainndarray.append(bagofwords2vec(vocablist, i))
        print('训练集加载 :', ind / length, end='\r')
    p0v, p1v, pab = trainNB(np.array(trainndarray), np.array(label))
    thisdoc = np.array(bagofwords2vec(vocablist, a))
    ans = classify(thisdoc, p0v, p1v, pab)
    if ans == 0: ans = '正常邮件'
    else : ans = '垃圾邮件'
    print('朴素贝叶斯分类器归类邮件为 :', ans)
