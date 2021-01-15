import requests, re
from bs4 import BeautifulSoup


def getUserId(username):
    r = requests.get("https://mbasic.facebook.com/" + username)

    src_code = BeautifulSoup(r.text, 'html.parser')

    for balise_a in src_code.find_all('a') :
        link = balise_a.get('href')
        if link.startswith('/r.php?')
            return re.findall(r"[0-9]{15}", link)[0]






