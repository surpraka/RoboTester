# -*- coding: utf-8 -*-
"""
Created on Fri May 15 20:07:45 2020

@author: surpraka
"""

regressionFile = "Regression/Regression.xlsx"
regressionFile1 = "Regression/Regression1.xlsx"

import os

def threeThreads(threadCount,sheetNames,reportName):
    size = len(sheetNames)
    count = 0
    
    if(size>=3):
            #odd Scenario
            print("Odd Scenarios "+ str(size))
            if(size%2!=0):
                while(count<=(size-2)):
                    sc1 = sheetNames[count];
                    sc2 = sheetNames[count+1];
                    sc3 = sheetNames[count+2]
                    print("Parallel Execution of scenarios :"+sc1+" , "+sc2+" and "+sc3)
                    os.system('python Parallel/parallel3Process.py '+sc1+' '+sc2+' '+sc3+' '+reportName)
                    count = count+3
            else:
                #Even Scenario
                print("Even Scenarios "+ str(size))
                
    else:
        print("Please set proper thread count")