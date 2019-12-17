from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd



class Dropdown:
    
    def action(self,sentence,driver,dic):
        
        driver.implicitly_wait(1)
       
        array = sentence.split("'")
        flag = 0
        
        temp = ""
        
        try:
            if(flag==0):
                flag=1
                temp = "//*[text()='"+ array[1]+"']/.."
                elem = driver.find_element_by_xpath(temp)
                print('this is by super')
        except NoSuchElementException:
                flag=0
                pass
        
        try :
            if(flag==0):
                flag =1 
                temp = "//*[@title = '"+array[3]+"']"
                elem = driver.find_element_by_xpath(temp)
                print('this is by @title')
        except NoSuchElementException:
                flag=0
                pass
         
        
        try :
            if(flag==0):
                flag =1 
                temp = "//*[text()  = '"+array[3]+"']"
                elem = driver.find_element_by_xpath(temp)
                print('this is by text')
        except NoSuchElementException:
                flag=0
                pass
        
        if(flag==0):
            if array[3] in dic.keys():
               try:
                    temp = dic[array[3]]
                    flag=1
                    elem = driver.find_element_by_xpath(temp)
                    print('element found in dictionary')
               except NoSuchElementException:
                    flag=0
                    pass
            
        
        if(flag == 1):
            dropdown = Select(elem)
            dropdown.select_by_visible_text(array[1])
        else:
            print('elements not found')
            return flag
        
        windowhandle = driver.window_handles
        if(len(windowhandle)>1):
            switchwindow = driver.window_handles[-1]
            driver.switch_to_window(switchwindow)
               
        validFlag = 0
        
        if(elem.is_enabled()):
            print("Pass")
            validFlag =1 
        
        if(flag==1):
            if not array[3] in dic.keys():
                dic[array[3]] = temp 

            
        return flag and validFlag 