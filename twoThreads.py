# -*- coding: utf-8 -*-
"""
Created on Fri May 15 19:53:06 2020

@author: surpraka
"""

import pandas as pd
from selenium import webdriver
import allinone
import MoveToCommonRepo
import os                                                                   


regressionFile = "Regression/Regression.xlsx"
regressionFile1 = "Regression/Regression1.xlsx"


def twoThreads(threadCount,sheetNames,reportName):
    size = len(sheetNames)
    count = 0

    if(size>=2):
        # Even Scenarios
        if(size%2 == 0):
            print("Even Scenarios")
            while(count<=(size-1)):
                sc1 = sheetNames[count];
                sc2 = sheetNames[count+1];
                print("Parallel Execution of scenarios :"+sc1+" and "+sc2)
                os.system('python parallelProcess.py '+sc1+' '+sc2+' '+reportName)
                count = count+2
        #Odd scenarios
        else:
            print("Odd Scenarios "+ str(size))
            modifiedSize = size-1
            while(count<=(modifiedSize-1)):
                sc1 = sheetNames[count];
                sc2 = sheetNames[count+1];
                print("Parallel Execution of scenarios :"+sc1+" and "+sc2)
                os.system('python parallelProcess.py '+sc1+' '+sc2+' '+reportName)
                count = count+2
            print("Parallel Execution of scenario : "+sheetNames[size-1])
            driver = webdriver.Chrome(executable_path="Environment\Windows\chromedriver.exe", )
            data = pd.read_excel(r"TestCases.xlsx", sheetNames[size-1])
            writer = pd.ExcelWriter(regressionFile1, engine='xlsxwriter')
            data.to_excel(writer, sheetNames[size-1])
            writer.save()   
            allinone.allione(driver,regressionFile1,reportName+'-'+sheetNames[size-1]+'.html',sheetNames[size-1])
            writer.close()
            print("")
            print("************************ Moving Duplicate Elements to Common Repo *************************")
            MoveToCommonRepo.fetchCommonXpathsFromObjectRepo()
            print("************************ Moved Duplicate Elements to Common Repo  *************************")
            print("")
    else:
        print("Please set proper thread Count")
