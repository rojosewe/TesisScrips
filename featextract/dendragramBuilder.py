'''
Created on Feb 22, 2014

After the hierarchical clustering has been built, 
It uses the linkage values to construct the clusters per se
writing the results in the labels.csv file. 

@author: rojosewe
'''
import pickle
from scipy.cluster.hierarchy import linkage, dendrogram
import pylab
import fastcluster
import scipy.cluster.hierarchy as sch
import csv
import numpy as np 

structfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/44/'
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/44snub/'

def loadDistanceMatrix():
    dfile = open(structfolder + 'distanceMatrix5000.pkl', 'rb')
    distMatrix = pickle.load(dfile)
    dfile.close();
    return distMatrix

def loadLinkage():
    lfile = open(structfolder + 'linkage.pkl', 'rb')
    link = pickle.load(lfile)
    lfile.close();
    return link

def saveLinkage(distanceMatrix):
#     link = linkage(distanceMatrix, 'ward')
    link = fastcluster.linkage(distanceMatrix, method='ward') # D-distance matrix
    afile = open(structfolder + 'wardlinkage.pkl', 'wb')
    pickle.dump(link, afile);
    afile.close();
    return link

def loadFCluster():
    afile = open(structfolder + 'fcluster5000.pkl', 'rb')
    fc = pickle.load(afile)
    afile.close();
    print len(fc)

def main():
#     distMatrix = loadDistanceMatrix()
#    linkage = saveLinkage(distMatrix)
#     linkage = loadLinkage()
#     loadFCluster()
#     R = dendrogram(linkage, truncate_mode='level',  p=4, show_contracted=True)
#     afile = open(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/R5000.pkl', 'wb')
#     pickle.dump(R, afile);
#     afile.close();
    linkage = loadLinkage()
    print len(linkage)
    k = 1.5
#   18 -> 54 
#   19 -> 46 
    
    R = dendrogram(linkage, color_threshold=6.8, show_contracted=True)
    pylab.savefig( "/home/rojosewe/Dropbox/MAI90/tesis/images/wordClustering/dgram446.8.png" )
#    print "cheese!"
    T = sch.fcluster(linkage, k, 'distance')
    n = len(T)
 #   print len(T)
    # calculate labels
    labels = np.zeros((n, 1))
    print str(k) + ": " + str(max(T))
    for i in range(n):
        labels[i,0] = int(T[i]);
    with open(datafolder + 'labels.csv', 'wb') as csvfile:
        csvw = csv.writer(csvfile);
        for i in range(n):
            csvw.writerow(labels[i,:])
            
    print 'done writing'

if __name__ == '__main__':
    main()
