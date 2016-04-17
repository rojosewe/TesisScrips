'''
Created on Feb 25, 2014

@author: rojosewe
'''

from nltk.corpus import wordnet as wn
import numpy as np

words = [];

def calculateDistance(word1, word2):
    w1 = wn.synset(word1)
    w2 = wn.synset(word2)
    return w1.path_similarity(w2)

def wordReader(posFile):
    f = open(posFile, 'r')
    wc = 0;
    for line in f:
        words.append(line.strip());
        wc = wc + 1;
    return wc;

def main():
    posFile = '/home/rojosewe/Dropbox/MAI90/tesis/data/singleWords50w.csv'
    wordCount = wordReader(posFile);
    wordDistance = array
    
if __name__ == '__main__':
    main()