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
from pathlib import Path
from selenium import webdriver
import allinone
import MoveToCommonRepo

driver = None
home = str(Path.home())
df = pd.read_excel(r"TestCases.xlsx", sheet_name= "Driver")
wb = xlrd.open_workbook(r"TestCases.xlsx") 
sheet = wb.sheet_by_name("Driver")
headers = sheet.row_values(0)
wb.release_resources()
del wb

for header in headers:
    if('EndToEndExecutionFlag[Y]' in header):
        print('************************* Starting End To End Execution *************************')
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
        allinone.allione(driver)
        writer.close()
    elif('RegressionExecutionFlag[Y]' in header):
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
                writer = pd.ExcelWriter(r"Regression.xlsx", engine='xlsxwriter')
                data.to_excel(writer, sheet_name= "RunTest")
                writer.save()   
                allinone.allione(driver)
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
