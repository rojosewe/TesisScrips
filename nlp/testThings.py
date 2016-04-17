'''
Created on Mar 2, 2014

@author: rojosewe
'''
import pickle
from gensim import models, corpora, similarities
import MySQLdb as mdb

structsfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/76LDA/'
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/76LDA/'
words = []
con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNCToWork')

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def wordReader(posFile):
    f = open(posFile, 'r')
    wc = 0;
    for line in f:
        words.append(line.strip());
        wc = wc + 1;
    return wc;

def dictLoader():
    file2 = open(structsfolder + 'wordAppeareanceNum30.pkl', 'rb')
    wordAppear = pickle.load(file2)
    file2.close()
    return wordAppear

def main():
    tts = {}
    for i in range(350):
        tts[i] = []
    posFile = datafolder + 'singleWords50w.csv'
    wordReader(posFile);
    wordAppear = dictLoader()
    
    topics = pickleLoad(structsfolder + 'topicDict.pkl')
    keys = topics.keys()
    keys.sort()
    for key in keys:
        if len(topics[key]) > 0:
            topic = topics[key][0][0]
            tts[topic].append(key)
        
    for key in tts.keys():
        print key
        f = open(datafolder + 'LDA/sents'+str(key)+'.txt', 'wb')
        cur = con.cursor()
        inp = ', '.join(str(x) for x in tts[key]) 
        sql = "SELECT service FROM work WHERE row IN ("+inp+")"
        cur.execute(sql);
        for j in range(cur.rowcount):
            result = cur.fetchone()
            sent = result[0]
            f.write(sent + "\n")
        f.close()
    

if __name__ == '__main__':
    main()