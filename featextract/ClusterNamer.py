'''
Created on Mar 2, 2014

Creates the clusters and clustersProb files which allow to extract the predominating
words and to measure the goodness of the grouping.

@author: rojosewe
'''
import pickle

structsfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/44snub/'
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/44snub/clusters/'
k = 562

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def getNames():
    f = open(datafolder + '../clustersProb.csv', 'wb')
    e = open(datafolder + '../clusters.csv', 'wb')
    for i in range(k+1):
        print i 
        out = open(datafolder + 'POS/count'+str(i)+'.csv', 'rb')
        line = out.readline()
        clusterdesc = ""
        numinst = float(line.split(' ')[0])
        if(int(numinst) > 0):
            line = out.readline()
            firstword = line.split('\t')[0]
            firstcount = float(line.split('\t')[1])
            line = out.readline()
            secondword = line.split('\t')[0]
            secondcount = float(line.split('\t')[1])
            line = out.readline()
            thirdword = line.split('\t')[0]
            thirdcount = float(line.split('\t')[1])
            clusterdesc = "cluster " + str(i) + ":, " + firstword + "*" + str((firstcount)/numinst) + ", "
            clusterdesc = clusterdesc + secondword + "*" + str((secondcount)/numinst) + ", "
            clusterdesc = clusterdesc + thirdword + "*" + str((thirdcount)/numinst) + ", "
            f.write(clusterdesc + "\n")
            clusterdesc = "cluster " + str(i) + ":, " + firstword + ","+ secondword + ","+ thirdword
        else:
            firstword = 0
            clusterdesc = ""
            f.write(clusterdesc + "\n")
        out.close()
        e.write(clusterdesc + "\n")
    f.close()
    e.close()

def main():
    getNames()
  
if __name__ == '__main__':
    main()