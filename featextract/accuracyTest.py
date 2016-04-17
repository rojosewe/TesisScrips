'''
Created on Mar 2, 2014

After Clustering and KNN to NLP procedures it counts how many times the 
predominating word appears in the services. making an approximate accuracy test 
to the NLP classification. 

@author: rojosewe
'''
import pickle

structsfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/44snubs'
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/NLP/75/clusters/'
k = 75

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def countUnclassed():
    classedlabels = pickleLoad(structsfolder + 'classedThreshold.pkl')
    counter = {}
    counter[-1] = 0
    for i in range(75):
        counter[i] = 0
    for i in range(len(classedlabels)):
        c = classedlabels[i][1]
        counter[c] = counter[c] + 1
    sum = 0
    for i in range(75):
        sum = sum + counter[i] 
    print counter
    print sum
    
def checkNNsAccuracy():
    exclude = [44]
    total = 0
    acc = 0
    for i in range(k):
        if not i in exclude: 
            out = open(datafolder + 'POS/count'+str(i)+'.csv', 'rb')
            line = out.readline()
            numinst = line.split(' ')[0]
            if(int(numinst) > 0):
                line = out.readline()
                firstword = line.split('\t')[1]
            else:
                firstword = 0
            total = total + int(numinst)
            acc = acc + int(firstword)
            out.close()
        else:
            print 'here'
    accuracy = (acc*100)/total
    print accuracy
def main():
#    corpus = pickleLoad(r'/home/rojosewe/Dropbox/MAI90/tesis/structs/LDACorpus.mm')
    checkNNsAccuracy()
  
if __name__ == '__main__':
    main()