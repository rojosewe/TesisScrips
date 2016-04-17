'''
Created on Feb 17, 2014

Cluster maker.

@author: rojosewe
'''
import MySQLdb as mdb
import numpy as np 
import pickle
import csv
import sys
from scipy.spatial.distance import pdist
import random
import fastcluster

wordAppear = {};
words = []
con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNCToWork')
featMatrix = None;
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/44snub/'
structsfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/44snub/'

def wordReader(posFile):
    f = open(posFile, 'r')
    wc = 0;
    for line in f:
        words.append(line.strip());
        wc = wc + 1;
    return wc;

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def rowCounter():
    cur = con.cursor()
    sql = "SELECT count(id) FROM work"
    cur.execute(sql)
    for i in range(cur.rowcount):
        result = cur.fetchone()
        rowCount = result[0]
    return rowCount;

def matrixInit(rowCount, wordCount):
    featMatrix = np.zeros((rowCount, wordCount));
    return featMatrix;

        
def wordChecker():
    wordCounter = 0;
    for i in range(len(words)):
        word = words[i];
        wordCounter = wordCounter + 1;
        cur = con.cursor()
        sql = "SELECT row FROM work WHERE service REGEXP '[[:<:]]"+word+"[[:>:]]'" 
        cur.execute(sql);
        for j in range(cur.rowcount):
            result = cur.fetchone()
            row = result[0]
            if(row in wordAppear):
                wordAppear[row].append(i);
            else:
                wordAppear[row] = []
                wordAppear[row].append(i);
#         if(wordCounter%10 ==0):
        print str(wordCounter) + " words.";
        print str(len(wordAppear)) + " appearances.";
    afile = open(structsfolder + 'wordAppeareanceNum30.pkl', 'wb')
    pickle.dump(wordAppear, afile);
    afile.close();
    return wordAppear
    
def dictLoader():
    file2 = open(structsfolder + 'sampleDict.pkl', 'rb')
    wordAppear = pickle.load(file2)
    file2.close()
    return wordAppear

def witoutMatchesDeleter(wordAppear):
    rows = range(201753)
    empties = diff(rows, wordAppear.keys())
    for empty in empties:
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM dangerousQuery WHERE row = "+str(empty))
            con.commit()
            print 'delete ' + str(empty)
        except IOError as e:
            print e
    print 'done.'
    
def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]

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

def buildClusters(featMatrix):
    distanceMatrix = pdist(featMatrix[:,:], metric='jaccard')
    pickleSave(structsfolder + 'distanceMatrix.pkl', distanceMatrix)
#     ed = euclidean_distances(featMatrix[1:100,:], featMatrix[1:100,:])
    linkage = fastcluster.linkage(distanceMatrix, method='ward') # D-distance matrix
#     fc = fcluster(link, 30, criterion='maxclust')
    #R = dendrogram(link, color_threshold=0.3, leaf_font_size=6)
    #pylab.savefig( "/home/rojosewe/Dropbox/MAI90/tesis/images/wordClustering/featMatrix.png" )
    distanceMatrix = None
    pickleSave(structsfolder + 'linkage.pkl', linkage)
#     afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/fcluster260002.pkl', 'wb')
#     pickle.dump(fc, afile);
#     afile.close();
#     k = 40
#     n = len(linkage)
#     print n
#     
#     R = dendrogram(linkage, color_threshold=0.2*max(linkage[:,2]), show_contracted=True)
#     pylab.savefig( "/home/rojosewe/Dropbox/MAI90/tesis/images/wordClustering/dgramall.png" )
#     T = fcluster(linkage, k, 'maxclust')
# 
#     # calculate labels
#     labels = np.zeros((n, 1));
#     for i in range(n):
#         labels[i,0] = T[i];
#         
#         
#     with open('/home/rojosewe/Dropbox/MAI90/tesis/data/labelsall.csv', 'wb') as csvfile:
#         csvw = csv.writer(csvfile);
#         for i in range(n):
#             csvw.writerow(labels[i,:])
#     with open('/home/rojosewe/Dropbox/MAI90/tesis/data/flat260002.csv', 'wb') as csvfile:
#         csvw = csv.writer(csvfile);
#         for i in range(len(fc)):
#             csvw.writerow([i,fc[i]])

#     afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/distanceMatrix260003.pkl', 'wb')
#     pickle.dump(distanceMatrix, afile);
#     afile.close();

def writeMatrixToCSV(featMatrix, rowCount, wordCount):
    with open(datafolder + 'featMatrix30.csv', 'wb') as csvfile:
        csvw = csv.writer(csvfile);
        for i in range(rowCount):
            csvw.writerow(featMatrix[i,:])

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
    pickleSave(structsfolder + 'sampleDict.pkl', dup)
    return dup
    
def buildDBScan(X):
#     db = DBSCAN(eps=0.1, min_samples=20).fit(X)
# #     core_samples = db.core_sample_indices_
#     labels = db.labels_
#     # Number of clusters in labels, ignoring noise if present.
#     n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#     print('Estimated number of clusters: %d' % n_clusters_)
#     afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/dbscan.pkl', 'wb')
#     pickle.dump(db, afile);
#     afile.close();
#     afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/wordAppeardb.pkl', 'wb')
#     pickle.dump(db, afile);
#     afile.close();
    print ""
    
def csvReader(filename):
    csv = np.loadtxt(filename)
    return csv
    
def excludeByCSV(wordAppear):
    ffs = csvReader(datafolder + '44.csv')
    kk = set(wordAppear.keys()).difference(set(np.ravel(ffs)))
    for k in kk:
        del wordAppear[k]
    return wordAppear
    
     
def main():
    posFile = datafolder + 'singleVerbs.csv'
    wordCount = wordReader(posFile);
    rowCount = rowCounter()
#     rowCount = 120
    wordAppear = wordChecker()
    print len(wordAppear)
#     wordAppear = dictLoader();
    wordAppear = excludeByCSV(wordAppear)
    rowCount = len(wordAppear)
    print len(wordAppear)
#     sys.exit()
#     wordAppear = removeDuplicates(wordAppear, rowCount, wordCount)
#     wordAppear = chooseRandSample(wordAppear, 12000)
#     print len(wordAppear)
#     rowCount = len(wordAppear)
    print 'done loading'
#     witoutMatchesDeleter(wordAppear)
    featMatrix = matrixInit(rowCount, wordCount);
    print 'matrix created'
#     wordChecker();
    featMatrix = markMatrixColIfWordPresent(wordAppear, featMatrix, rowCount, wordCount)
    print 'matrix marked'
#    writeMatrixToCSV(featMatrix, rowCount, wordCount)
    print 'building clusters'
    buildClusters(featMatrix)
    print 'done'
#     buildDBScan(featMatrix)

if __name__ == '__main__':
    main()
