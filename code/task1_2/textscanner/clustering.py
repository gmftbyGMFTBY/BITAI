#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.12.29

'''
    聚类算法对结果聚类
'''

def KMeans(TF_IDF, K):
    '''
        输入TF-IDF权重矩阵，还有K个要分的簇
    '''
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters = K)
    km.fit(TF_IDF)

    clusters = km.labels_.tolist()
    return clusters

if __name__ == "__main__":
    pass
