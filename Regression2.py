# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 19:17:35 2019

@author: surpraka
"""
import os
import pandas as pd

TestCasesloc = r'C:\Users\surpraka\Desktop\RoboTester\testcases.xlsx'
Regressionloc = r'C:\Users\surpraka\Desktop\RoboTester\Regression.xlsx'
runTestCase = "RunTest"

TestCasesDict = {'MFS1':'Yes',
                 'MFS2':'No'}
df = []

for sheetName,flag in TestCasesDict.items():
    if(flag == ('Yes')):
        data = pd.read_excel(TestCasesloc, sheet_name = sheetName)
        df.append(data)

df = pd.concat(df) 
print(df)

writer = pd.ExcelWriter(Regressionloc, engine='xlsxwriter')
df.to_excel(writer, sheet_name= runTestCase)
writer.save()   

os.system('python C:\\Users\\surpraka\\Desktop\\RoboTester\\allinone.py')