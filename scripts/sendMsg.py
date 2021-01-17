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
    print("Variable env => ",os.environ.get("ITEAMS_LOGIN"))
    print("Variable env => ",os.environ.get("ITEAMS_PASS"))
    
    #Open the BROWSER and go to login page
    BROWSER.get('http://mbasic.facebook.com/')

    #Login to the fb account
    username_ipt = BROWSER.find_element_by_id("m_login_email")
    username_ipt.send_keys(os.environ.get("ITEAMS_LOGIN"))
   
    password_ipt = BROWSER.find_element_by_name("pass")
    password_ipt.send_keys(os.environ.get("ITEAMS_PASS"))
    

    BROWSER.find_element_by_name("login").click()
    while not pageLoaded(BROWSER): time.sleep(0.5)
  
    #Redirect to the message page of the user
    BROWSER.get('http://mbasic.facebook.com/messages/thread/'+ userID)
    while not pageLoaded(BROWSER): time.sleep(0.5)

    # If the user is not a friend
    try:
        message_ipt = WebDriverWait(BROWSER, 10).until(EC.presence_of_element_located((By.NAME, "body")))
    #If the user is a friend
    except:
        message_ipt = WebDriverWait(BROWSER, 10).until(EC.presence_of_element_located((By.ID, "composerInput")))
    else:
        print("Can't find input")
    message_ipt.send_keys(message)
    BROWSER.find_element_by_name("Send").click()
