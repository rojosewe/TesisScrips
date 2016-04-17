'''
Created on Mar 2, 2014

@author: rojosewe
'''
import logging
from gensim import models, corpora, similarities
import pickle

words = []
wordDict = {}
numTopics = 100
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/76LDA/'
structsfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/76LDA/'

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

def textBuilder(wordAppear):
    keys = wordAppear.keys()
    keys.sort()
    texts = []
    for key in keys:  
        appearing = []
        for value in wordAppear[key]:
            appearing.append(words[value])
        texts.append(appearing)
        wordDict[key] = appearing 
    return texts

def classify(dictionary, lsi, corpus):
    topicDict = {}
    keys = wordDict.keys()
    keys.sort()
    f = open(datafolder + 'labels.csv', 'wb')
#     index = similarities.MatrixSimilarity(lsi[corpus])
    for key in keys:
        vec_bow = dictionary.doc2bow(wordDict[key])
        vec_lsi = lsi[vec_bow]
#         sims = index[vec_lsi]
#         sims = sorted(enumerate(sims), key=lambda item: -item[1])
        topicDict[key] = sorted(vec_lsi, key=lambda item: item[1], reverse=True)
#         print topicDict[key]
        f.write(str(topicDict[key][0][0])+'\n')
    f.close()
    return topicDict

def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    posFile = datafolder + 'singleWords50w.csv'
    wordAppear = dictLoader()
    wordReader(posFile);
    texts = textBuilder(wordAppear)
    dictionary = corpora.Dictionary.load(structsfolder + 'LDADict.dict')
    lda = models.LdaModel.load(structsfolder + 'corpusLDA.lsi')
    corpus = pickleLoad(structsfolder + 'LDACorpus.mm')
    topicDict = classify(dictionary, lda, corpus)
    pickleSave(structsfolder + 'topicDict.pkl', topicDict)
    

if __name__ == '__main__':
    main()
