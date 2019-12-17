from get import Get
from button import Button
from textfield import Textfield
from dropdown import Dropdown
import model
from selenium import webdriver
import HTMLTestRunner


driver = webdriver.Chrome()

driver.get('https://www.mfs.com')
#elem = driver.find_element_by_xpath("(//div[@role='navigation']//a[contains(.,'Investment Professional')])[1]//*['svg'][contains(@class,'icon')]")
#elem = driver.find_element_by_css_selector("a.left-link > svg.icon.icon-dir-down")
elem = driver.find_element_by_css_selector("div[class*='left'] a[title*='Change your location'] span[class*='label-selected'] + svg[viewBox]")
elem.click()

sample = [ "select 'UNITED STATES' from 'Change your location' dropdown",
         "select 'INDIVIDUAL INVESTOR' from 'Select your role'"]


for sen in sample:
    
    sample1 = [sen]
    sample1 = vectorizer.transform(sample1).toarray()
    print(classifier.predict(sample1))
    
    if(classifier.predict(sample1) ==0):
        print("button")
        button = Button()
        button.action(str(sen),driver) 
        
    if(classifier.predict(sample1) ==3):
        print("dropdown")
        dropdown = Dropdown()
        dropdown.action(str(sen),driver)
        
    if(classifier.predict(sample1) ==1):
        print("get")
        get = Get()
        get.browse(str(sen),driver)
        
    if(classifier.predict(sample1) ==2):
        
        print("textfield")
        textfield = Textfield()
        textfield.action(str(sen),driver)
        
if __name__ == "__main__":
    HTMLTestRunner.main()

#driver.find_element_by_xpath("(//a[contains(@href,'contact-us')])[1]").click()