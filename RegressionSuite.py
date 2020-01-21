# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:20:14 2019

@author: surpraka
"""
import os
import pandas as pd
import xlrd
from pathlib import Path

home = str(Path.home())

df = pd.read_excel(r"TestCases.xlsx", sheet_name= "Driver")

wb = xlrd.open_workbook(r"TestCases.xlsx") 
sheet = wb.sheet_by_name("Driver")
headers = sheet.row_values(0)
wb.release_resources()
del wb
print(headers)

for header in headers:
    if('EndToEndExecutionFlag[Y]' in header):
        print('Starting End To End Execution')
        scenarios = df['Scenario'].tolist()
        regressionFlags =  df['EndToEndExecutionFlag[Y]'].tolist()

        df = []
        for i in range(0,len(regressionFlags)):
            if(regressionFlags[i] == ('Y')):
                data = pd.read_excel(r"TestCases.xlsx", sheet_name = scenarios[i])
                df.append(data)

        df = pd.concat(df)
        print(df)

        writer = pd.ExcelWriter(r"Regression.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name= "RunTest")
        writer.save()   
        os.system('python allinone.py')
        writer.close()
    if('RegressionExecutionFlag[Y]' in header):
        print('Starting Individual Execution')
        scenarios = df['Scenario'].tolist()
        regressionFlags =  df['RegressionExecutionFlag[Y]'].tolist()
        testCases = 0
        
        for i in range(0,len(regressionFlags)):
            if(regressionFlags[i] == ('Y')):
                testCases = testCases +1;
        
        print("Total Number Of Test Cases :"+str(testCases))
        for i in range(0,len(regressionFlags)):
            if(regressionFlags[i] == ('Y')):
                data = pd.read_excel(r"TestCases.xlsx", sheet_name = scenarios[i])
                writer = pd.ExcelWriter(r"Regression.xlsx", engine='xlsxwriter')
                data.to_excel(writer, sheet_name= "RunTest")
                writer.save()   
                os.system('python allinone.py')
                writer.close()

        
    