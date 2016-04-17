'''
Created on Feb 9, 2014

@author: rojosewe
'''

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
            pos = tokensxline[1]
            chooseCounter(pos, token.upper())
        else:
            print len(tokensxline)

def printFiles():
    nounOut = open('nouns.txt', 'a')
    for key in nounDict:
        nounOut.write(key+"\t"+str(nounDict[key])+"\n")
    nounOut.close()
    
    verbOut = open('verbs.txt', 'a')
    for key in verbDict:
        verbOut.write(key+"\t"+str(verbDict[key])+"\n")
    verbOut.close()
    
    adjOut = open('adjs.txt', 'a')
    for key in adjDict:
        adjOut.write(key+"\t"+str(adjDict[key])+"\n")
    adjOut.close()

def main():
    posFile = '/home/rojosewe/Dropbox/MAI90/tesis/docs/POSTagResult.txt'
#     wordcount(posFile)
#     printFiles()

if __name__ == '__main__':
    adjDict = {}
    verbDict = {}
    nounDict = {}
    main()