import json

from conf import ITEAMS_ACCESS_TOKEN
from conf import ITEAMS_LOGIN, ITEAMS_PASS

from messenger import Messenger
from scripts.browser import WebBrowser
from scripts.requete import Requete
from scripts.utils import *

os.environ['ITEAMS_ACCESS_TOKEN'] = ITEAMS_ACCESS_TOKEN
os.environ['ITEAMS_LOGIN'] = ITEAMS_LOGIN
os.environ['ITEAMS_PASS'] = ITEAMS_PASS
os.chdir('/home/iteams/Bot-Crush')


def tache1(data):
    try:
        del_msg(driver.browser, req.getUserID(data[2]))
    except Exception as err:
        print(err)

    username_crush = decode(json.loads(data[-1]).get('username_crush'))
    crushId = get_user_id(username_crush, driver)
    print(crushId)
    if not crushId:
        bot.send_action(data[2], 'mark_seen')
        bot.send_action(data[2], 'typing_on')
        bot.send_message(data[2], "❌Votre lien semble incorrect :-/")
        bot.send_action(data[2], 'typing_off')
        req.updateFinishJob(data[0])
        return
    try:
        send_msg(driver.browser, crushId, data[3])
        req.ajoutCrush(crushId, data[2])
        bot.send_action(data[2], 'mark_seen')
        bot.send_action(data[2], 'typing_on')
        bot.send_message(data[2], "✔Votre crush a été bien enregistrer. \n Merci pour votre confiance.")
        req.setAction(data[2], None)

    except Exception as err:
        print(err)
        bot.send_message(data[2], "❌❌❌Oh, une erreur s'est produite :-/")
        req.updateFinishJob(data[0])
        return None
    bot.send_action(data[2], 'typing_off')

    res, val = req.match(req.getUserID(data[2]))
    if res[1]:
        for v in val:
            i = 0
            bot.send_action(v[0], 'typing_on')
            msg = f'''
			Félicitations à vous et à :
			
			https://www.facebook.com/{v[1]} 


			❣❣❣Vous vous crusher l'un sur l'autre❣❣❣
			😍😍😍Vous avez rencontrer votre âme soeur💕
			'''
            bot.send_message(v[0], msg, prio=0 == i)
            bot.send_action(v[0], 'typing_off')
            i += 1
        req.updateNotif(val[0][0], val[1][0])
    req.updateFinishJob(data[0])


def tache2(data):
    pass


def tache3(data):
    username = req.getUserName(data[2])
    user_id = get_user_id(username, driver)
    if not user_id:
        bot.send_action(data[2], 'mark_seen')
        bot.send_action(data[2], 'typing_on')
        bot.send_message(data[2], "❌Votre Lien semble incorrecte :-/")
        bot.send_action(data[2], 'typing_off')
        req.setAction(data[2], None)
        req.updateFinishJob(data[0])
        return
    sexe = bot.get_gender(data[2])
    try:
        send_msg(driver.browser, user_id, data[3])
        req.setUserID(user_id, data[2])
        bot.send_action(data[2], 'mark_seen')
        bot.send_action(data[2], 'typing_on')
        bot.send_message(data[2], "Verifier vos messages, votre code a été envoyé :-)")
        try : 
            add_friend(driver.browser, user_id)   
            bot.send_message(data[2], "Veuillez accepter , notre demande d'ami s'il vous plaît") 
        except Exception as err :
            print("On est déjà ami")
            pass   
        req.setAction(data[2], 'ATTENTE_CODE_CONFIRMATION')
        bot.send_message(data[2], "Veuillez saisir votre code de confirmation")
    except Exception as err:
        print(err)
        bot.send_message(data[2], "❌❌❌Oh, une erreur s'est produite :-/")
        req.updateFinishJob(data[0])
        return
    req.updateFinishJob(data[0])


if __name__ == '__main__':
    driver = WebBrowser()
    connexion(driver.browser)
    req = Requete()
    bot = Messenger(ITEAMS_ACCESS_TOKEN)

    while True:
        req = Requete()
        taches = req.getTaches()
        print(taches)
        for tch in taches:
            if tch[1] == 1:
                tache1(tch)
            elif tch[1] == 2:
                tache2(tch)
            elif tch[1] == 3:
                tache3(tch)
            time.sleep(5)
        req._close()
        time.sleep(10)
