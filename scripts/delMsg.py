import time
from utils import connexion,pageLoaded
from getUserId import getUserId

def delMsg(Browser, userID): 
    '''
        Fonction pour effacer automatiquement les messages de tout les utilisateurs
    après l'envoie de message.
        Elle prend une seule paramètre: ex =delMsg(ratodisoa)
    '''
    pageID = "100142865413064"
    connexion(Browser)
    
    # Accéder à la page des messages
    Browser.get("https://mbasic.facebook.com/messages/read/?tid=cid.c."+userID+"%3A"+pageID+"&pageID="+pageID)
    while not pageLoaded(Browser): time.sleep(0.5)
    Browser.find_element_by_name("delete").click()
    
    # Effacer le message 
    while not pageLoaded(Browser):time.sleep(0.5)
    Browser.find_element_by_link_text("Supprimer").click()

    driver.close()
