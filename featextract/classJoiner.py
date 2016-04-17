'''
Created on Mar 2, 2014

@author: rojosewe
'''
import pickle
import numpy as np
import csv

structfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/44snub/'
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/44snub/'

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def csvReader(filename, ndim):
    csv = np.loadtxt(filename, delimiter=',', ndmin=ndim)
    return csv 

def getSampled():
    sampled = {}
    sample = pickleLoad(structfolder + 'sampleDict.pkl')
    classes = csvReader(datafolder + 'labels.csv', 1)
    keys = sample.keys()
    keys.sort()
    for i, key in enumerate(keys):
        sampled[key] = classes[i]
    return sampled

def getKnned():
    knned = {}
    sample = pickleLoad(structfolder + 'unclassedDict.pkl')
    classes = pickleLoad(structfolder + 'classedlabels.pkl')
    keys = sample.keys()
    keys.sort()
    for key in keys:
        if key in classes:
            knned[key] = classes[key]
        else:
            knned[key] = -1
    return knned

def getRemoved(joint, jointclass):
    removed = {}
    deleted = pickleLoad(structfolder + 'deleted.pkl')
    strjoint = []
    for key in joint.keys():
        nl = joint[key]
        strjoint.append(', '.join(str(x) for x in nl))
    for item in deleted.items():
        tofind = ', '.join(str(x) for x in item[1])
        matched = strjoint.index(tofind)
        removed[item[0]] = jointclass.values()[matched]
    removedkeys = removed.keys()
    removedkeys.sort()
    pair = []
    for key in removedkeys:
        pair.append((key,removed[key]))
    pickleSave(structfolder + 'deletedClass.pkl', removed)
    with open(datafolder + 'removedclasses.csv', 'wb') as csvfile:
        csvw = csv.writer(csvfile);
        for p in pair:
            csvw.writerow(p)
#     [i for i, v in enumerate(L) if v[0] == 53]
#     for i in range(len(joint)):
        
    return removed

def joinDicts():
    knn = pickleLoad(structfolder + 'unclassedDict.pkl')
    sample = pickleLoad(structfolder + 'sampleDict.pkl')
    joint = dict(knn.items() + sample.items())
    return joint

def joinClasses(sampled, knned):
    joint = dict(sampled.items() + knned.items())
    return joint

def main():
    sampled = getSampled()
    knned = getKnned()
#     joint = joinDicts()
    jointclass = joinClasses(sampled, knned)
#     removed = getRemoved(joint, jointclass)
#     jointclass = joinClasses(jointclass, removed)
    pickleSave(structfolder + 'jointclass.pkl', jointclass)
    skeys = jointclass.keys()
    skeys.sort()
    out = open(datafolder + 'allclasses.csv', 'wb')
    for k in skeys:
        out.write(str(jointclass[k])+"\n")
    out.close()
  
if __name__ == '__main__':
    main()