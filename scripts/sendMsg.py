import os, time, pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

Browser = None

def pageLoaded(Browser):
    '''
        Pour verifier qu'un driver a fini de charger la page...
            True dans ce cas , sinon False
    '''
    status = Browser.execute_script('return document.readyState;')
    print(status)
    return status == 'complete'

def connexion(Browser):

    #Login to the fb account
    username_ipt = Browser.find_element_by_id("m_login_email")
    username_ipt.send_keys(os.environ.get("ITEAMS_LOGIN"))
    print("Variable env => ",os.environ.get("ITEAMS_LOGIN"))

    password_ipt = Browser.find_element_by_name("pass")
    password_ipt.send_keys(os.environ.get("ITEAMS_PASS"))
    print("Variable env => ",os.environ.get("ITEAMS_PASS"))

    Browser.find_element_by_name("login").click()

    while not pageLoaded(Browser): time.sleep(0.5)
    
    with open("cookies.pkl","wb") as fcookies:
        pickle.dump(Browser.get_cookies() , fcookies)


def sendMsg(Browser, userID, message):
    '''
        Fonction pour envoyer un message specifique à utilisateur Facebook
            Elle admet trois parametres, le driver, l'userID (ex: 100000144) et le message en texte.
    '''
    Browser.get('https://mbasic.facebook.com/')
    while not pageLoaded(Browser): time.sleep(0.5)

    if os.path.isfile('cookies.pkl'):
        with open("cookies.pkl", "rb") as fcookies:
            cookies = pickle.load(fcookies)
            for cookie in cookies:
                Browser.add_cookie(cookie)

    else: connexion(Browser)
    #Redirect to the message page of the user
    Browser.get('https://mbasic.facebook.com/messages/thread/'+ userID)
    while not pageLoaded(Browser): time.sleep(0.5)

    if 'login.php' in Browser.current_url: 
        connexion(Browser)
        Browser.get('https://mbasic.facebook.com/messages/thread/'+ userID)
        while not pageLoaded(Browser): time.sleep(0.5)

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