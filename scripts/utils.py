import hashlib
import os
import pickle
import re
import time

import requests
from bs4 import BeautifulSoup


def page_loaded(Browser):
    """
        Pour verifier qu'un driver a fini de charger la page...
            True dans ce cas , sinon False
    """
    status = Browser.execute_script('return document.readyState;')
    return status == 'complete'


def connexion(Browser):
    """
        fonction de connexion pour le driver donnee en parametre
        avec verification de presence de cookie.
    """
    Browser.get('https://mbasic.facebook.com/')

    if os.path.isfile('cookies.pkl'):
        with open("cookies.pkl", "rb") as fcookies:
            cookies = pickle.load(fcookies)
            for cookie in cookies:
                try:
                    Browser.add_cookie(cookie)
                except:
                    os.remove('cookies.pkl')
                    connexion(Browser)
        Browser.get('https://mbasic.facebook.com/')
        while not page_loaded(Browser):
            time.sleep(0.5)
        Browser.find_element_by_tag_name('body').screenshot("conn.png")
        if 'login' in Browser.current_url:
            print('Je me login encore')
            try:
                os.remove('cookies.pkl')
            except FileNotFoundError:
                pass
            finally:
                connexion(Browser)
        return
    Browser.get('https://mbasic.facebook.com/')
    # Login to the fb account
    # print(Browser.page_source)
    # print(Browser.current_url)
    if '/cookie/' in Browser.current_url:
        print('ato va')
        Browser.find_element_by_xpath('//button[@type="submit"]').click()
    Browser.find_element_by_tag_name('body').screenshot("conn1.png")
    username_ipt = Browser.find_element_by_id("m_login_email")
    username_ipt.send_keys(os.environ.get("ITEAMS_LOGIN"))
    print("Variable env => ", os.environ.get("ITEAMS_LOGIN"))

    password_ipt = Browser.find_element_by_name("pass")
    password_ipt.send_keys(os.environ.get("ITEAMS_PASS"))

    Browser.find_element_by_name("login").click()
    while not page_loaded(Browser):
        time.sleep(0.5)
    Browser.find_element_by_tag_name('body').screenshot("conn1.png")
    print("connexion success")
    with open("cookies.pkl", "wb") as fcookies:
        pickle.dump(Browser.get_cookies(), fcookies)


def send_msg(Browser, userID, message):
    """
        Fonction pour envoyer un message specifique à utilisateur Facebook
            Elle admet trois parametres, le driver, l'userID (ex: 100000144) et le message en texte.
    """
    # Connecter le driver à Facebook
    while not page_loaded(Browser):
        time.sleep(0.5)
    # Redirect to the message page of the user
    Browser.find_element_by_tag_name('body').screenshot("conn.png")
    Browser.get('https://mbasic.facebook.com/messages/thread/' + userID)
    while not page_loaded(Browser):
        time.sleep(0.5)

    # If the user is not a friend
    try:
        message_ipt = Browser.find_element_by_name("body")
    # If the user is a friend
    except:
        message_ipt = Browser.find_element_by_id("composerInput")

    # Browser.find_element_by_tag_name('body').screenshot("test.png")
    # message_ipt = Browser.find_element_by_tag_name('textarea')

    message_ipt.send_keys(message)

    # Send the message
    try:
        Browser.find_element_by_name("Send").click()
    except:
        Browser.find_element_by_name("send").click()


def del_msg(Browser, userID):
    """
        Fonction pour effacer automatiquement les messages de tout les utilisateurs
    après l'envoie de message.
        Elle prend une seule paramètre: ex =del_msg(ratodisoa)
    """
    page_id = "100142865413064"

    # Accéder à la page des messages
    Browser.get(
        "https://mbasic.facebook.com/messages/read/?tid=cid.c." + userID + "%3A" + page_id + "&page_id=" + page_id)
    while not page_loaded(Browser):
        time.sleep(0.5)
    Browser.find_element_by_tag_name('body').screenshot("conn0.png")
    print(Browser.page_source)
    Browser.find_element_by_name("delete").click()
    Browser.find_element_by_tag_name('body').screenshot("conn2.png")
    print(Browser.page_source)
    # Effacer le message 
    while not page_loaded(Browser):
        time.sleep(0.5)
    Browser.find_element_by_link_text("Supprimer").click()
    Browser.find_element_by_tag_name('body').screenshot("con3.png")


def get_user_id(username, driver):
    """
        A partir d'un username du profil facebook,
            retourne l'userID sinon None si Not found
    """

    # Les données du cookies du navigateur

    cookies = {cookie['name']: cookie['value'] for cookie in driver.browser.get_cookies()}

    s = requests.Session()
    r = s.get("https://mbasic.facebook.com/" + username, cookies=cookies)
    print(r)
    if r.status_code == 404:
        return

    src_code = BeautifulSoup(r.text, 'html.parser')

    for balise_a in src_code.find_all('a'):
        link = balise_a.get('href')
        print(link)
        if link is not None and (link.startswith('/r.php?') or 'profile_id' in link or 'owner_id' in link or 'thread' in link):
            print('--- : ', link)
            res = re.findall(r"1000[0-9]{11}", link)
            if len(res) > 0: return res[0]
    print('tsy naita ? ')



def decode(txt_encode):
    txt = ''
    for u in txt_encode.split('-'):
        txt = txt + chr(int(u))
    return txt


def encode(txt):
    txt_encode = ''
    for u in txt:
        txt_encode = txt_encode + str(ord(u)) + '-'
    return txt_encode[:-1]
