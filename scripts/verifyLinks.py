import requests,re
from browser import WebBrowser
from utils import connexion
from bs4 import BeautifulSoup

'''
Une fonction qui passe en paramètre le lien envoyé par l'utilisateur et qui return une valeur booléene True
si c'st validé,False si ça ne l'est pas.
exemple:
    verify_links("https://mbasic.facebook.com/rivolalaina.rajaonarivony") =>True
'''
def verify_links(links):
    if (links.startswith("https://www.facebook.com/") is True or links.startswith("https://mbasic.facebook.com/") is True):        
        browser =  WebBrowser()
        driver= browser.browser
        connexion(driver)
        cookies = {cookie['name']:cookie['value'] for cookie in driver.get_cookies()}        
        request = requests.Session()
        if (links.startswith("https://www.facebook.com/")) is True:
            mbasic_links=links.replace("https://www.facebook.com/","https://mbasic.facebook.com/")
        else:
            mbasic_links=links
        r = request.get(mbasic_links, cookies=cookies)
        src_code = BeautifulSoup(r.text, 'html.parser')
        x=src_code.find("a", string="Trouver de l’aide ou signaler un profil")
        if (x is not None):
            return True
        else :
            return False
        driver.close()  
    else :       
        return False      
