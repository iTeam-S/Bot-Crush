import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from getUserId import getUserId
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
    x = os.environ.get("ITEAMS_LOGIN")
    print("Variable env => ", x)
    print("Variable env => ",os.environ.get("ITEAMS_PASS"))
    
    #Open the BROWSER and go to login page
    BROWSER.get('http://mbasic.facebook.com/')

    #Login to the fb account
    username_ipt = BROWSER.find_element_by_id("m_login_email")
    username_ipt.send_keys(os.environ.get("ITEAMS_LOGIN"))
   
    password_ipt = BROWSER.find_element_by_name("pass")
    password_ipt.send_keys(os.environ.get("ITEAMS_PASS"))
    
    body = BROWSER.find_element_by_tag_name("body")
    print(body.get_attribute('outerHTML'))
    body.screenshot("./log0.png")

    BROWSER.find_element_by_name("login").click()
    while not pageLoaded(BROWSER):
        time.sleep(0.5)
    body = BROWSER.find_element_by_tag_name("body")
    print(body.get_attribute('outerHTML'))
    body.screenshot("./log1.png")

    #Redirect to the message page of the user
    BROWSER.get('http://mbasic.facebook.com/messages/thread/'+ userID)
    body = BROWSER.find_element_by_tag_name("body")
    print(body.get_attribute('outerHTML'))
    body.screenshot("./log2.png")

    return
    
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


'''
    Pour effacer l'historique de message entre le Bot et ces utilisateurs.
'''

def delete_messages( BROWSER,username):
    page_id="100142865413064"
    user_id=getUserId(username)
    links="https://mbasic.facebook.com/messages/read/?tid=cid.c."+user_id+"%3A"+page_id
    BROWSER.get(links)
    BROWSER.find_element_by_name("delete").click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "Supprimer"))).click()
