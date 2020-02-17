# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 19:56:22 2020

@author: surpraka
"""

import os
import csv
import pandas as pd

def readCommonXpathsFromObjectRepo():
    print("Searching in Common Repo.......")
    dic = {}
    filePath = "ObjectMap/Common/BasePage.txt";
    
    with open(filePath) as csv_file :

        csv_reader = csv.reader(csv_file,delimiter=';')
        line_count=0
        for row in csv_reader:
            if line_count==0:
                line_count+=1
            else:
                dic[row[1]] = row[2]
    return dic    
        

def readXpathsFromObjectRepo(name):
    dic = {}
    print("Searching in Page Specific Repo.......")
    
    if('.txt' not in name):
        filepath = "ObjectMap/"+name+".txt"
    else:
        filepath = name
    
    if(os.path.exists(filepath)):
        print(name+".txt file exists")
        pass
    else:
        print("Making file with the name "+name+".txt")
        f= open(filepath,"w+")
        f.close()
# =============================================================================
# read the elements and xpaths for current page from object map to dictionary
# =============================================================================
    with open(filepath) as csv_file :

        csv_reader = csv.reader(csv_file,delimiter=';')
        line_count=0
        for row in csv_reader:
            if line_count==0:
                line_count+=1
            else:
                dic[row[1]] = row[2]
    
    return dic

def updateDictionary(flag,elementName,dic,elementXpath,filepath):
    
        #if element found and not in dictionary then update dictionary
        if(flag==1):
            if not elementName in dic.keys():
                dic[elementName] = elementXpath
        # write dictionary to csv file of object map for current page
        df = pd.DataFrame( [(k,v) for k,v in dic.items()],columns = ['key','value'])
        df.to_csv(filepath,sep = ';')
        print("**************** Element "+elementName+" stored into page "+filepath+"**************")