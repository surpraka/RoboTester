from selenium import webdriver
#import test

class Get:
    
    def browse(self,url,driver):
        
        array = url.split("'")
        print("http://"+array[1])
        driver.get("http://"+array[1])
        
        return 1