from get import Get
from button import Button
from textfield import Textfield
from dropdown import Dropdown
import model
import pickle
import pandas as pd
import csv

from selenium import webdriver

from py4j.java_gateway import JavaGateway, GatewayParameters



sample1= ["open 'www.mfs.com'",
         "click on 'Menu'",
         "click on 'Products & Strategies'", 
         "click on 'Mutual Funds'", 
         "Select 'Massachusetts Investors Trust' from 'Select a Fund' dropdownlist"]

sample2 = ["opem 'www.mfs.com'", 
          "click on 'Search'",
          "enter text 'Mutual Fund' in the 'Search' box"]


# =============================================================================
# sample3 = ["open 'www.mfs.com'",
#           "click on 'left-container'", 
#           "select 'Australia' from 'Change your location' dropdown list'"]
# =============================================================================

sample4 = ["open 'www.mfs.com'",
          "'Register' is clicked",
          "click on 'INVESTMENT PROFESSIONAL'",
          "click on 'UNITED STATES'",
          "click on 'Financial Advisor'",
          "click on 'I AGREE'",
          "enter 'password' in 'password'",
          "ENTER 'BAT123' IN 'userName'",
          "Click on 'Complete'"
          ]

# =============================================================================
# sample5 = ["open 'www.mfs.com",
#            "click on 'INDIVIDUAL INVESTOR'",
#          "select 'UNITED STATES' from 'Change your location' dropdown",
#          "select 'INDIVIDUAL INVESTOR' from 'Select your role'"
#          ]
# =============================================================================


# =============================================================================
# sample6 = ["open 'www.amazon.in'",
#             "click on 'Best Sellers'",
#             "click on 'Movers and Shakers'",
#             "click on 'Don't Lose Out, Work Out!'",
#             "click on 'Add To Cart'"
#             ]
# =============================================================================
sample6 = ["open 'www.amazon.in'",
            "click on 'Amazon Pay'",
            "click on 'Your Offers'",
            "click on 'Sign in'"
            ]


sample7 = ["open 'www.facebook.com'",
           "Enter 'Bat123' in 'email'",
           "Enter 'password' in 'pass'",
           "Enter 'Batman' in 'First name'",
           "Enter 'Begins' in 'Surname'",
           "Enter '825416973' in 'Mobile number or email address'"
           "Enter 'newpassword' in 'reg_passwd__'"
           "Select '30' fron 'Day' dropdown list"
           "Select 'Mar' fron 'Month' dropdown list"
           "Select '1997' fron 'Year' dropdown list"
           "Click on 'Male' to specify gender"
           "Click on 'Sign Up' to register"]


# =============================================================================
# sample8 =  ["open 'www.mfs.com'",
#           "'Login' is clicked",
#           "enter 'password' in 'userpassword'",
#           "ENTER 'BAT123' IN 'userid'",
#           "click on 'Login'"
#           ]
# =============================================================================

sample9 = ["open 'www.geeksforgeeks.org'",
           "Click on 'GBlog'"]

sample10 = ["open 'www.publicissapient.com'",
            "click on 'menu'",
            "click on 'Careers'",
            "Select 'Business Development' from 'Select a Discipline'dropdown",
            "Select 'India, Gurgaon' from 'Select a Location' dropdown",
            "Click on 'Search Jobs'",
            "enter 'freelance' in 'Keywords'",
            "Select 'India' from 'Select a region'",
            "Select 'India - Haryana - Gurgaon' from 'All Locations'",
            "Select 'Internship' from 'Select a type of job'",
            "Select 'Program Management' from 'Select a discipline'",
            "click on 'Search'"
            ]

# =============================================================================
# sample11 = ["open 'careers.publicissapient.com'",
#             "Select 'Business Development' from 'Select a Discipline'dropdown",
#             "Select 'India, Gurgaon' from 'Select a Location' dropdown",
#             "Click on 'Search Jobs'"
#             ]
# =============================================================================

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
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=25536))
driver = webdriver.Chrome()

df = pd.read_excel(r"testcases.xlsx", sheet_name=1) # can also index sheet by name or fetch all sheets
mylist = df['Actions'].tolist()

print(mylist)


sample = mylist

for sen in sample7:
    
    
    
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