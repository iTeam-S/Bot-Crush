import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BROWSER = None

def pageLoaded(BROWSER):
    '''
        Pour verifier qu'un driver a fini de charger la page...
            True dans ce cas , sinon False
    '''
    status = BROWSER.execute_script('return document.readyState;')
    print(status)
    return status == 'complete'


def sendMsg(BROWSER, userID, message):
    '''
        Fonction pour envoyer un message specifique à utilisateur Facebook
            Elle admet trois parametres, le driver, l'userID (ex: 100000144) et le message en texte.
    '''
    #Open the BROWSER and go to login page
    BROWSER.get('http://mbasic.facebook.com/')

    #Login to the fb account
    username_ipt = BROWSER.find_element_by_id("m_login_email")
    username_ipt.send_keys(os.environ.get("iteam-s_login"))

    password_ipt = BROWSER.find_element_by_name("pass")
    password_ipt.send_keys(os.environ.get("iteam-s_login"))

    BROWSER.find_element_by_name("login").click()
    while not pageLoaded(BROWSER): time.sleep(0.5)
  
    #Redirect to the message page of the user
    BROWSER.get('http://mbasic.facebook.com/messages/thread/'+ userID)
    while not pageLoaded(BROWSER): pass

    # If the user is not a friend
    try:
        message_ipt = WebDriverWait(BROWSER, 5).until(EC.presence_of_element_located((By.NAME, "body")))
    #If the user is a friend
    except:
        message_ipt = WebDriverWait(BROWSER, 5).until(EC.presence_of_element_located((By.ID, "composerInput"))) 
    message_ipt.send_keys(message)
    BROWSER.find_element_by_name("Send").click()