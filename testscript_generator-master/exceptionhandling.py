# -*- coding: utf-8 -*-




from selenium import webdriver
#import test

class Textfield:
    
    def action(self,sentence,driver):
       
        array = sentence.split("'")
        #temp = "//input[contains(@text,'"+array[3]+"')]"
        temp = "//input[@title = '"+array[3]+"']"
        inputbox = driver.find_element_by_xpath(temp)
        inputbox.clear()
        inputbox.send_keys(array[1])