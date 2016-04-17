'''
Created on Mar 1, 2014

@author: rojosewe
'''
import MySQLdb as mdb
import pickle
from gensim import corpora, models
import logging
import csv
import numpy as np

numTopics = 120
words = []
con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNCToWork')
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/76LDA/'
structsfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/76LDA/'

def wordChecker():
    wordAppear = {}
    wordCounter = 0;
    for i in range(len(words)):
        word = words[i];
        wordCounter = wordCounter + 1;
        cur = con.cursor() 
        cur.execute("SELECT row FROM work WHERE service REGEXP '[[:<:]]"+word.replace("(","").replace(")","").replace("\"", "")+"[[:>:]]'");
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

def textBuilder(wordAppear):
    keys = wordAppear.keys()
    keys.sort()
    texts = []
    for key in keys:  
        appearing = []
        for value in wordAppear[key]:
            appearing.append(words[value])
        texts.append(appearing)
    file2 = open(structsfolder + 'listOfTexts.pkl', 'wb')
    pickle.dump(texts, file2)
    file2.close()
    return texts

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def dictionaryBuilder(wordAppear, texts):
    dictionary = corpora.Dictionary(texts)
    dictionary.save(structsfolder + 'LDADict.dict')
    return dictionary

def corpusBuilder(dictionary, texts):
    corpus = [dictionary.doc2bow(text) for text in texts]
    pickleSave(structsfolder + 'LDACorpus.mm', corpus)
    return corpus
    
def corpus2Topics(dictionary, corpus, numTopics):
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=numTopics) # initialize an LSI transformation
    lsi.save(structsfolder + 'corpusLDA.lsi')
    topics = lsi.print_topics(numTopics-1);
    f = open(datafolder + 'LDAtopics.txt', 'wb')
    for topic in topics:
        f.write(topic + "\n")
    f.close()

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
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    posFile = datafolder + 'singleWords50w.csv'
    wordReader(posFile);
#     wordAppear = wordChecker()
    wordAppear = dictLoader()
#     wordAppear = excludeByCSV(wordAppear)
    texts = textBuilder(wordAppear)
    dictionary = dictionaryBuilder(wordAppear, texts)
    corpus = corpusBuilder(dictionary, texts)
    corpus2Topics(dictionary, corpus, numTopics)
    

if __name__ == '__main__':
    main()
