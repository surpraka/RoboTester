"""
/**********************************************************************
* RoboTester Version 1.0
* PUBLICIS SAPIENT PROPRIETARY/CONFIDENTIAL
* Use is subject to Organization terms
* @author Varun Sharma,Ashok Yadav & Suraj Prakash
* @since version 1.0
************************************************************************/
"""

import csv
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os.path

class FindElement:
    
    def action(self,sentence,driver):
        
        driver.implicitly_wait(2)
        array = sentence.split("'")
        flag = 0 ;
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//input[@id = '"+array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                print('this is by //input_@id')
        except NoSuchElementException :
            flag =0
            pass

        try:
            if(flag==0):
               elem = driver.find_element_by_link_text(array[1])
               flag=1
               print('this is by link text()')
        except NoSuchElementException:
           flag =0
           pass
       
        try :
            if(flag == 0):
                flag = 1
                temp = "//input[contains(@text,'"+array[1]+"')]"
                elem = driver.find_element_by_xpath(temp)
                print('this is by contains @text')
        except NoSuchElementException :
            flag =0
            pass

        try :
            if(flag == 0):
                flag = 1
                temp = "//input[@title = '"+array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                print('this is by //input_title')
        except NoSuchElementException :
            flag =0
            pass

        try :
            if(flag == 0):
                flag = 1
                temp = "//input[contains(@name,'"+array[1]+"')]"
                elem = driver.find_element_by_xpath(temp)
                print('this is by contains @name')
        except NoSuchElementException :
            flag =0
            pass
        
        try :
            if(flag==0):
                temp ="//button[@class='"+ array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                flag=1
                print('this is by //button_@class')
        except NoSuchElementException :
            flag =0
            pass

        try :
            if(flag==0):
                temp ="//button[text()='"+ array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                flag=1
                print('this is by //button_text()')

        except NoSuchElementException :
            flag =0
            pass

        try :
            if(flag==0):
                temp ="//*[text()='"+ array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                flag=1
                print('this is by text')

        except NoSuchElementException :
            flag =0
            pass

        try:
            if(flag==0):
               temp = "//*[contains(@value,'"+array[1]+"')]"
               elem = driver.find_element_by_xpath(temp)
               flag=1
               print(temp)
               print('this is by contains @value')
        except NoSuchElementException:
            flag=0
            pass
        
        try :
            if(flag==0):
                temp= "//*[@class='"+array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                flag=1
                print('this is by @class')

        except NoSuchElementException :
            flag =0
            pass
        
        try :
            if(flag==0):
                temp= "//*[contains(@class,'"+array[1]+"')]"
                elem = driver.find_element_by_xpath(temp)
                flag=1
                print('this is by @class')

        except NoSuchElementException :
            flag =0
            pass
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//*[contains(text(),'"+array[1]+"')]"
                elem = driver.find_element_by_xpath(temp)
                print('this is by contains placeholder')
        except NoSuchElementException :
            flag =0
            pass
        
        dic = {}
        driver.implicitly_wait(1)
        name = driver.title
        name = re.sub(r'\W','',str(name))
        #name = name[-15:]
        filepath = "ObjectMap/"+name+".txt"

        if(os.path.exists(filepath)):
            print("file exists")
            pass
        else:
            print("making file")
            f= open(filepath,"w+")
            f.close()
            
# =============================================================================
# read the elements and xpaths for current page from object map to dictionary
# =============================================================================
        with open(filepath ) as csv_file :

            csv_reader = csv.reader(csv_file,delimiter=';')
            line_count=0
            for row in csv_reader:
                if line_count==0:
                    line_count+=1
                else:
                    dic[row[1]] = row[2]

   
#if element not found yet then check in dictionary
        if(flag==0):
            print('searching in dictionary')
            if array[1] in dic.keys():
               try:
                    temp = dic[array[1]]
                    flag=1
                    elem = driver.find_element_by_xpath(temp)
                    print('element found in dictionary')
               except NoSuchElementException:
                    flag=0
                    pass
        print(elem)
        
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of(elem))

        return elem
