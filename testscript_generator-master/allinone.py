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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

df = pd.read_excel(r"testcases.xlsx", sheet_name=1) # can also index sheet by name or fetch all sheets
mylist = df['Actions'].tolist()


reviews = load_files('Functionalties')

x,y = reviews.data , reviews.target

with open('x.pickle','wb') as f:
    pickle.dump(x,f)
    
with open('y.pickle','wb') as f:
    pickle.dump(y,f)
    
corpus = []
for i in range(0, len(x)):
    review = re.sub(r'\W',' ',str(x[i]))
    review = review.lower()
    review = re.sub(r'\s+[a-z]\s+',' ',review)
    review = re.sub(r'^[a-z]\s+','', review)
    review = re.sub(r'\s+', ' ', review)
  
    corpus.append(review)

vectorizer = TfidfVectorizer(max_features=100, min_df=3,max_df=0.8,stop_words=stopwords.words('english'))

X_train, X_test, Y_train, Y_test = train_test_split(corpus, y, test_size=0.3, random_state=42)

X_train = vectorizer.fit_transform(X_train).toarray()
X_test = vectorizer.transform(X_test).toarray()

classifier = LogisticRegression(random_state=42, solver='newton-cg', max_iter=1000, multi_class='multinomial', n_jobs=-1)
classifier.fit(X_train, Y_train)

class Get:
    
    def browse(self,url,driver):
        
        array = url.split("'")
        print("http://"+array[1])
        driver.get("http://"+array[1])
        
        return 1
    
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

class Button:
        
    def action(self,sentence,driver,dic):  
            
        array = sentence.split("'")
       
        flag = 0
        driver.implicitly_wait(1)
        
        temp=""
            
        try :
            if(flag==0):
                temp ="//button[@class='"+ array[1]+"']"
                elem = driver.find_element_by_xpath(temp)
                flag=1 
                print('this is by //button_@class')
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
        
        validFlag = 0 
        
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
        
        driver.implicitly_wait(1)
        
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
       
        if(flag==1):
            if not array[1] in dic.keys():
                dic[array[1]] = temp 
            
        windowhandle = driver.window_handles
        if(len(windowhandle)>1):
            switchwindow = driver.window_handles[-1]
            driver.switch_to_window(switchwindow)
            
        
            
        
        
        return flag and validFlag
    
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
        


dic = {}

with open('object_map.txt') as csv_file :
    csv_reader = csv.reader(csv_file,delimiter=',')
    line_count = 0 
    for row in csv_reader:
        if line_count == 0 :
            line_count += 1
        else:
            dic[row[1]] = row[2]

print(dic)
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=20509))
driver = webdriver.Chrome()


print(mylist)


sample = mylist

for sen in sample:
    
    
    
    testcase = [sen]
    testcase = vectorizer.transform(testcase).toarray()
   
    print(classifier.predict(testcase))
    
    if(classifier.predict(testcase) ==0):
        print("button")
        button = Button()
        status_flag  = button.action(str(sen),driver,dic) 
        if(status_flag == 1 ):
            gateway.entry_point.reportPass('testcase :'+sen+' is succesful')
        else:
            gateway.entry_point.reportFail('testcase :'+sen+' is fail')
            break
            
        
    if(classifier.predict(testcase) ==3):
        print("dropdown")
        dropdown = Dropdown()
        status_flag = dropdown.action(str(sen),driver,dic)
        if(status_flag == 1 ):
            gateway.entry_point.reportPass('testcase :'+sen+' is succesful')
        else:
            gateway.entry_point.reportFail('testcase :'+sen+' is fail')
            break
        
    if(classifier.predict(testcase) ==1):
        print("get")
        get = Get()
        status_flag = get.browse(str(sen),driver)
        if(status_flag == 1 ):
            gateway.entry_point.reportPass('testcase :'+sen+' is succesful')
        else:
            gateway.entry_point.reportFail('testcase :'+sen+' is fail')
            break
        
    if(classifier.predict(testcase) ==2):
        
        print("textfield")
        textfield = Textfield()
        status_flag = textfield.action(str(sen),driver,dic)
        if(status_flag == 1 ):
            gateway.entry_point.reportPass('testcase :'+sen+' is succesful')
        else:
            gateway.entry_point.reportFail('testcase :'+sen+' is fail')
            break


df = pd.DataFrame( [(k,v) for k,v in dic.items()],columns = ['key','value'])
df.to_csv('object_map.txt',sep = ',')

       
gateway.entry_point.endAll()
print('program has ended')

