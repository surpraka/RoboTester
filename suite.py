# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:20:14 2019

@author: surpraka
"""
import os

regressionLoc = r'C:\Users\surpraka\Desktop\RoboTester'
suiteDict = {"Regression1":"Yes",
             "Regression2":"Yes"}

for regression,flag in suiteDict.items():
    if(flag == 'Yes'):
            print("Executing Regression : "+regression)
            os.system('python '+regressionLoc+'\\'+regression+".py")