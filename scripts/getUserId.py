import requests, re
from bs4 import BeautifulSoup


def getUserId(username):
    '''
        A partir d'un username du profil facebook, 
            retourne l'userID sinon None si Not found
    '''

    # Les données du cookies du navigateur
    auth_cookies = {
        'c_user': '',
        'xs': '' 
    }

    s = requests.Session()
    r = s.get("https://mbasic.facebook.com/" + username, cookies=auth_cookies)
    
    if r.status_code == 404:
        return

    src_code = BeautifulSoup(r.text, 'html.parser')

    for balise_a in src_code.find_all('a') :
        link = balise_a.get('href')
        if link.startswith('/r.php?') or 'profile_id' in link:
            return re.findall(r"[0-9]{15}", link)[0]
