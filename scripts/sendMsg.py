import os, time, pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scripts.utils import connexion, pageLoaded


def sendMsg(Browser, userID, message):
    '''
        Fonction pour envoyer un message specifique à utilisateur Facebook
            Elle admet trois parametres, le driver, l'userID (ex: 100000144) et le message en texte.
    '''
    # Connecter le driver à Facebook
    connexion(Browser)

    # Redirect to the message page of the user
    Browser.get('https://mbasic.facebook.com/messages/thread/'+ userID)
    while not pageLoaded(Browser): time.sleep(0.5)
        
    body = BROWSER.find_element_by_tag_name("body")
    print(body.get_attribute('outerHTML'))
    body.screenshot("./log1.png")

    # If the user is not a friend
    try:
        message_ipt = WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.NAME, "body")))
    #If the user is a friend
    except:
        message_ipt = WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.ID, "composerInput")))
    
    message_ipt.send_keys(message)
    try:
        Browser.find_element_by_name("Send").click()
    except:
        Browser.find_element_by_name("send").click()
