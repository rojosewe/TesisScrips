'''
Created on Feb 23, 2014

@author: rojosewe
'''
from sklearn import decomposition
import MySQLdb as mdb
import numpy as np 
import pickle
import csv
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage,fcluster,dendrogram
from sklearn.cluster import DBSCAN
import random
import fastcluster
import pylab
import pylab as pl

wordAppear = {};
words = [];
con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNCToWork')
featMatrix = None;

def dictLoader():
    file2 = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/wordAppeareanceNum2.pkl', 'rb')
    wordAppear = pickle.load(file2)
    file2.close()
    return wordAppear

def wordReader(posFile):
    f = open(posFile, 'r')
    wc = 0;
    for line in f:
        words.append(line.strip());
        wc = wc + 1;
    return wc;

def removeDuplicates(wordAppear, rowCount, wordCount):
    uniqueValues = set()
    for key in wordAppear.keys():
        nl = wordAppear[key]
        strr = ', '.join(str(x) for x in nl)
        if not strr in uniqueValues:
            uniqueValues.add(strr)
        else:
            del wordAppear[key]
    return wordAppear

def chooseRandSample(wordAppear, sampleSize):
    keys = wordAppear.keys()
    rand = random.sample(keys, sampleSize)
    dup = {}
    for r in rand:
        dup[r] = wordAppear[r]
    return dup

def rowCounter():
    cur = con.cursor()
    sql = "SELECT count(id) FROM work"
    cur.execute(sql)
    for i in range(cur.rowcount):
        result = cur.fetchone()
        rowCount = result[0]
    return rowCount;

def matrixInit(rowCount, wordCount):
    featMatrix = np.zeros((rowCount+1, wordCount));
    return featMatrix;

def markMatrixColIfWordPresent(wordAppear, featMatrix, rowCount, wordCount):
    count = 0
    keys = wordAppear.keys()
    keys.sort()
    for row in keys:
        count  = count + 1
        words = wordAppear[row]
        for word in words:  
#             print count, word
            featMatrix[count, word] = 1;
    return featMatrix

def main():
    posFile = '/home/rojosewe/Dropbox/MAI90/tesis/data/singleWords50.csv'
    wordCount = wordReader(posFile);
    rowCount = rowCounter()
    wordAppear = dictLoader();
    print len(wordAppear)
    wordAppear = removeDuplicates(wordAppear, rowCount, wordCount)
    wordAppear = chooseRandSample(wordAppear, 26000)
    print len(wordAppear)
    rowCount = len(wordAppear)
    print 'done loading'
#     witoutMatchesDeleter(wordAppear)
    featMatrix = matrixInit(rowCount, wordCount);
    print 'matrix created'
#     wordChecker();
    featMatrix = markMatrixColIfWordPresent(wordAppear, featMatrix, rowCount, wordCount)
    print 'matrix marked'
#     pca = decomposition.PCA(n_components=2)
#     print 'PCA init'
#     pca.fit(featMatrix)
#     print 'PCA fitted'
#     X = pca.transform(featMatrix)
#     print 'PCA transformed'
    print len( np.where(featMatrix[:, 2] == 1)[0])
    pl.scatter(range(26001), featMatrix[:, 2], s=1)
    pylab.savefig( "/home/rojosewe/Dropbox/MAI90/tesis/images/wordClustering/scatter.png" )
    

if __name__ == '__main__':
    main()