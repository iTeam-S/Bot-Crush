import requests, re
from scripts.browser import WebBrowser
from bs4 import BeautifulSoup
from scripts.utils import *


def getUserId(username, driver):
    '''
        A partir d'un username du profil facebook, 
            retourne l'userID sinon None si Not found
    '''

    # Les données du cookies du navigateur

    cookies = {cookie['name']:cookie['value'] for cookie in driver.browser.get_cookies()}

    s = requests.Session()
    r = s.get("https://mbasic.facebook.com/" + username, cookies=cookies)

    if r.status_code == 404:
        return

    src_code = BeautifulSoup(r.text, 'html.parser')

    for balise_a in src_code.find_all('a') :
        link = balise_a.get('href')
        if link != None and (link.startswith('/r.php?') or 'profile_id' in link or 'owner_id' in link):
            res = re.findall(r"1000[0-9]{11}", link)
            if len(res) > 0: return res[0]


