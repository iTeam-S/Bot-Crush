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
    username_ipt.send_keys("0349144933")

    password_ipt = BROWSER.find_element_by_name("pass")
    password_ipt.send_keys("__rootKit@")

    BROWSER.find_element_by_name("login").click()
    while not pageLoaded(): 
        pass

    sleep(1)
        
    #Redirect to the message page of the user
    BROWSER.get('http://mbasic.facebook.com/messages/thread/'+ userID)
    while not pageLoaded(): pass

    #If the user is not a friend
    try:
        message_ipt = WebDriverWait(BROWSER, 5).until(EC.presence_of_element_located((By.NAME, "body")))
    #If the user is a friend
    except:
        message_ipt = WebDriverWait(BROWSER, 5).until(EC.presence_of_element_located((By.ID, "composerInput"))) 
    #In the case of error


    # #If the user is a friend   
    # if EC.presence_of_element_located((By.NAME, "body")): 
    #     message_ipt = BROWSER.find_element_by_name("body")
    # # #If the user is not a friend
    # elif EC.presence_of_element_located((By.ID, "composerInput")): 
    #     message_ipt = BROWSER.find_element_by_id("composerInput")

    # message_ipt = BROWSER.find_element_by_id("composerInput")
    message_ipt.send_keys(message)
    BROWSER.find_element_by_name("send").click()
