import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import connexion,pageLoaded
from getUserId import getUserId
from browser import WebBrowser

def delMsg(username): 
    '''
        Fonction pour effacer automatiquement les messages de tout les utilisateurs
    après l'envoie de message.
        Elle prend une seule paramètre: ex =delMsg(ratodisoa)
    '''

    page_id= "100142865413064"
    user_id=str(getUserId(username))
    #print (user_id)
    browser =  WebBrowser()
    driver= browser.browser
    connexion(driver)
    links="https://mbasic.facebook.com/messages/read/?tid=cid.c."+user_id+"%3A"+page_id
    driver.get(links)
    while not pageLoaded(driver): 
        time.sleep(0.5)
    driver.find_element_by_name("delete").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Supprimer"))).click()

    driver.close()



