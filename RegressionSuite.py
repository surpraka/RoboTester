# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:21:17 2020

@author: surpraka
"""

"""
/**********************************************************************
* RoboTester Version 1.0
* PUBLICIS SAPIENT PROPRIETARY/CONFIDENTIALs
* Use is subject to Organization terms
* @author Varun Sharma,Ashok Yadav & Suraj Prakash
* @since version 1.0
************************************************************************/
"""

import pandas as pd
import xlrd
from selenium import webdriver
import allinone
import MoveToCommonRepo
import time
import datetime
import twoThreads
import threeThread

driver = None
df = pd.read_excel(r"TestCases.xlsx", sheet_name= "Driver")
wb = xlrd.open_workbook(r"TestCases.xlsx") 
sheet = wb.sheet_by_name("Driver")
headers = sheet.row_values(0)
wb.release_resources()
del wb

regressionFile = "Regression/Regression.xlsx"
regressionFile1 = "Regression/Regression1.xlsx"

for header in headers:
    if('RegressionExecutionFlag[Y]' in header):
        print('*************************************  Starting Individual Execution *********************************')
        scenarios = df['Scenario'].tolist()
        regressionFlags =  df['RegressionExecutionFlag[Y]'].tolist()
        BrowserOptions = df['Browser'].tolist()
        OSoptions = df['OS'].tolist()
        testCases = 0
        
        for i in range(0,len(regressionFlags)):
            if(regressionFlags[i] == ('Y')):
                testCases = testCases +1;
            
        print("****************************** Total Number Of Test Cases to execute :"+str(testCases)+" ******************************")
        print(" ")
        
        testCasesCount = 1
        
        threadCount = df['ThreadCount'].tolist()[0];
        print("Thread Count is : " + str(threadCount))
        sheetNames = []
        
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        reportName = 'extent_report/HtmlReport'+str(st).replace(":", "").replace("-", "").replace(" ", "")
                    
        # Parallel Execution
        if(threadCount > 1):

            for i in range(0,len(regressionFlags)):
                if(regressionFlags[i] == ('Y')):
                    sheetNames.append(scenarios[i])
            
            size = len(sheetNames)
            count = 0
            
            print("Number of scenarios : "+str(size)+" and are :")
            print(sheetNames)
            
            if(threadCount==2):
                twoThreads.twoThreads(threadCount, sheetNames, reportName)
            if(threadCount == 3):
                threeThread.threeThreads(threadCount, sheetNames, reportName)
        #Serial Execution
        else:
            print("Serial Execution : ")
            for i in range(0,len(regressionFlags)):
                if(regressionFlags[i] == ('Y')):
                    browser = BrowserOptions[i]
                    OS = OSoptions[i]
                    
                    print (" ")
                    print("*********************************************************************")
                    print("**************************** TestCase["+str(testCasesCount)+"] ****************************")
                    print("*********************************************************************")
                    print (" ")
                    
                    if(browser == 'Chrome' or browser == 'Firefox' or browser == 'IE'):
                        if(browser == 'Chrome'):
                            if(OS == 'Windows'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Chrome(executable_path="Environment\Windows\chromedriver.exe", )
                            elif(OS == 'Mac'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Chrome(executable_path="Environment/Mac/chromedriver")
                            elif(OS == 'Linux'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Chrome(executable_path="Environment\Linux\chromedriver")
                        if(browser == 'IE'):
                            if(OS == 'Windows'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Ie(executable_path="Environment\Windows\IEDriverServer.exe")
                            elif(OS == 'Mac'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Ie(executable_path="Environment/Mac/IEDriverServer")
                            elif(OS == 'Linux'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Ie(executable_path="Environment\Linux\IEDriverServer")
                        if(browser == 'Firefox'):
                            if(OS == 'Windows'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Ie(executable_path="Environment\Windows\geckodriver.exe")
                            elif(OS == 'Mac'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Ie(executable_path="Environment/Mac/geckodriver")
                            elif(OS == 'Linux'):
                                print (" ")
                                print("*****************  Environment Set up through Excel File *****************")
                                print("******** For "+OS+" Operating System , Intializing "+browser+" ***********")
                                print (" ")
                                driver = webdriver.Ie(executable_path="Environment\Linux\geckodriver")
                    data = pd.read_excel(r"TestCases.xlsx", sheet_name = scenarios[i])
                    writer = pd.ExcelWriter(regressionFile, engine='xlsxwriter')
                    data.to_excel(writer, sheet_name= scenarios[i])
                    writer.save()   
                    allinone.allione(driver,regressionFile,reportName+'-'+scenarios[i]+'.html',scenarios[i])
                    writer.close()
                    
                    print("")
                    print("************************ Moving Duplicate Elements to Common Repo *************************")
                    MoveToCommonRepo.fetchCommonXpathsFromObjectRepo()
                    print("************************ Moved Duplicate Elements to Common Repo  *************************")
                    print("")
                    
                    print (" ")
                    print("*********************************************************************")
                    print("************************** TestCase["+ str(testCasesCount)+"] has ended **************************")
                    print("*********************************************************************")
                    print (" ")
                    testCasesCount = testCasesCount+1
                    
print("Regression has ended")