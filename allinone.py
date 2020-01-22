import pickle
import pandas as pd
import csv
from selenium import webdriver
from py4j.java_gateway import JavaGateway, GatewayParameters
import re
import pickle
from nltk.corpus import stopwords
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import json
import os.path
import findElement


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

        array = url.split("'")
        print("http://"+array[1])
        driver.get("http://"+array[1])

        return 1 
    
class Dropdown:

    def action(self,sentence,driver):

        driver.implicitly_wait(1)

        array = sentence.split("'")
        flag = 0

        temp = ""
# =============================================================================
# try to find the element using different strategies
# and status flag keeps track of whether the element has been found
# =============================================================================
        try:
            if(flag==0):
                flag =1
                temp = "//select[contains(@class,'"+array[3]+"')]"
                elem = driver.find_element_by_xpath(temp)
                print("this is by @class for "+array[3])
        except NoSuchElementException:
                flag =0
                pass
        
        try:
            if(flag==0):
                flag =1
                temp = "//select[contains(@id,'"+array[3]+"')]"
                elem = driver.find_element_by_xpath(temp)
                print("this is by @id for "+array[3])
        except NoSuchElementException:
                flag =0
                pass
        
        try:
            if(flag==0):
                flag =1
                temp = "//select[@id='"+array[3]+"']"
                elem = driver.find_element_by_xpath(temp)
                print("this is by @id for "+array[3])
        except NoSuchElementException:
                flag =0
                pass
        
        try:
            if(flag==0):
                flag =1
                temp = "//select[@class='"+array[3]+"']"
                elem = driver.find_element_by_xpath(temp)
                print("this is by @class for "+array[3])
        except NoSuchElementException:
                flag =0
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

#        try:
#            if(flag==0):
#                flag=1
#                temp = "//*[text()='"+ array[1]+"']/.."
#                elem = driver.find_element_by_xpath(temp)
#                print('this is by super'+array[3]+array[1])
#        except NoSuchElementException:
#                flag=0
#                pass
#        
        dic = {}
        driver.implicitly_wait(1)
        #name = driver.current_url
        name = driver.title
        name = re.sub(r'\W','',str(name))
        #name = name[-15:]
        print(name)
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
        with open(filepath) as csv_file :

            csv_reader = csv.reader(csv_file,delimiter=';')
            line_count=0
            for row in csv_reader:
                if line_count==0:
                    line_count+=1
                else:
                    dic[row[1]] = row[2]

#if element not found yet then check in dictionary
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

        option = None
#perform action
        if(flag == 1):
            elem.click()
            dropdown = Select(elem)
            try:
                option = dropdown.select_by_visible_text(array[1])
            except NoSuchElementException:
                option = False
                pass
        if(option == False):
            dropdown = Select(elem)
            try:
                option = dropdown.select_by_value(array[1])
            except NoSuchElementException:
                option = False
                pass
        else:
            print('elements not found')
            return flag
#if new window opens switch windows
        windowhandle = driver.window_handles
        if(len(windowhandle)>1):
            switchwindow = driver.window_handles[-1]
            driver.switch_to_window(switchwindow)


#if element found and not in dictionary then update dictionary
        if(flag==1):
            if not array[3] in dic.keys():
                dic[array[3]] = temp
# write dictionary to csv file of object map for current page
        df = pd.DataFrame( [(k,v) for k,v in dic.items()],columns = ['key','value'])
        df.to_csv(filepath,sep = ';')
        return flag

class Button:

    def action(self,sentence,driver):

        array = sentence.split("'")

        flag = 0
        driver.implicitly_wait(1)

        temp=""
# =============================================================================
# try to find the element using different strategies
# and status flag keeps track of whether the element has been found
# =============================================================================
        try :
            if(flag==0):
                temp ="//button[contains(@id,'"+ array[1]+"')]"
                elem = driver.find_element_by_xpath(temp)
                flag=1
                print('this is by //button_@id')
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

        try:
            if(flag==0):
               elem = driver.find_element_by_link_text(array[1])
               flag=1
               print('this is by link text()')

        except NoSuchElementException:

           flag =0
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
                temp ="//*[text()='"+ array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                flag=1
                print('this is by text')

        except NoSuchElementException :
            flag =0
            pass

        validFlag = 0

        dic = {}
        #name = driver.current_url
        driver.implicitly_wait(1)
        name = driver.title
        name = re.sub(r'\W','',str(name))
        #name = name[-15:]
        print(name)
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
            if array[1] in dic.keys():
               try:
                    temp = dic[array[1]]
                    print(temp)
                    flag=1
                    elem = driver.find_element_by_xpath(dic[array[1]])
                    print('element found in dictionary')
               except NoSuchElementException:
                    flag=0
                    pass

        driver.implicitly_wait(2)

        if(flag==1):
             try:
                if(elem.is_displayed()):
                    print('pass')
                    validFlag = 1
             except:
                print('valid flag didnt work')
                pass
        else:
            print('element not found')
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
#if element found and not in dictionary then update dictionary
        if(flag==1):
            if not array[1] in dic.keys():
                dic[array[1]] = temp
