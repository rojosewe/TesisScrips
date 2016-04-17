'''
Created on Feb 26, 2014

Use KNN to classify the sentences according to the clustered sentences.
write the putput to knnclasses.csv

@author: rojosewe
'''
import pickle
import numpy as np
from sklearn import neighbors, tree
import random
import sys
import csv

structsfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/44snub/'
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/44snub/'

def labelsReader():
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

def loadWholeDict():
    afile = open(structsfolder + 'wordAppeareanceNum30.pkl', 'rb')
    wordAppear = pickle.load(afile)
    afile.close()
    return wordAppear 

def dictLoader():
    afile = open(structsfolder + 'sampleDict.pkl', 'rb')
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

def wordReader():
    f = open(datafolder + 'singleWords50w.csv', 'rb')
#     wc = 0;
#     for line in f:
#         wc = wc + 1;
    wc = len(f.readlines())
    f.close()
    return wc;
    

def redistributeLabels(rowCount, labels):
    wa = {}
    afile = open(structsfolder + 'sampleDict.pkl', 'rb')
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

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def classify(train, labels, predict, thr):
    knn = neighbors.KNeighborsClassifier(n_neighbors=3, weights='distance',algorithm='ball_tree',metric='jaccard', leaf_size=12)
    knn.fit(train, np.ravel(labels))
    probs = knn.predict_proba(predict)
    #print "score: " + str(knn.score(predict, np.ravel(predictLabels)))
    classedlabels = []
    classedThreshold = []
    for indx,prob in enumerate(probs): 
        m = max(prob)
        mindx = [u for u, v in enumerate(prob) if v == m]
        if len(mindx) > 0:
            topic = mindx[0]
            classedlabels.append((indx, topic))
            if(m > thr):
                classedThreshold.append((indx, topic))
            else:
                classedThreshold.append((indx, -1))
        else:
            classedThreshold.append((indx, -1))
    pickleSave(structsfolder + 'knnprobs.pkl', probs)
    pickleSave(structsfolder + 'classedlabels.pkl', classedlabels)
    pickleSave(structsfolder + 'classedThreshold.pkl', classedThreshold)
    return classedlabels
    
def chooseRandSample(wordAppear, sampleSize):
    keys = wordAppear.keys()
    rand = random.sample(keys, sampleSize)
    dup = {}
    for r in rand:
        dup[r] = wordAppear[r]
#     afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/sampleDict30.pkl', 'wb')
#     pickle.dump(dup, afile);
#     afile.close();
    return dup

def removeDuplicates(wordAppear, rowCount, wordCount):
    uniqueValues = set()
    deleted = {}
    for key in wordAppear.keys():
        nl = wordAppear[key]
        strr = ', '.join(str(x) for x in nl)
        if not strr in uniqueValues:
            uniqueValues.add(strr)
        else:
            deleted[key] = nl
            del wordAppear[key]
    pickleSave(structsfolder + 'deleted.pkl', deleted)
    return wordAppear

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
    wordCount = wordReader();
    classedlabels = labelsReader();
    unclassedDict = loadWholeDict();
    unclassedDict = excludeByCSV(unclassedDict)
#     unclassedDict = removeDuplicates(unclassedDict, len(unclassedDict), wordCount)
    print len(unclassedDict)
    cDict = dictLoader();
    classedDict = {}
    for key in cDict.keys():
        classedDict[key] = unclassedDict[key] 
    for key in classedDict.keys():
#         if key in unclassedDict:
            del unclassedDict[key]
#     classedDict = chooseRandSample(classedDict, 1000)
#     unclassedDict = chooseRandSample(unclassedDict, 2000)
#     wordAppear = chooseRandSample(wordAppear, 1000)
#     rowCount = len(wordAppear)
#     print rowCount
    pickleSave(structsfolder + 'unclassedDict.pkl', unclassedDict)
    sys.exit()
    classedMatrix = matrixInit(len(classedDict), wordCount);
    classedMatrix = markMatrixColIfWordPresent(classedDict, classedMatrix, len(classedDict), wordCount)

    unclassedMatrix = matrixInit(len(unclassedDict), wordCount);
    unclassedMatrix = markMatrixColIfWordPresent(unclassedDict, unclassedMatrix, len(unclassedDict), wordCount)
    
#     samplesize = math.floor(rowCount*0.15)
#     randa = random.sample(range(1,rowCount), int(samplesize))
#     all = set(range(1,rowCount))
#     trainindxs = list(all.difference(randa))
#     testindxs = list(all.intersection(randa))
    
#     trainData = featMatrix[trainindxs]
#     trainLabels = labels[trainindxs]
#     testData = featMatrix[testindxs]
#     testLabels =  labels[testindxs]
    classes = classify(classedMatrix, classedlabels, unclassedMatrix, 0.5)
    with open(datafolder + 'knnclasses.csv', 'wb') as csvfile:
        csvw = csv.writer(csvfile);
        for i in range(len(classes)):
            csvw.writerow(classes[i])

if __name__ == '__main__':
    main()