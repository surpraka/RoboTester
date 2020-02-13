# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:17:43 2020

@author: surpraka
"""
import csv
import os

def readCommonXpathsFromObjectRepo():
    files = []
    for i in os.listdir("ObjectMap/"):
        i = "ObjectMap/"+i
        if i.endswith('.txt'):
            files.append(i)
    
    listOfkeys = []
    listofXpaths = []

    for filePath in files:
        with open(filePath) as csv_file :
            csv_reader = csv.reader(csv_file,delimiter=';')
            line_count=0
            for row in csv_reader:
                if line_count==0:
                    line_count+=1
                else:
                    listOfkeys.append(row[1])
                    listofXpaths.append(row[2])
            
    commonKeys = set([x for x in listOfkeys if listOfkeys.count(x) > 1])
    commonXpaths = set([x for x in listofXpaths if listofXpaths.count(x) > 1])
    print(commonKeys)
    print(commonXpaths)
    
if __name__ == "__main__":
    readCommonXpathsFromObjectRepo()
    