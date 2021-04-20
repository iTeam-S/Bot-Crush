import time
from scripts.utils import pageLoaded

def delMsg(Browser, userID): 
    '''
        Fonction pour effacer automatiquement les messages de tout les utilisateurs
    après l'envoie de message.
        Elle prend une seule paramètre: ex =delMsg(ratodisoa)
    '''
    pageID = "100142865413064"
    
    # Accéder à la page des messages
    Browser.get("https://mbasic.facebook.com/messages/read/?tid=cid.c."+userID+"%3A"+pageID+"&pageID="+pageID)
    while not pageLoaded(Browser): time.sleep(0.5)
    Browser.find_element_by_tag_name('body').screenshot("conn0.png")
    print(Browser.page_source)
    Browser.find_element_by_name("delete").click()
    Browser.find_element_by_tag_name('body').screenshot("conn2.png")
    print(Browser.page_source)
    # Effacer le message 
    while not pageLoaded(Browser):time.sleep(0.5)
    Browser.find_element_by_link_text("Supprimer").click()
    Browser.find_element_by_tag_name('body').screenshot("con3.png")


