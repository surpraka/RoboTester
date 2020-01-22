# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 10:38:16 2020

@author: surpraka
"""

from selenium import webdriver

browserFilePath = r"C:\Users\surpraka\Desktop\RoboTester\DriverConfig\BrowserType.txt"
f = open(browserFilePath,"r");

for x in f:
    if('Y' in x or 'y' in x or 'Yes' in x or 'YES' in x):
        print(x)
        browserType = x.split(":")[0].strip()
        break

print("Intializing "+browserType+" .......")    

if(browserType == "Chrome"):
    driver = webdriver.Chrome(executable_path='DriverConfig\chromedriver.exe')
elif(browserType == "Firefox"):
    driver = webdriver.Firefox(executable_path='DriverConfig\geckodriver.exe')
elif(browserType == "IE" or browserType == "Interent Explorer"):
    driver =  webdriver.Ie(executable_path='DriverConfig\IEDriverServer.exe')

driver.maximize_window()
