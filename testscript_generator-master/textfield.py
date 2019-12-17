from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class Textfield:
    
    def action(self,sentence,driver,dic):
       
        driver.implicitly_wait(1)
        
        array = sentence.split("'")
        flag = 0 ;
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//input[contains(@text,'"+array[3]+"')]"
                inputbox = driver.find_element_by_xpath(temp)
                print('this is by contains @text')
        except NoSuchElementException :
            flag =0
            pass
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//input[@title = '"+array[3]+"']"
                inputbox = driver.find_element_by_xpath(temp)
                print('this is by //input_title')
        except NoSuchElementException :
            flag =0
            pass
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//input[@id = '"+array[3]+"']"
                inputbox = driver.find_element_by_xpath(temp)
                print('this is by //input_@id')
        except NoSuchElementException :
            flag =0
            pass
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//input[contains(@name,'"+array[3]+"')]"
                inputbox = driver.find_element_by_xpath(temp)
                print('this is by contains @name')
        except NoSuchElementException :
            flag =0
            pass
        
        try:
            if(flag==0):
               temp = "//*[contains(@value,'"+array[3]+"')]"
               elem = driver.find_element_by_xpath(temp)
               flag=1
               print(temp)
               print('this is contains @value')
        except NoSuchElementException:
            flag=0
            pass            
     
        
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//input[contains(@name,'"+array[3]+"')]"
                inputbox = driver.find_element_by_link_text(array[3])
                print('this is by link text')
        except NoSuchElementException :
            flag =0
            pass
        
        try :
            if(flag == 0):
                flag = 1
                temp = "//*[contains(text(),'"+array[3]+"')]//..//input"
                inputbox = driver.find_element_by_xpath(temp)
                print('this is by contains placeholder')
        except NoSuchElementException :
            flag =0
            pass    
        
        
        validFlag = 0
        
        if(flag==0):
            if array[3] in dic.keys():
               try:
                    temp = dic[array[3]]
                    flag=1
                    inputbox = driver.find_element_by_xpath(temp)
                    print('element found in dictionary')
               except NoSuchElementException:
                    flag=0
                    pass
        
        if(flag == 1):
            inputbox.clear()
            inputbox.send_keys(array[1])
            
            try:
                if(inputbox.is_displayed()):
                    print("pass")
                    validFlag = 1
            except:
                print("fail")
        else:
            print('element not found')    
        
        if(flag==1):
            if not array[3] in dic.keys():
                dic[array[3]] = temp
        
        return flag and validFlag
        
        