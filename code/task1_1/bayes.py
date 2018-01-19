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
    for ii in spam:
        with open(ii, 'r') as f:
            content = []
            meet = 0
            for i in f.readlines():
                if 'X-Mailer' in i or 'Content-Type' in i or 'X-MimeOLE' in i or 'Errors-To' in i or 'Content-Transfer-Encoding' in i or 'Message-Id' in i or 'Subject' in i:
                    meet = 1
                    continue
                elif meet != 0:
                    line = jieba.lcut(i, HMM=True)
                    for p in line:
                        if p not in filte and p.isnumeric() == False:
                            for k in p:
                                if k in en_zh_filter:
                                    break
                            else:
                                content.append(p)
            postinglist.append(content)
            classvec.append(1)
    ham = glob.glob('data/new/train/ham/*')
    for ii in ham:
        with open(ii, 'r') as f:
            content = []
            meet = 0
            for i in f.readlines():
                if 'X-Mailer' in i or 'Content-Type' in i or 'X-MimeOLE' in i or 'Errors-To' in i or 'Content-Transfer-Encoding' in i or 'Message-Id' in i or 'Subject' in i:
                    meet = 1
                    continue
                elif meet != 0:
                    line = jieba.lcut(i, HMM=True)
                    for p in line:
                        if p not in filte and p.isnumeric() == False:
                            for k in p:
                                if k in en_zh_filter:
                                    break
                            else:
                                content.append(p)
            postinglist.append(content)
            classvec.append(0)
    return postinglist, classvec

def createvocablist(dataset):
    vocabset = set([])
    for i in dataset:
        vocabset = vocabset | set(i)
    return list(vocabset)

def bagofwords2vec(vocablist, inputset):
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

def train_error_count():
    # 检测训练集错误率,正确率
    data, label = loaddataset()
    vocablist = createvocablist(data)

    sum_count   = len(data)
    error_count = 0
    right_count = 0
    zhaohui_count = 0

    trainndarray = []
    for ind, i in enumerate(data):
        trainndarray.append(bagofwords2vec(vocablist, i))
        print('训练集加载 :', ind / sum_count, end = '\r')
    p0v, p1v, pab = trainNB(np.array(trainndarray), np.array(label))
    for ind, i in enumerate(data):
        thisdoc = np.array(bagofwords2vec(vocablist, i))
        ans = classify(thisdoc, p0v, p1v, pab)
        if ans == 0 and label[ind] == 0 : right_count += 1
        if ans == 1 and label[ind] == 1 : zhaohui_count += 1
        print('训练集测试 :', ind / sum_count, end='\r')
    return right_count * 1.0 / (len(data) / 2), zhaohui_count * 1.0 / (len(data) / 2)

def loaddatatest():
    # 加载测试集
    filte = [',', '.', ' ', '\n', '\t', '?', '!', '(', ')', '{', '}', '[', ']', '/', '-', '=', '+', '%', '#', '@', '~', '$', '^', '&', '*', '_', ':', ';', '\'', '"', '！', '。', '，', '（', '）', '：', '？', '￥', '＠', '＆', '‘', '“', '；', '｛', '｝', '－' ,'＋', '＝', '─', '》', '《', '☆', '、', '…', '\\', '|', '━', '／', 'ノ', '⌒', '〃', '⌒', 'ヽ', '”', '◇', '\u3000', '～', '╭', '╮', '〒', '失敗', '〒', '╭', '╮', 'Ω', '≡', 'ξ', '◤', 'μ', 'Θ', '◥', '█', '敗', '◤', '▎', 'υ', 'Φ', '│', '╰', '╯', '【']
    postinglist = []
    en_zh_filter = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＳＴＵＶＷＸＹＺ'
    tests = glob.glob('data/new/test/*')
    tests.sort()
    for ii in tests:
        with open(ii, 'r') as f:
            content = []
            meet = 0
            for i in f.readlines():
                if 'X-Mailer' in i or 'Content-Type' in i or 'X-MimeOLE' in i or 'Errors-To' in i or 'Content-Transfer-Encoding' in i or 'Message-Id' in i or 'Subject' in i:
                    meet = 1
                    continue
                elif meet != 0:
                    line = jieba.lcut(i, HMM=True)
                    for p in line:
                        if p not in filte and p.isnumeric() == False:
                            for k in p:
                                if k in en_zh_filter:
                                    break
                            else:
                                content.append(p)
            postinglist.append(content)
    label = []
    with open('test_label', 'r') as f:
        for i in f.readlines():
            if 'spam' in i : label.append(1)
            else : label.append(0)
    return postinglist, label

def test_error_count():
    # 检测测试集错误率
    data, label = loaddataset()
    vocablist = createvocablist(data)
    testdata, testlabel = loaddatatest()
    sum_count   = len(testdata)
    error_count = 0
    right_count = 0
    zhaohui_count = 0

    trainndarray = []
    lenp = len(data)
    for ind, i in enumerate(data):
        trainndarray.append(bagofwords2vec(vocablist, i))
        print('测试集加载 :', ind / lenp, end = '\r')
    p0v, p1v, pab = trainNB(np.array(trainndarray), np.array(label))
    for ind, i in enumerate(testdata):
        thisdoc = np.array(bagofwords2vec(vocablist, i))
        ans = classify(thisdoc, p0v, p1v, pab)
        if ans == 0 and testlabel[ind] == 0 : right_count += 1
        if ans == 1 and testlabel[ind] == 1 : zhaohui_count += 1
        print('测试集测试 :', ind / sum_count, end= '\r')
        if ind == 10 : break
    return right_count * 1.0 / (sum_count / 2), zhaohui_count * 1.0 / (sum_count / 2)

def save_model(p0v, p1v, pab):
    # 模型序列化
    with open('model', 'w') as f:
        f.write(str(p0v) + '\n')
        f.write(str(p1v) + '\n')
        f.write(str(pab) + '\n')

def load_model():
    with open('model', 'r') as f:
        p0v = float(f.readline())
        p1v = float(f.readline())
        pab = float(f.readline())
    print(p0v, p1v, pab)
    return p0v, p1v, pab

if __name__ == "__main__":
    '''
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
    '''
    print()
    ans2, ans3 = train_error_count()
    print('训练集正确率，召回率 :', ans2, ans3)
