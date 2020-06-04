# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:13:12 2020

@author: surpraka
"""

import pandas as pd
from selenium import webdriver
import allinone
import MoveToCommonRepo
import sys

regressionFile = "Regression/Regression2.xlsx"

def Regg2(sheetName,reportName):
    print("******** For "+ 'Windows2' +" Operating System , Intializing "+'Chrome'+" ***********")
    print("For Scenario : "+ sheetName)
    driver = webdriver.Chrome(executable_path="Environment\Windows\chromedriver.exe", )
    data = pd.read_excel(r"TestCases.xlsx", sheetName)
    writer = pd.ExcelWriter(regressionFile, engine='xlsxwriter')
    data.to_excel(writer, sheet_name= sheetName)
    writer.save()
    reportName = reportName+'-'+sheetName+'.html'
    allinone.allione(driver,regressionFile,reportName,sheetName)
    writer.close()
    
    print("")
    print("************************ Moving Duplicate Elements to Common Repo *************************")
    MoveToCommonRepo.fetchCommonXpathsFromObjectRepo()
    print("************************ Moved Duplicate Elements to Common Repo  *************************")
    print("")

if __name__ == '__main__':
    Regg2(sys.argv[1],sys.argv[2])