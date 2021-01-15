from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from getpass import getpass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

BROWSER = None

def pageLoaded():
    status = BROWSER.execute_script('return document.readyState;')
    print(status)
    return status == 'complete'

def sendMsg(userID, message):
    #Open the BROWSER and go to login page
    global BROWSER 
    BROWSER = webdriver.Firefox()
    BROWSER.get('http://mbasic.facebook.com/')

    #Login to the fb account
    username_ipt = BROWSER.find_element_by_id("m_login_email")
    username_ipt.send_keys(input("Num/Email :"))

    password_ipt = BROWSER.find_element_by_name("pass")
    password_ipt.send_keys(getpass())

    BROWSER.find_element_by_name("login").click()
    while not pageLoaded(): 
        pass

    sleep(2)
        
    #Redirect to the message page of the user
    BROWSER.get('http://mbasic.facebook.com/messages/thread/'+ userID)
    while not pageLoaded(): pass

    #Type the message and send it
    message_ipt = BROWSER.find_element_by_id("composerInput")
    message_ipt.send_keys(message)

    BROWSER.find_element_by_name("send").click()