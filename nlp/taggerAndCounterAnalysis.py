'''
Created on Feb 24, 2014

@author: rojosewe
'''
import os
import operator

basicfolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/44snub/'
datafolder = basicfolder + 'clusters/'
k = 563
words = set()

def wordReader(posFile):
    f = open(posFile, 'r')
    wc = 0;
    for line in f:
        words.add(line.strip());
        wc = wc + 1;
    return wc;

def countVerb(token):
    if token in verbDict:
        if len(token.strip()) > 0:
            verbDict[token] = verbDict[token] + 1
    else:
        verbDict[token] = 1

def countNoun(token):
    if token in nounDict:
        if len(token.strip()) > 0:
            nounDict[token] = nounDict[token] + 1
    else:
        nounDict[token] = 1

def countAdj(token):
    if token in adjDict:
        if len(token.strip()) > 0:
            adjDict[token] = adjDict[token] + 1
    else:
        adjDict[token] = 1

def chooseCounter(pos, token):
    if "NC" in pos[:2]:
        countNoun(token)
    elif "V" in pos[:1]:
        countVerb(token)
    elif "ADJ" in pos[:3]:
        countAdj(token)
        
def wordcount(inFileName):
    f = open(inFileName, 'r')
    for line in f:
        tokensxline = line.split("\t")
        token = ""
        if len(tokensxline) == 3:
            # 0 for words, 1 for lemmas, 2 for PoS
            token = tokensxline[0]
            print token
            pos = tokensxline[1]
            chooseCounter(pos, token.upper())
        else:
            print len(tokensxline)

def printCount(numlines, f):
    out = open(f, 'wb')
    nouns = set(nounDict.keys())
    verbs = set(verbDict.keys())
    adjs = set(adjDict.keys())
    allDict = {}
    keywords = nouns.union(verbs.union(adjs))
    print str(len(keywords)) + " words"
#     keywords = keywords.intersection(words)
    print "converted to " + str(len(keywords))
    out.write(str(numlines) + " instances\n")
    for key in keywords:
        key = key.upper()        
        count = 0
        if(key in nounDict):
            count = count + nounDict[key]
        if(key in verbDict):
            count = count + verbDict[key]
        if(key in adjDict):
            count = count + adjDict[key]
        allDict[key] = count
    sorted_all = sorted(allDict.iteritems(), key=operator.itemgetter(1))
    sorted_all.reverse()
    for pair in sorted_all:
        out.write(pair[0]+"\t"+str(pair[1])+"\n")
    out.close()
    
def extractKeywords(k):
    for i in range(0,k):
        command = "cd /home/rojosewe/Dropbox/MAI90/tesis/NLP/TreeTagger"
        command = command + "&& cat "+datafolder+"sents"+str(i)+".txt | cmd/tree-tagger-spanish > "+datafolder+"words"+str(i)+".txt"
        os.system(command)


def main():
#    filename = "/home/rojosewe/Dropbox/MAI90/tesis/data/incclusters/sents12.txt"
#    print len(open(filename).readlines())
#    sys.exit()
    posFile = basicfolder + 'singleVerbs.csv'
    wordReader(posFile);
    extractKeywords(k)
    for i in range(0,k):
        f = datafolder + "sents"+str(i)+".txt"
        out = open(f, 'rb')
        numlines = len(out.readlines())
        out.close()
        adjDict.clear()
        verbDict.clear()
        nounDict.clear()
        f = datafolder + 'words'+str(i)+'.txt'
        wordcount(f)
        f = datafolder + 'POS/count'+str(i)+'.csv'
        printCount(numlines, f)
        
    
if __name__ == '__main__':
    adjDict = {}
    verbDict = {}
    nounDict = {}
    main()
