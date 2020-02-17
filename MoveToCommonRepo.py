"""
/**********************************************************************
* RoboTester Version 1.0
* PUBLICIS SAPIENT PROPRIETARY/CONFIDENTIALs
* Use is subject to Organization terms
* @author Varun Sharma,Ashok Yadav & Suraj Prakash
* @since version 1.0
************************************************************************/
"""


import csv
import os
import Dictionary
import pandas as pd

def updatefile(updatedlist,filePath):
    with open(filePath,"w",newline="") as f:
        Writer=csv.writer(f)
        Writer.writerows(updatedlist)
        print(filePath+ " File has been updated")

def deleteCommonXpathsFromPageObjectRepo(commonELementsdic):
    
    files = []
    for i in os.listdir("ObjectMap/"):
        i = "ObjectMap/"+i
        if i.endswith('.txt'):
            files.append(i)
    
    for filePath in files:
        elementsDic = Dictionary.readXpathsFromObjectRepo(filePath)
        
        for elementKey in elementsDic:
            for commonKey in commonELementsdic:
                if(elementKey == commonKey):
                    try :
                        elementsDic = {key:val for key, val in elementsDic.items() if key != elementKey}
                        print("Deleted element "+commonKey+" from page "+filePath)
                    except KeyError:
                        pass
        
        df = pd.DataFrame( [(k,v) for k,v in elementsDic.items()],columns = ['key','value'])
        df.to_csv(filePath,sep = ';')
        
        
def moveElementToCommonRepo(dic):
    filePath = "ObjectMap/Common/BasePage.txt";
    
    for key, value in dic.items():
        dic = Dictionary.readCommonXpathsFromObjectRepo()
        Dictionary.updateDictionary(1,key,dic,value,filePath)
    

def fetchCommonXpathsFromObjectRepo():
    files = []
    for i in os.listdir("ObjectMap/"):
        i = "ObjectMap/"+i
        if i.endswith('.txt'):
            files.append(i)
    
    listOfkeys = []
    listofXpaths = []
    
    for filePath in files:
        print(filePath)
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
    
    # To maintain order of elements and respective xpaths
    commonELementsdic = {}
    for i in range(0,len(listOfkeys)):
        if(listOfkeys[i] in commonKeys):
            commonELementsdic[listOfkeys[i]] = listofXpaths[i] 
            
    #Move Common Elements
    moveElementToCommonRepo(commonELementsdic)
    
    #Delete Common Elements
    deleteCommonXpathsFromPageObjectRepo(commonELementsdic)