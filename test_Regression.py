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
from selenium import webdriver
import allinone
import time
import datetime
import pytest


# ================================================================================================
# ==================== Reading Testcases and Configurations ======================================
# ================================================================================================
driver = None
df = pd.read_excel(r"TestCases.xlsx", sheet_name= "Driver")
scenarios = df['Scenario'].tolist()
regressionFlags =  df['RegressionExecutionFlag'].tolist()
BrowserOptions = df['Browser'].tolist()
OSoptions = df['OS'].tolist()
indexes = []
for i in range(0,len(regressionFlags)):
                if(regressionFlags[i] == ('Y')):
                    indexes.append(i)

# ================================================================================================
# ==================== Regression Execution Function  ============================================
# ================================================================================================

print('*************************************  Starting Regression Execution *********************************')
@pytest.mark.parametrize('scenarioIndex',indexes)
def test_RegressionTestCase(scenarioIndex):
    #Report Name
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    reportName = 'extent_report/HtmlReport'+str(st).replace(":", "").replace("-", "").replace(" ", "")
    
    #Driver
    browser = BrowserOptions[scenarioIndex]
    OS = OSoptions[scenarioIndex]
    driver = initEnv(browser, OS)
    
    
    data = pd.read_excel(r"TestCases.xlsx", sheet_name = scenarios[scenarioIndex])
    allinone.allione(driver,data,reportName+'-'+scenarios[scenarioIndex]+'.html',scenarios[scenarioIndex])
print("****************************** Total Number Of Test Cases to execute :"+str(len(indexes))+" ******************************")
print("Regression has ended")

# ================================================================================================
# ==================== Config Browser and Operating System  ======================================
# ================================================================================================

def initEnv(browser,OS):
    global driver
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
    return driver