"""
/**********************************************************************
* RoboTester Version 1.0
* PUBLICIS SAPIENT PROPRIETARY/CONFIDENTIALs
* Use is subject to Organization terms
* @author Varun Sharma,Ashok Yadav & Suraj Prakash
* @since version 1.0
************************************************************************/
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

driver = None

def setUpDriver():
    global driver
    
    # Reading Environment Configuration
    browserFilePath = "Environment/Config.txt"
    f = open(browserFilePath,"r");
    for x in f:
        if('Operating System' in x):
            OsType = x.split(":")[1].split("#")[0].strip()
        elif('Browser' in x):
            browserType = x.split(":")[1].split("#")[0].strip()
        
    if(OsType == 'Windows'):
        print("For "+ OsType +" Operating System , Intializing "+browserType+" browser "+ ".......")    
        if(browserType == "Chrome"):
            options = Options()
            driver = webdriver.Chrome(chrome_options=options, executable_path="Environment\Windows\chromedriver.exe", )
        elif(browserType == "Firefox"):
            driver = webdriver.Firefox(executable_path='Environment\Windows\geckodriver.exe')
        elif(browserType == "IE" or browserType == "Interent Explorer"):
            driver =  webdriver.Ie(executable_path='Environment\Windows\IEDriverServer.exe')

    elif(OsType == 'Linux'):
        print("For "+ OsType +" Operating System , Intializing "+browserType+" browser "+ ".......")    
        if(browserType == "Chrome"):
            driver = webdriver.Chrome(chrome_options=options, executable_path="Environment/Linux/schromedriver", )
        elif(browserType == "Firefox"):
            driver = webdriver.Firefox(executable_path='Environment\Linux\geckodriver')
        elif(browserType == "IE" or browserType == "Interent Explorer"):
            driver =  webdriver.Ie(executable_path='Environment\Linux\IEDriverServer')
        
    elif(OsType == 'Mac'):
        print("For "+ OsType +" Operating System , Intializing "+browserType+" browser "+ ".......")    
        if(browserType == "Chrome"):
            driver = webdriver.Chrome(chrome_options=options, executable_path="Environment/Mac/chromedriver", )
        elif(browserType == "Firefox"):
            driver = webdriver.Firefox(executable_path='Environment\Mac\geckodriver')
        elif(browserType == "IE" or browserType == "Interent Explorer"):
            driver =  webdriver.Ie(executable_path='Environment\Mac\IEDriverServer')
    
    return driver
