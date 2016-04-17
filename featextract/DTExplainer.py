'''
Created on Feb 22, 2014

Makes a Decision tree out of the clustered Data to understand the clustering
separation decisions.


@author: rojosewe
'''
import pickle
from scipy.cluster.hierarchy import linkage, dendrogram
import pylab
import fastcluster
import scipy.cluster.hierarchy as sch
import csv
import numpy as np
from numpy import genfromtxt
from featextract.dimReduction import rowCounter
from sklearn import tree
import pydot
from sklearn.externals.six import StringIO

def csvReader(datafolder):
#     matrixfile = 'featMatrix26000.csv';
    labelsfile = 'labels402.csv';
    #     data = genfromtxt(datafolder + matrixfile, delimiter=',')
    lbss = np.loadtxt(datafolder + labelsfile, delimiter=',', ndmin=1)
    labels = np.zeros((len(lbss), 1))
    for i in range(len(lbss)):
        lbl = lbss[i];
        labels[i,0] = lbl;
#     dt = np.concatenate(data, labels)
    return np.array(labels); 

def dictLoader():
    afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/sampleDict260002.pkl', 'rb')
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
            featMatrix[count-1, word] = 1;
    return featMatrix

def matrixInit(rowCount, wordCount):
    featMatrix = np.zeros((rowCount, wordCount));
    return featMatrix;

def treeMaker(X, Y, outfolder):
    for index, item in enumerate(Y):
        if not (item == 1):
            Y[index] = 0
    S = set(Y[:,0])
    print S
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    print 'TREE FITTED'
    dot_data = StringIO() 
    tree.export_graphviz(clf, out_file=dot_data)
    print 'TREE EXPORTED' 
    with open(outfolder + "wordtree2cluster1.dot", 'wb') as f:
        f = tree.export_graphviz(clf, out_file=f)
    print 'TREE EXPORTED TO DOT'    
#     graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
#     graph.write_pdf(outfolder + "wordtree2.pdf")
#     print 'TREE SAVED' 
    

def main():
    wordCount = 4381+1
    datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/'
    imgfolder = '/home/rojosewe/Dropbox/MAI90/tesis/images'
    labels = csvReader(datafolder);
    wordAppear = dictLoader();
    rowCount = len(wordAppear)
    featMatrix = matrixInit(rowCount, wordCount);
    featMatrix = markMatrixColIfWordPresent(wordAppear, featMatrix, rowCount, wordCount)
#     for i in range(len(labels)):
#         featMatrix[i,wordCount-1] = labels[i];
    treeMaker(featMatrix, labels, imgfolder)
    print 'done'

if __name__ == '__main__':
    main()
