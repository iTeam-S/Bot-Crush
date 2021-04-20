import time
from scripts.utils import pageLoaded


def sendMsg(Browser, userID, message):
    '''
        Fonction pour envoyer un message specifique à utilisateur Facebook
            Elle admet trois parametres, le driver, l'userID (ex: 100000144) et le message en texte.
    '''
    # Connecter le driver à Facebook
    while not pageLoaded(Browser): time.sleep(0.5)
    # Redirect to the message page of the user
    Browser.find_element_by_tag_name('body').screenshot("conn.png")
    Browser.get('https://mbasic.facebook.com/messages/thread/'+ userID)
    while not pageLoaded(Browser): time.sleep(0.5)

    # If the user is not a friend
    try:
        message_ipt = Browser.find_element_by_name("body")
    # If the user is a friend
    except:
        message_ipt = Browser.find_element_by_id("composerInput")

    #Browser.find_element_by_tag_name('body').screenshot("test.png")
    #message_ipt = Browser.find_element_by_tag_name('textarea')

    message_ipt.send_keys(message)
    
    #Send the message
    try:
        Browser.find_element_by_name("Send").click()
    except:
        Browser.find_element_by_name("send").click()