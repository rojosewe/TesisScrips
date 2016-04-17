'''
Created on Feb 22, 2014

Retrieve the sentences from the Database after they have been clustered and 
save them in the sentsXX.txt files. 

@author: rojosewe
'''
import pickle
import pylab
import csv
import numpy as np
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNCToWork')
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/44snub/'
structfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/44snub/'
sentsfolder = 'clusters/'
wordCount = 3920
clustnum = 563

def csvReader(datafolder):
#     matrixfile = 'featMatrix26000.csv';
    labelsfile = 'labels.csv';
    #     data = genfromtxt(datafolder + matrixfile, delimiter=',')
    lbss = np.loadtxt(datafolder + labelsfile, delimiter=',', ndmin=1)
    labels = np.zeros((len(lbss), 1))
    for i in range(len(lbss)):
        lbl = lbss[i];
        labels[i,0] = lbl;
#     dt = np.concatenate(data, labels)
    return np.array(labels); 

def dictLoader():
    afile = open(structfolder + 'sampleDict.pkl', 'rb')
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

def wordCounterByCluster(Y,clusterid, wordAppear, datafolder):
    dit = {}
    indxs = []
    keys = wordAppear.keys()
    keys.sort()
    kk = []
    for index, item in enumerate(Y):
        if item == clusterid:
            indxs.append(index)
    for indx in indxs:
        kk.append(keys[indx])
    f = open(datafolder + sentsfolder + 'sents'+str(clusterid)+'.txt','wb')
    if len(kk) > 0:
        inp = ', '.join(str(k) for k in kk) 
        cur = con.cursor()
        sql = "SELECT service FROM work WHERE row IN ("+inp+")"
        cur.execute(sql);
        for j in range(cur.rowcount):
            result = cur.fetchone()
            service = result[0]
            f.write(service+"\n") # python will convert \n to os.linesep
    f.close()

def main():
    
    labels = csvReader(datafolder);
    print max(labels)
    wordAppear = dictLoader();
#     rowCount = len(wordAppear)
#     featMatrix = matrixInit(rowCount, wordCount);
#     featMatrix = markMatrixColIfWordPresent(wordAppear, featMatrix, rowCount, wordCount)
#     for i in range(len(labels)):
#         featMatrix[i,wordCount-1] = labels[i];
    for i in range(clustnum + 1):
        print i
        wordCounterByCluster(labels, i, wordAppear, datafolder)

if __name__ == '__main__':
    main()
