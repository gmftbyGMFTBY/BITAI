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
# __all__  = ['loadcorpus', 'clustering', 'VSM', 'TFIDF', 'PCA', 'visualization']
# __name__ = 'textscanner'

# 测试代码块
import loadcorpus as tl
import clustering as tc
import visualization as tv
import VSM as tV
import PCA as tP
import TFIDF as tT

def test():
    kind_list = ['C3-Art', 'C19-Computer', 'C7-History', 'C32-Agriculture', 'C31-Enviornment']
    stopwords = tl.read_stopwords()
    doc = []
    for i in kind_list:
        ans = tl.read_kind(i, 200)
        for j in ans:
            doc.append(tl.cut_without_stopwords(j, stopwords))
    print('分词完成')
    pdoc = []
    for i in doc:
        con = ' '.join(i)
        pdoc.append(con)
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()    
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(pdoc))
    word = vectorizer.get_feature_names() #所有文本的关键字
    weight = tfidf.toarray()              #对应的tfidf矩阵
    '''
    ans, bag = tV.create_VSM(doc)
    print('词袋模型构建完毕')
    TF_IDF = tT.cal_TFIDF(ans)
    print('TF-IDF权重矩阵计算完毕')
    # TF_IDF = tP.create_PCA(TF_IDF, int(0.1 * TF_IDF.shape[1]))
    '''
    cluster = tc.KMeans(weight, len(kind_list))
    print('获得分类结果')
    return cluster, kind_list

if __name__ == "__main__":
    ans, kind = test()
    # 计算平均正确率
    length = len(kind)
    from collections import Counter
    sump = 0
    for i in range(length):
        pause = ans[i * 100 : i * 100 + 99]
        print(pause)
        w = Counter(pause)
        top = w.most_common(1)[0][1]
        sump += top
    print(ans)
    print('平均正确率:', sump / length)
