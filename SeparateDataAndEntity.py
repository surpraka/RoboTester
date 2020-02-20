"""
/**********************************************************************
* RoboTester Version 1.0
* PUBLICIS SAPIENT PROPRIETARY/CONFIDENTIALs
* Use is subject to Organization terms
* @author Varun Sharma,Ashok Yadav & Suraj Prakash
* @since version 1.0
************************************************************************/
"""

import re
from nltk.corpus import wordnet as wn

def checkFirstSentenceContainstVerb(phrases):
    for i in range(0,len(phrases)):
        phrases[i] = phrases[i].strip()
    
    wordset = phrases[0].split(" ")
    if(len(wordset[0]) == 0):
        wordset = phrases[1].split(" ")

    tmp = []
    
    for w in wordset:
        try:
            tmp.append(wn.synsets(w)[0].pos())
        except IndexError:
            pass

    return tmp    

def checkPOStag(sentence,info):
    phrases = sentence.split("'")
    
    pos = []
    words = []
    data = None
    
    for i in range(0,len(phrases)):
        if(phrases[i] not in info):
            wordset = phrases[i].strip().split(" ")
            for w in wordset:
                words.append(w)
                try:
                    pos.append(wn.synsets(w)[0].pos())
                except IndexError:
                    pos.append("-")
                    pass
            
            if('v' in pos):
                if(pos.count("v") > 1):
                    data = phrases[i-1]
                elif(pos.count("v") == 1):
                    data = phrases[i+1]
            
            words.clear()
            pos.clear()
    
    if(data == None):
        data = "Empty"
    
    return data

def returnData():
    return Data

def returnElement():
    return Element
     
def findOutDataAndEntity(sentence):
    print("*************************************** Separating Data and Entity **********************************")
    print("findOutDataAndEntity .......................... ")
    info = []
    info = re.findall("'(.*?)'",sentence)
    
    phrases = sentence.split("'")
    verbFlags = checkFirstSentenceContainstVerb(phrases)
    
    global Data
    global Element
    
    Data = None
    Element = None
    
    if(len(verbFlags) != 0):
        print("checkFirstSentenceContainstVerb .......................... ")
        if('v' in verbFlags):
            Data = info[0]
            Element = info[1]
    
    if(Data == None or Element == None):
        print("checkPOStag ..........................")
        Data = checkPOStag(sentence,info)
        
        if(Data != "Empty"):
            if(Data == info[0]):
                Element = info[1]
            else:
                Element = info[0]
        else:
            Element = "Empty"
            print("Couldn't Separate Data and Entity")
    
    final= {}
    final["data"] = Data
    final["element"] = Element
    print("*************************************** Separated Data and Entity **********************************")
    
    return final
    