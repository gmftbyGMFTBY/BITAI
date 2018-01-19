#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.12.29

'''
PCA 降维模块
'''

from sklearn.decomposition import PCA

def create_PCA(TF_IDF, weight):
    pca = PCA(n_components = weight)
    X = pca.fit(TF_IDF)
    return X