#if new window opens switch windows
        windowhandle = driver.window_handles
        if(len(windowhandle)>1):
            switchwindow = driver.window_handles[-1]
            driver.switch_to_window(switchwindow)
# write dictionary to csv file of object map for current page
        df = pd.DataFrame( [(k,v) for k,v in dic.items()],columns = ['key','value'])
        df.to_csv(filepath,sep = ';')



        return flag and validFlag

class Textfield:

    def action(self,sentence,driver):

        driver.implicitly_wait(2)

        array = sentence.split("'")
        flag = 0 ;
# =============================================================================
# try to find the element using different strategies
# and status flag keeps track of whether the element has been found
# =============================================================================
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
                temp = "//input[contains(@text,'"+array[3]+"')]"
                inputbox = driver.find_element_by_xpath(temp)
                print('this is by contains @text')
        except NoSuchElementException :
            flag =0
            pass
        
        try:
            if(flag==0):
               temp = "//*[contains(@value,'"+array[3]+"')]"
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
                temp = "//*[contains(text(),'"+array[3]+"')]//..//input"
                inputbox = driver.find_element_by_xpath(temp)
                print('this is by contains placeholder')
        except NoSuchElementException :
            flag =0
            pass


        validFlag = 0

        dic = {}
        #name = driver.current_url
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
            if array[3] in dic.keys():
               try:
                    temp = dic[array[3]]
                    flag=1
                    inputbox = driver.find_element_by_xpath(temp)
                    print('element found in dictionary')
               except NoSuchElementException:
                    flag=0
                    pass
#perform action
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
#if element found and not in dictionary then update dictionary
        if(flag==1):
            if not array[3] in dic.keys():
                dic[array[3]] = temp
# write dictionary to csv file of object map for current page
        df = pd.DataFrame( [(k,v) for k,v in dic.items()],columns = ['key','value'])
        df.to_csv(filepath,sep = ';')
        return flag and validFlag


# establish connection to java gateway entry point
gateway = JavaGateway(gateway_parameters=GatewayParameters())

browserFilePath = "DriverConfig/BrowserType.txt"
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

print(mylist)


sample = mylist

for sen in sample:


# =============================================================================
#     vectorize the testcase and then predict class using classifier
# =============================================================================
    testcase = [sen]
    testcase = vectorizer.transform(testcase).toarray()
    print(classifier.predict(testcase))

    if(classifier.predict(testcase) ==0):
        print("button")
        button = Button()
        # pass the action to button class 
        status_flag  = button.action(str(sen),driver)
        if(status_flag == 1 ):
            gateway.entry_point.reportPass('testcase :'+sen+' is successful')
        else:
            gateway.entry_point.reportFail('testcase :'+sen+' is fail')
            break


    if(classifier.predict(testcase) ==5):
        print("dropdown")
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
        print("get")
        get = Get()
         # pass the action to get class 
        status_flag = get.browse(str(sen),driver)
        if(status_flag == 1 ):
            gateway.entry_point.reportPass('testcase :'+sen+' is successful')
        else:
            gateway.entry_point.reportFail('testcase :'+sen+' is fail')
            break

    if(classifier.predict(testcase) ==6):

        print("textfield")
        textfield = Textfield()
         # pass the action to textfield class 
        status_flag = textfield.action(str(sen),driver)
        if(status_flag == 1 ):
            gateway.entry_point.reportPass('testcase :'+sen+' is successful')
        else:
            gateway.entry_point.reportFail('testcase :'+sen+' is fail')
            break

    if(classifier.predict(testcase) == 3):
        gateway.entry_point.reportPass('***** Running WebService Test*****')
        print('getservice')
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


    if(classifier.predict(testcase) == 2):
        gateway.entry_point.reportPass('***** Running WebService Test*****')
        print('post service')
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

    if(classifier.predict(testcase) == 4):
        print('validation')
        array = sen.split("'")
        
        if('Hover' in sen or 'hover' in sen):
            Element = findElement.FindElement()
            elem = Element.action(str(sen),driver)
            hover = ActionChains(driver).move_to_element(elem)
            hover.perform()        
        if('wait for' in sen):
            driver.implicitly_wait(5)
        if('equal to' in sen):
            Element = findElement.FindElement()
            elem = Element.action(str(sen),driver)
            text = elem.text
            if(text == array[3]):
                gateway.entry_point.reportPass("Asserted : "+sen)
            else:
                gateway.entry_point.reportFail("Asserted :"+sen)
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

    
driver.close()
gateway.entry_point.endAll()
print('program has ended')