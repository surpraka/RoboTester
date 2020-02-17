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
from py4j.java_gateway import JavaGateway, GatewayParameters
import re
from nltk.corpus import stopwords
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json

import findElement
import DriverSetUp
import Dictionary
import SeparateDataAndEntity

def allione(driver):
    # =============================================================================
    # Read the testcases from excel sheet and load them into a list of strings
    # =============================================================================
    df = pd.read_excel(r"Regression.xlsx", sheet_name= "RunTest") # can index sheet by name 
    mylist = df['Actions'].tolist()
    
    # =============================================================================
    # Read the scenario names as well for extent report beautification
    # =============================================================================
    sc = df['Scenario'].to_list()
    scnames = [ a for a in sc if isinstance(a,str) ]
    print(scnames)
    
    
    # =============================================================================
    # Load the training data for the classifier and store the train data in x and
    # target(labels) values in y
    # =============================================================================
    reviews = load_files('Functionalties')
    x,y = reviews.data , reviews.target
    
    # =============================================================================
    # data pre-processing to remove all the insignificant words from each string
    # =============================================================================
    corpus = []
    for i in range(0, len(x)):
        review = re.sub(r'\W',' ',str(x[i]))
        review = review.lower()
        review = re.sub(r'\s+[a-z]\s+',' ',review)
        review = re.sub(r'^[a-z]\s+','', review)
        review = re.sub(r'\s+', ' ', review)
    
        corpus.append(review)
    
    
    # =============================================================================
    # Initialize a tfidf vectorizer which converts a string into array of floating number 
    # =============================================================================
    vectorizer = TfidfVectorizer(max_features=100, min_df=3,max_df=0.8,stop_words=stopwords.words('english'))
    
    # =============================================================================
    # split the sample data into training set and test set
    # =============================================================================
    X_train, X_test, Y_train, Y_test = train_test_split(corpus, y, test_size=0.3, random_state=42)
    
    # converts to array
    X_train = vectorizer.fit_transform(X_train).toarray()
    X_test = vectorizer.transform(X_test).toarray()
    
    #initialize and train the model
    classifier = LogisticRegression(random_state=42, solver='newton-cg', max_iter=1000, multi_class='multinomial', n_jobs=-1)
    classifier.fit(X_train, Y_train)
    
    class Get:
    
        def browse(self,url,driver):
    
            #array = url.split("'")
            array = re.findall("'(.*?)'",url)
            print("http://"+array[0])
            driver.get("http://"+array[0])
            driver.implicitly_wait(1)
            return 1 
        
    class Dropdown:
    
        def action(self,sentence,driver):
    
            driver.implicitly_wait(1)
            #array = sentence.split("'")
            array = SeparateDataAndEntity.findOutDataAndEntity(sentence)
            elementName = array["element"]
            dropdownOption = array["data"]
            
            flag = 0
    
            temp = ""
    # =============================================================================
    # try to find the element using different strategies
    # and status flag keeps track of whether the element has been found
    # =============================================================================
            try:
                if(flag==0):
                    flag =1
                    temp = "//select[contains(@class,'"+elementName+"')]"
                    elem = driver.find_element_by_xpath(temp)
                    print("this is by @class for "+elementName)
            except NoSuchElementException:
                    flag =0
                    pass
            
            try:
                if(flag==0):
                    flag =1
                    temp = "//select[contains(@id,'"+elementName+"')]"
                    elem = driver.find_element_by_xpath(temp)
                    print("this is by @id for "+elementName)
            except NoSuchElementException:
                    flag =0
                    pass
            
            try:
                if(flag==0):
                    flag =1
                    temp = "//select[@id='"+elementName+"']"
                    elem = driver.find_element_by_xpath(temp)
                    print("this is by @id for "+elementName)
            except NoSuchElementException:
                    flag =0
                    pass
            
            try:
                if(flag==0):
                    flag =1
                    temp = "//select[@class='"+elementName+"']"
                    elem = driver.find_element_by_xpath(temp)
                    print("this is by @class for "+elementName)
            except NoSuchElementException:
                    flag =0
                    pass
            
            try :
                if(flag==0):
                    flag =1
                    temp = "//*[@title = '"+elementName+"']"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by @title')
            except NoSuchElementException:
                    flag=0
                    pass
    
    
            try :
                if(flag==0):
                    flag =1
                    temp = "//*[text()  = '"+elementName+"']"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by text')
            except NoSuchElementException:
                    flag=0
                    pass
    
            # Read Xpaths from object dictionary   
            driver.implicitly_wait(1)
            name = driver.title
            name = re.sub(r'\W','',str(name))
            filepath = "ObjectMap/"+name+".txt"  
            commonDic = {}
            pageDic = {}
            
            commonDic = Dictionary.readCommonXpathsFromObjectRepo()
            pageDic = Dictionary.readXpathsFromObjectRepo(name)
            
            #Common Elements
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(commonDic) == 0):
                    print("Common Dictionary Is Empty")
                else:
                    if elementName in commonDic.keys():
                       try:
                            temp = commonDic[elementName]
                            flag=1
                            elem = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in Common Dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
          
            #Page Specific Elements              
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(pageDic) == 0):
                    print(name+' Page Dictionary is Empty')
                else:
                    if elementName in pageDic.keys():
                       try:
                            temp = pageDic[elementName]
                            flag=1
                            elem = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in Page Specific dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
             
            Dictionary.updateDictionary(flag,elementName,pageDic,temp,filepath)  
            
            #perform action
            if(flag == 1):
                elem.click()
                dropdown = Select(elem)
                try:
                    option = dropdown.select_by_visible_text(dropdownOption)
                except NoSuchElementException:
                    option = False
                    pass
            
            if(option == False):
                dropdown = Select(elem)
                try:
                    option = dropdown.select_by_value(dropdownOption)
                except NoSuchElementException:
                    option = False
                    pass
            else:
                print('Element'+ elementName +' not found')
                return flag
            
            #if new window opens switch windows
            windowhandle = driver.window_handles
            if(len(windowhandle)>1):
                switchwindow = driver.window_handles[-1]
                driver.switch_to_window(switchwindow)
    
            return flag
    
    class Button:
    
        def action(self,sentence,driver):
    
            #array = sentence.split("'")
            array = re.findall("'(.*?)'",sentence)
            flag = 0
            driver.implicitly_wait(1)
            temp=""
            elementName =  array[0]
    # =============================================================================
    # try to find the element using different strategies
    # and status flag keeps track of whether the element has been found
    # =============================================================================
            try :
                if(flag==0):
                    temp ="//button[contains(@id,'"+ elementName +"')]"
                    elem = driver.find_element_by_xpath(temp)
                    flag=1
                    print('Found Xpath by --  //button_@id')
            except NoSuchElementException :
                flag =0
                pass
            
            try :
                if(flag==0):
                    temp ="//button[@class='"+ elementName +"']"
                    elem = driver.find_element_by_xpath(temp)
                    flag=1
                    print('Found Xpath by --  //button_@class')
            except NoSuchElementException :
                flag =0
                pass
            
            try :
                if(flag==0):
                    temp ="//button[text()='"+ elementName +"']"
                    elem = driver.find_element_by_xpath(temp)
                    flag=1
                    print('Found Xpath by --  //button_text()')
    
            except NoSuchElementException :
                flag =0
                pass
    
            try:
                if(flag==0):
                   elem = driver.find_element_by_link_text(elementName)
                   flag=1
                   print('Found Xpath by --  link text()')
    
            except NoSuchElementException:
    
               flag =0
               pass
    
            try :
                if(flag==0):
                    temp= "//*[@class='"+elementName+"']"
                    elem = driver.find_element_by_xpath(temp)
                    flag=1
                    print('Found Xpath by -- @class')
    
            except NoSuchElementException :
                flag =0
                pass
            
            try:
                if(flag==0):
                   temp = "//*[contains(@value,'"+elementName+"')]"
                   elem = driver.find_element_by_xpath(temp)
                   flag=1
                   print(temp)
                   print('Found Xpath by -- @value')
            except NoSuchElementException:
                flag=0
                pass
            
            try :
                if(flag==0):
                    temp ="//*[text()='"+ elementName +"']"
                    elem = driver.find_element_by_xpath(temp)
                    flag=1
                    print('Found Xpath by -- text')
    
            except NoSuchElementException :
                flag =0
                pass
    
            validFlag = 0
            
            
            # Read Xpaths from object dictionary   
            driver.implicitly_wait(1)
            name = driver.title
            name = re.sub(r'\W','',str(name))
            filepath = "ObjectMap/"+name+".txt"  
            
            commonDic = {}
            pageDic = {}
            commonDic = Dictionary.readCommonXpathsFromObjectRepo()
            pageDic = Dictionary.readXpathsFromObjectRepo(name)
            
            #Common Elements
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(commonDic) == 0):
                    print("Common Dictionary Is Empty")
                else:
                    if elementName in commonDic.keys():
                       try:
                            temp = commonDic[elementName]
                            flag=1
                            elem = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in Common Dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
          
            #Page Specific Elements              
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(pageDic) == 0):
                    print(name+' Page Dictionary is Empty')
                else:
                    if elementName in pageDic.keys():
                       try:
                            temp = pageDic[elementName]
                            flag=1
                            elem = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in Page specific Dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
             
            Dictionary.updateDictionary(flag,elementName,pageDic,temp,filepath)  
            
            #driver.implicitly_wait(2)
            if(flag==1):
                 try:
                    if(elem.is_displayed()):
                        print(elementName+' is displayed')
                        validFlag = 1
                 except:
                    print(elementName+' element is not Visible in View Port')
                    print("Solution :  Try using scroll")
                    pass
            else:
                print(elementName+ 'element not found')
            
            #perform action
            if(flag==1):
                try:
                    elem.click()
                    print("click")
                except ElementNotInteractableException:
                    Hover = ActionChains(driver).move_to_element(elem).click().perform()
                    print("NotInteractable Hover")
                except ElementClickInterceptedException:
                    Hover = ActionChains(driver).move_to_element(elem).click().perform()
                    print("Intercepted hover")
            
            #if new window opens switch windows
            windowhandle = driver.window_handles
            if(len(windowhandle)>1):
                switchwindow = driver.window_handles[-1]
                driver.switch_to_window(switchwindow)
          
            return flag and validFlag
    
    class Hover:
        
        def action(self,sentence,driver):
            
            driver.implicitly_wait(1)        
            #array = sentence.split("'")
            array = re.findall("'(.*?)'",sentence)
            flag = 0 ;
            elementName = array[0]
    # =============================================================================
    # try to find the element using different strategies
    # and status flag keeps track of whether the element has been found
    # =============================================================================
            
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[contains(@text,'"+ elementName +"')]"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by contains Input Tag and @text')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[@title = '"+elementName+"']"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by //input_title')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[@id = '"+elementName+"']"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by //input_@id')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[contains(@name,'"+elementName+"')]"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by contains @name')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    elem = driver.find_element_by_link_text(elementName)
                    print('this is by link text')
            except NoSuchElementException :
                flag =0
                pass
            
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[contains(@text,'"+elementName+"')]"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by contains @text')
            except NoSuchElementException :
                flag =0
                pass
            
            try:
                if(flag==0):
                   temp = "//*[contains(@value,'"+elementName+"')]"
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
                    temp = "//*[contains(text(),'"+elementName+"')]//..//input"
                    elem = driver.find_element_by_xpath(temp)
                    print('this is by contains placeholder')
            except NoSuchElementException :
                flag =0
                pass
    
    
            validFlag = 0
    
            # Read Xpaths from object dictionary   
            driver.implicitly_wait(1)
            name = driver.title
            name = re.sub(r'\W','',str(name))
            filepath = "ObjectMap/"+name+".txt"  
            commonDic = {}
            pageDic = {}
            
            commonDic = Dictionary.readCommonXpathsFromObjectRepo()
            pageDic = Dictionary.readXpathsFromObjectRepo(name)
            
            #Common Elements
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(commonDic) == 0):
                    print("Common Dictionary Is Empty")
                else:
                    if elementName in commonDic.keys():
                       try:
                            temp = commonDic[elementName]
                            flag=1
                            elem = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in Common Dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
          
            #Page Specific Elements              
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(pageDic) == 0):
                    print(name+' Page Dictionary is Empty')
                else:
                    if elementName in pageDic.keys():
                       try:
                            temp = pageDic[elementName]
                            flag=1
                            elem = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in page Specific dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
             
            Dictionary.updateDictionary(flag,elementName,pageDic,temp,filepath)  
            
            #perform action
            if(flag == 1):
                hover = ActionChains(driver).move_to_element(elem)
                hover.perform() 
    
                try:
                    if(elem.is_displayed()):
                        print(elementName + " is visible in View Port")
                        validFlag = 1
                except:
                     print(elementName + " is visible in View Port")
            else:
                print(elementName+' Element not found')
            
            return flag and validFlag
            
    class Textfield:
    
        def action(self,sentence,driver):
    
            driver.implicitly_wait(1)
            
            array = SeparateDataAndEntity.findOutDataAndEntity(sentence)
            elementName = array["element"]
            text_to_enter = array["data"]
            flag = 0 ;
    
    # =============================================================================
    # try to find the element using different strategies
    # and status flag keeps track of whether the element has been found
    # =============================================================================
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[contains(@text,'"+elementName+"')]"
                    inputbox = driver.find_element_by_xpath(temp)
                    print('this is by contains @text')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[@title = '"+elementName+"']"
                    inputbox = driver.find_element_by_xpath(temp)
                    print('this is by //input_title')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[@id = '"+elementName+"']"
                    inputbox = driver.find_element_by_xpath(temp)
                    print('this is by //input_@id')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[contains(@name,'"+elementName+"')]"
                    inputbox = driver.find_element_by_xpath(temp)
                    print('this is by contains @name')
            except NoSuchElementException :
                flag =0
                pass
    
            try :
                if(flag == 0):
                    flag = 1
                    inputbox = driver.find_element_by_link_text(elementName)
                    print('this is by link text')
            except NoSuchElementException :
                flag =0
                pass
            
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//input[contains(@text,'"+elementName+"')]"
                    inputbox = driver.find_element_by_xpath(temp)
                    print('this is by contains @text')
            except NoSuchElementException :
                flag =0
                pass
            
            try:
                if(flag==0):
                   temp = "//*[contains(@value,'"+elementName+"')]"
                   inputbox = driver.find_element_by_xpath(temp)
                   flag=1
                   print(temp)
                   print('this is contains @value')
            except NoSuchElementException:
                flag=0
                pass
            
            try :
                if(flag == 0):
                    flag = 1
                    temp = "//*[contains(text(),'"+elementName+"')]//..//input"
                    inputbox = driver.find_element_by_xpath(temp)
                    print('this is by contains placeholder')
            except NoSuchElementException :
                flag =0
                pass
    
    
            validFlag = 0
    
            
            # Read Xpaths from object dictionary   
            driver.implicitly_wait(1)
            name = driver.title
            name = re.sub(r'\W','',str(name))
            filepath = "ObjectMap/"+name+".txt"  
            commonDic = {}
            pageDic = {}
            
            commonDic = Dictionary.readCommonXpathsFromObjectRepo()
            pageDic = Dictionary.readXpathsFromObjectRepo(name)
            
            #Common Elements
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(commonDic) == 0):
                    print("Common Dictionary Is Empty")
                else:
                    if elementName in commonDic.keys():
                       try:
                            temp = commonDic[elementName]
                            flag=1
                            inputbox = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in Common Dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
          
            #Page Specific Elements              
            #if element not found yet then check in dictionary
            if(flag==0):
                if(len(pageDic) == 0):
                    print(name+' Page Dictionary is Empty')
                else:
                    if elementName in pageDic.keys():
                       try:
                            temp = pageDic[elementName]
                            flag=1
                            inputbox = driver.find_element_by_xpath(temp)
                            print('Element '+elementName+' found in Page Specific dictionary')
                       except NoSuchElementException:
                            flag=0
                            pass
             
            Dictionary.updateDictionary(flag,elementName,pageDic,temp,filepath)  
            
            #perform action
            if(flag == 1):
                inputbox.clear()
                inputbox.send_keys(text_to_enter)
    
                try:
                    if(inputbox.is_displayed()):
                        print(elementName+" is displayed in View Port")
                        validFlag = 1
                except:
                    print(elementName+" is not displayed in View Port")
            else:
                print(elementName+ ' Element not found')
   
            return flag and validFlag
    
    
    # establish connection to java gateway entry point
    gateway = JavaGateway(gateway_parameters=GatewayParameters())
    if(driver == None):
        print(" ********************** Environment Set up through config File **********************")
        driver = DriverSetUp.setUpDriver()
    driver.maximize_window()
    sample = mylist
    
    for sen in sample:
    # =============================================================================
    #     vectorize the testcase and then predict class using classifier
    # =============================================================================
        testcase = [sen]
        testcase = vectorizer.transform(testcase).toarray()
        print(classifier.predict(testcase))
    
        if(classifier.predict(testcase) ==0):
            print('Action is classified as Button')
            button = Button()
            # pass the action to button class 
            status_flag  = button.action(str(sen),driver)
            if(status_flag == 1 ):
                gateway.entry_point.reportPass('testcase :'+sen+' is successful')
            else:
                gateway.entry_point.reportFail('testcase :'+sen+' is fail')
                break
    
    
        if(classifier.predict(testcase) ==6):
            print('Action is classified as DropDown')
            dropdown = Dropdown()
            # pass the action to dropdown class 
            status_flag = dropdown.action(str(sen),driver)
            if(status_flag == 1 ):
                gateway.entry_point.reportPass('testcase :'+sen+' is successful')
            else:
                gateway.entry_point.reportFail('testcase :'+sen+' is fail')
                break
    
        if(classifier.predict(testcase) ==1):
            gateway.entry_point.reportScenario('***** Running TestCase :'+scnames.pop(0)+' *****')
            print('Action is classified as  Hit URL')
            get = Get()
             # pass the action to get class 
            status_flag = get.browse(str(sen),driver)
            if(status_flag == 1 ):
                gateway.entry_point.reportPass('testcase :'+sen+' is successful')
            else:
                gateway.entry_point.reportFail('testcase :'+sen+' is fail')
                break
    
        if(classifier.predict(testcase) ==7):
    
            print('Action is classified as TextField')
            textfield = Textfield()
             # pass the action to textfield class 
            status_flag = textfield.action(str(sen),driver)
            if(status_flag == 1 ):
                gateway.entry_point.reportPass('testcase :'+sen+' is successful')
            else:
                gateway.entry_point.reportFail('testcase :'+sen+' is fail')
                break
    
        if(classifier.predict(testcase) == 4):
            gateway.entry_point.reportPass('***** Running WebService Test*****')
            print('Action is classified as Get Service')
            array = sen.split("'")
    
            URL = array[1]
            PARAMS = array[3]
            if(PARAMS == 'null' or PARAMS == 'no'):
                 r = requests.get(url=URL)
            else:
                 r = requests.get(url = URL, params = PARAMS)
                 
            try:
                data = json.loads(r.content)
                print(data)
                print(r.status_code)
    
                if(r.status_code == 200):
                    gateway.entry_point.reportPass('status code is : 200 OK')
                    if('verify response' in sen or 'Verify response' in sen or 'validate response' in sen):
                        givenValue = array[5]
                        print(givenValue)
                        if(str(data)==givenValue):
                            gateway.entry_point.reportPass('service verified')
                        else:
                            gateway.entry_point.reportFail('response not matching')
                else:
                    gateway.entry_point.reportFail('status code is : '+r.status_code)
            except Exception as e:
                print(" An Exception Occured for "+ URL+" as "+str(e))
                gateway.entry_point.reportFail('status code is : '+r.status_code)
    
    
        if(classifier.predict(testcase) == 3):
            gateway.entry_point.reportPass('***** Running WebService Test*****')
            print('Action is classified as Post Service')
            array = sen.split("'")
    
            URL = array[1]
            PARAMS = array[3]
            if(PARAMS == 'null' or PARAMS == 'no'):
                r = requests.post(url=URL)
            else:
                r = requests.post(url = URL, params = PARAMS)
    
            data = json.loads(r.content)
    
    
            if(r.status_code == 200):
                gateway.entry_point.reportPass('status code is : 200 OK')
            else:
                gateway.entry_point.reportFail('status code is : '+r.status_code)
    
            givenValue = array[5]
            if(str(data)==givenValue):
                gateway.entry_point.reportPass('service verified')
            else:
                gateway.entry_point.reportFail('response not matching')
                
        if(classifier.predict(testcase) == 2):
            print('Action is classified as Hover')
            hover = Hover()
             # pass the action to textfield class 
            status_flag = hover.action(str(sen),driver)
            if(status_flag == 1 ):
                gateway.entry_point.reportPass('testcase :'+sen+' is successful')
            else:
                gateway.entry_point.reportFail('testcase :'+sen+' is fail')
                break
            
        if(classifier.predict(testcase) == 5):
            print('Action is classified as Validation')
            array = sen.split("'")
            
            if("www" in array[1] or "WWW" in array[1]):
                ##### Page URL Validation  #######
                url = array[1]
                if(driver.current_url == url):
                    gateway.entry_point.reportPass('Asserted : Page URL is correct as Actual : '+url+' And Expected : '+driver.current_url)
                else:
                    gateway.entry_point.reportFail('Asserted : Page URL is not correct as Actual : '+url+' And Expected : '+driver.current_url)
            elif("Page title" in sen or "page title" in sen or "Page Title" in sen):
                ##### Page Title Validation  #######
                title = array[1]
                if(driver.title == title):
                    gateway.entry_point.reportPass('Asserted : Page title is correct as Actual : '+title+' And Expected : '+driver.title)
                else:
                    gateway.entry_point.reportFail('Asserted : Page title is not correct as Actual : '+title+' And Expected : '+driver.title)
            elif('not displayed' in sen or 'not Displayed' in sen or 'not present' in sen or 'Not Present' in sen or 'not Present' in sen ):
                 ##### Element Displayed Validation  #######
                 Element = findElement.FindElement()
                 elem = Element.action(str(sen),driver)
                 if not elem.is_displayed():
                     gateway.entry_point.reportPass('Asserted: '+sen)
                 else:
                    gateway.entry_point.reportFail('Asserted: '+sen)
            elif('displayed' in sen or 'Displayed' in sen or 'present' in sen or 'Present' in sen):
                 ##### Element Displayed Validation  #######
                 Element = findElement.FindElement()
                 elem = Element.action(str(sen),driver)
                 if(elem.is_displayed()):
                     gateway.entry_point.reportPass('Asserted: '+ sen)
                 else:
                    gateway.entry_point.reportFail('Asserted: '+ sen)
            elif('enabled' in sen or 'enable' in sen):
                 ##### Element Enabled Validation  #######
                 Element = findElement.FindElement()
                 elem = Element.action(str(sen),driver)
                 if(elem.is_enabled()):
                     gateway.entry_point.reportPass('Asserted: '+ array[1]+' is Enabled')
                 else:
                    gateway.entry_point.reportFail('Asserted: '+ array[1]+' is not Enabled')
            elif('not selected' in sen or 'unselected' in sen):
                 ##### Element Not Selected Validation  #######
                 Element = findElement.FindElement()
                 elem = Element.action(str(sen),driver)
                 if not elem.is_selected():
                     gateway.entry_point.reportPass('Asserted: '+ array[1]+' is not selected')
                 else:
                    gateway.entry_point.reportFail('Asserted: '+ array[1]+' is selected but not expected')
            elif('selected' in sen):
                 ##### Element Selected Validation  #######
                 Element = findElement.FindElement()
                 elem = Element.action(str(sen),driver)
                 if(elem.is_selected()):
                     gateway.entry_point.reportPass('Asserted: '+ array[1]+' is selected')
                 else:
                    gateway.entry_point.reportFail('Asserted: '+ array[1]+' is not selected')
            elif('equal to' in sen or 'equals to' in sen or 'equals' in sen or 'equal' in sen):
                Element = findElement.FindElement()
                elem = Element.action(str(sen),driver)
                text = elem.text
                if(text == array[3]):
                    gateway.entry_point.reportPass("Asserted : "+sen)
                else:
                    gateway.entry_point.reportFail("Asserted :"+sen)
    
        
    driver.close()
    gateway.entry_point.endAll()