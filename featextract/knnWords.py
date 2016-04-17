'''
Created on Feb 26, 2014

@author: rojosewe
'''
import pickle
import numpy as np
from sklearn import neighbors, tree
import random
import math

def csvReader(datafolder):
#     matrixfile = 'featMatrix26000.csv';
    labelsfile = 'labels30.csv';
    #     data = genfromtxt(datafolder + matrixfile, delimiter=',')
    lbss = np.loadtxt(datafolder + labelsfile, delimiter=',', ndmin=1)
    labels = np.zeros((len(lbss), 1))
    for i in range(len(lbss)):
        lbl = lbss[i];
        labels[i,0] = lbl;
#     dt = np.concatenate(data, labels)
    return np.array(labels); 

def dictLoader():
    afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/sampleDict30.pkl', 'rb')
    wordAppear = pickle.load(afile)
    afile.close()
    return wordAppear

def markMatrixColIfWordPresent(wordAppear, featMatrix, rowCount, wordCount):
    count = 0
    keys = wordAppear.keys()
    keys.sort()
    for row in keys:
        count  = count + 1
        words = wordAppear[row]
        for word in words:  
#             print count, word
            if count-1 < rowCount:
                featMatrix[count-1, word] = 1;
    return featMatrix

def matrixInit(rowCount, wordCount):
    featMatrix = np.zeros((rowCount, wordCount));
    return featMatrix;

def wordReader(datafolder):
    f = open(datafolder + 'singleWords50w.csv', 'rb')
#     wc = 0;
#     for line in f:
#         wc = wc + 1;
    wc = len(f.readlines())
    f.close()
    return wc;
    

def redistributeLabels(rowCount, labels):
    wa = {}
    afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/sampleDict30.pkl', 'rb')
    wa = pickle.load(afile)
    afile.close()
    keys = wa.keys()
    keys.sort()
    biglabels = np.ones((rowCount, 1))
    biglabels = np.negative(biglabels)
    for index, item in enumerate(keys):
        if item-1 < rowCount:
            biglabels[item,0] = labels[index,0]
    return biglabels    

def separateMatrixByrows(featMatrix, wordcount, classedindxs):
    matrix = np.zeros((len(classedindxs), wordcount));
    for index, item in enumerate(classedindxs):
        matrix[index] = np.copy(featMatrix[item[0],:])
    return matrix

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

def main():
    datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/'
    wordCount = wordReader(datafolder);
    labels = csvReader(datafolder);
    print max(labels)
    wordAppear = dictLoader();
    rowCount = len(wordAppear)
    print rowCount
    featMatrix = matrixInit(rowCount, wordCount);
    featMatrix = markMatrixColIfWordPresent(wordAppear, featMatrix, rowCount, wordCount)
    knn = neighbors.KNeighborsClassifier(n_neighbors=5, weights='distance',algorithm='ball_tree',metric='jaccard', leaf_size=30)
    knn.fit(featMatrix, np.ravel(labels))
    

if __name__ == '__main__':
    main()
