'''
Created on Mar 2, 2014

@author: rojosewe
'''
import pickle
import numpy as np
import csv
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'hollywood1984', 'RNCToWork')
structfolder = '/home/rojosewe/Dropbox/MAI90/tesis/structs/75/'
datafolder = '/home/rojosewe/Dropbox/MAI90/tesis/data/75/'

def pickleSave(filename, object):
    file2 = open(filename, 'wb')
    pickle.dump(object, file2)
    file2.close()
    
def pickleLoad(filename):
    file2 = open(filename, 'rb')
    object = pickle.load(file2)
    file2.close()
    return object

def csvReader(filename):
    csv = np.loadtxt(filename)
    return csv 

def main():
#     wordAppear = pickleLoad(structfolder + 'sampleDict.pkl')
#     classes = csvReader(datafolder + 'classes.csv')
    transform = csvReader(datafolder + 'cluster2general.csv')
    for i in range(1,75):
        val = transform[i-1]
        cur = con.cursor()
        sql = "UPDATE work SET serviceClass = " + str(75 + val) + " WHERE serviceClass = " + str(i)
        cur.execute(sql)    
    con.commit()
    
  
if __name__ == '__main__':
    main()