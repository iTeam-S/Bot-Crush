# ********* SECTION IMPORTATION *******
<<<<<<< HEAD
import os, random
=======
import os
>>>>>>> refs/remotes/origin/main
from flask import Flask, request
from threading import Thread

from scripts.sendMsg import sendMsg
from scripts.getUserId import getUserId
<<<<<<< HEAD
from scripts.utils import encrypt
from scripts.browser import WebBrowser
from conf import ITEAMS_ACCESS_TOKEN
from conf import ITEAMS_LOGIN, ITEAMS_PASS
from messenger import Messenger
from scripts.requete import Requete
=======
from conf import ITEAMS_ACCESS_TOKEN
from messenger import Messenger
>>>>>>> refs/remotes/origin/main

# **************************************


# ********* SECTION INSTANCIATION ******

VERIFY_TOKEN = 'jedeconne'

app = Flask(__name__)
bot = Messenger(ITEAMS_ACCESS_TOKEN)
<<<<<<< HEAD
req = Requete()
=======

os.environ['ITEAMS_ACCESS_TOKEN'] = ITEAMS_ACCESS_TOKEN

# **************************************
>>>>>>> refs/remotes/origin/main

os.environ['ITEAMS_ACCESS_TOKEN'] = ITEAMS_ACCESS_TOKEN
os.environ['ITEAMS_LOGIN'] = ITEAMS_LOGIN
os.environ['ITEAMS_PASS'] = ITEAMS_PASS
os.environ['PROD'] = '0'

<<<<<<< HEAD
# **************************************
=======
def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Diso ooo'
>>>>>>> refs/remotes/origin/main


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    '''
        Route andefasany Facebook requete amntsika 
    '''
    if request.method == 'GET':
        # Mandefa GET izy ra iverifier hoe mande ve le serveur
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    elif request.method == "POST":
        # akato ndreka izy mandefa an le message tonga amn page iny mits
        # recuperena le json nalefany facebook 
        body = request.get_json()
        # alefa any amn processus afa manao azy 
        run = Analyse(body)
        # tsy mila miandry an le Analyse vita fa  lasa le code
        run.start()

    return "Voray ry Facebook fa Misoatra a!", 200


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Diso ooo'


class Analyse(Thread):
    def __init__(self, body):
        Thread.__init__(self)
        self.body = body
    
    def run(self):
        for event in self.body['entry']:
            messaging = event['messaging']
            for message in messaging:

                if message.get('message'):
                    senderID = message['sender']['id']
                    
                    if message['message'].get('quick_reply'):
                        traitement(senderID, message['message'].get('quick_reply').get('payload'))

                    elif message['message'].get('text'):
                        traitement(senderID, message['message'].get('text'))
                    
                elif message.get('postback'):
                    pass


def send_codeConfirmation(destID, lien_profil):
    '''
        Fonction pour envoyer le code de confirmation
            a un utilisateur donné en question
    '''
    bot.send_action(destID, 'mark_seen')
    lien_profil = lien_profil.lower()
    username = lien_profil.split('facebook.com/')[-1]
    userId = getUserId(username)

    if not userId:
        bot.send_action(destID, 'mark_seen')
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "Votre Lien semble incorrecte :-/")
        bot.send_action(destID, 'typing_off')
        req.setAction(destID, None)
        return
        
    sexe = bot.get_gender(destID)
    code = random.randint(1000, 9999)
    
    browser = WebBrowser()
    message = "Votre code de confirmation est: " + str(code)

    try:
        bot.send_action(destID, 'mark_seen')
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "Ca peut prendre quelque secondes ,veuillez patienter s'il vous plaît.")
        bot.send_action(destID, 'typing_off') 
        sendMsg(browser.browser, userId, message)
        req.updateCode(destID, username,code,userId,sexe)

    except Exception as err:
        print(err)
        
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "oh, une erreur s'est produite :-/")
        bot.send_action(destID, 'typing_off')
        return

    else:
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "Veuillez fournir le code de confirmation.")
        bot.send_action(destID, 'typing_off')
        req.setAction(destID, 'ATTENTE_CODE_CONFIRMATION')

    finally:
        # on ferme le browser
        browser.browser.close()
        del browser # on supprime la variable


def verif_codeConfirmation(destID, code, message,action):

    if req.verifCode(destID, code)  :
        req.validerInscription(destID)
        bot.send_action(destID, 'mark_seen')
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, message)
        bot.send_action(destID, 'typing_off')
        req.setAction(destID, action)
    else:
        bot.send_action(destID, 'mark_seen')
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "Le code semble incorrecte. Veuillez bien verifier ;-) .")
        bot.send_action(destID, 'typing_off')
        req.setAction(destID, None)
        return


def ajoutCrush(destID, lien_crush):

    bot.send_action(destID, 'mark_seen')
    lien_crush = lien_crush.lower()
    username = lien_crush.split('facebook.com/')[-1]

    bot.send_action(destID, 'mark_seen')
    bot.send_action(destID, 'typing_on')
    bot.send_message(destID, "Cela peut prendre quelque secondes ,veuillez patienter s'il vous plaît.")
    bot.send_action(destID, 'typing_off')
    
    crushID = getUserId(username)

    if not crushID:
        bot.send_action(destID, 'mark_seen')
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "Votre Lien semble incorrecte :-/")
        bot.send_action(destID, 'typing_off')
        req.setAction(destID, None)
        return

    browser = WebBrowser()

    try:         
        sendMsg(browser.browser, crushID,"Félicitation , une personne vient de nous informer qu'elle crush sur vous dans la page iTeam-$ Bot Crush :-) .")
        req.ajoutCrush(encrypt(crushID), encrypt(destID))
        req.match(destID)
        
    except Exception as err:
        print(err)
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "Oh,vraiment désolé mais une erreur s'est produite :-/")
        bot.send_action(destID, 'typing_off')
        req.setAction(destID, None)

    else:
        nb_crush=req.getNbCrush(destID)
        bot.send_action(destID, 'typing_on')
        bot.send_message(destID, "La personne est informée, merci d'avoir cru en nous.")
        Nb_crush_restant = 3 - nb_crush
        if Nb_crush_restant==0:

            Reponse="Avec cette opération vous avez épuisez les trois tentatives de crushé sur une personne pour ce mois."

        else :

            Reponse="Vous pouvez encore crushé sur "+ str (3 - nb_crush) +" personne pendant ce mois."

        bot.send_message(destID, Reponse)        
        bot.send_action(destID, 'typing_off')

        req.setAction(destID, None)

    finally:
        browser.browser.close()
        del browser
    
    res, val = req.match(req.getUserID(destID))

    if res[1]:
        for v in val:
            i = 0
            bot.send_action(v[0], 'typing_on')
            msg = f'''
            Felicitation à vous et à ce profil : https://facebook.com/{v[1]} 

            💓💓💓💓💓💓💓💓💓💓💓 Youuuu 💓💓💓💓💓💓💓💓

            Vous vous crusher l'un de l'autre ❤️ ️❤️️ ❤️️ ❤️️ ❤️️
            '''
            bot.send_message(v[0],msg, prio=0==i)
            bot.send_action(v[0],'typing_off')
            i += 1


def verifnbcrush (senderID):

    bot.send_action(senderID, 'mark_seen')

    nb_crush=req.getNbCrush(encrypt(senderID))


    if (nb_crush>=3):

        bot.send_action(senderID, 'typing_on')
        bot.send_message(senderID, "Malheureusement pour ce mois vous avez épuisé les trois tentatives de faire cette opération. Revenez le mois prochain.")
        bot.send_action(senderID, 'typing_off')
        req.setAction(senderID, None)
        return

    else :

        bot.send_action(senderID, 'typing_on')
        bot.send_message(senderID,"Veuillez nous fournir votre code de  confirmation.")         
        bot.send_action(senderID, 'typing_off')
        req.setAction(senderID,'ATTENTE_CODE_CRUSH')

        return # on empeche le code de continuer


        

def traitement(senderID, message):
    ''' 
        ATO ZAO NY FONCTION TENA IASA 
        SATRIA NO MANAO TRAITEMENT ISIKA
    '''

    # ajout dans la base si non present
    req.verifUtilisateur(senderID)

    # inona no tokony atao le utilisateur
    statut = req.getAction(senderID)

    if statut == 'ATTENTE_LIEN_PROFIL':
        send_codeConfirmation(senderID, message)
        return
    elif statut == 'ATTENTE_CODE_CONFIRMATION':
        verif_codeConfirmation(senderID, message,"Votre inscription a été confirmé :-) .", None)
        bot.send_codeConfirmation(senderID,"Souvenez vous votre code de confirmation. Vous allez en avoir besoin plutard.")
        return
    elif statut=='ATTENTE_CODE_CRUSH':
        verif_codeConfirmation(senderID, message,"Veuillez nous fournir le lien de son profil s'il vous plaît.","ATTENTE_LIEN_CRUSH")
        return
    elif statut=="ATTENTE_LIEN_CRUSH":
        ajoutCrush(senderID,message)     
        return

    # on enleve les espaces du devant et du derriere si present
    message = message.strip()

    if message.startswith('_INSCRIPTION'):
        # ENTRANT DANS LE MENU INSCRIPTION

        if message == '_INSCRIPTION_NOUVEAU':
            bot.send_action(senderID, 'mark_seen')
            bot.send_action(senderID, 'typing_on')
            bot.send_message(senderID, "Veuillez fournir le lien de votre profil s'il vous plait.")
            req.setAction(senderID, 'ATTENTE_LIEN_PROFIL')
            bot.send_action(senderID, 'typing_off')
            return

        elif message == '_INSCRIPTION_VALIDER':
            bot.send_action(senderID, 'mark_seen')
            bot.send_action(senderID, 'typing_on')
            bot.send_message(senderID, "Veuillez fournir le code de confirmation qu'on vient de vous envoyer s'il vous plait.")
            bot.send_action(senderID, 'typing_off')
            req.setAction(senderID, 'ATTENTE_CODE_CONFIRMATION')
            return

        else:
            bot.send_action(senderID, 'mark_seen')
            bot.send_action(senderID, 'typing_on')
            bot.send_quick_reply(senderID, MENU_INSCRIPTION=True)
            bot.send_action(senderID, 'typing_off')
            
            return

    elif message.startswith('_AJOUTER'):

        verifnbcrush(senderID)

        return




    # ataoko vue aloa le message
    bot.send_action(senderID, 'mark_seen')

    # ataoko en train d'ecrire 
    bot.send_action(senderID, 'typing_on')

    # envoie du menu principale
    bot.send_quick_reply(senderID, MENU_PRINCIPALE=True, INSCRIPTION=req.verifInscription(senderID))

    # anjanona le en train d ecrire
    bot.send_action(senderID, 'typing_off')

    req.setAction(senderID, None)


class Analyse(Thread):
    def __init__(self, body):
        Thread.__init__(self)
        self.body = body
    
    def run(self):
        for event in self.body['entry']:
            messaging = event['messaging']
            for message in messaging:

                if message.get('message'):
                    senderID = message['sender']['id']
                    
                    if message['message'].get('quick_reply'):
                        traitement(senderID, message['message'].get('quick_reply').get('payload'))

                    elif message['message'].get('text'):
                        traitement(senderID, message['message'].get('text'))
                    
                elif message.get('postback'):
                    pass


def traitement(senderID, message):
    ''' 
        ATO ZAO NY FONCTION TENA IASA 
        SATRIA NO MANAO TRAITEMENT ISIKA
    '''

    # on enleve les espace du devant et du derriere si present
    message = message.strip()

    if message.startswith('_INSCRIPTION'):
        # ENTRANT DANS LE MENU INSCRIPTION

        if message == '_INSCRIPTION_NOUVEAU':
            bot.send_message(senderID, "Pas encore fonctionnel") 
        elif message == '_INSCRIPTION_VALIDER':
            bot.send_message(senderID, "Pas encore fonctionnel") 
        else:
            bot.send_action(senderID, 'mark_seen')
            bot.send_action(senderID, 'typing_on')
            bot.send_quick_reply(senderID, MENU_INSCRIPTION=True)
            bot.send_action(senderID, 'typing_off')

        return # on empeche le code de continuer


    # ataoko vue aloa le message
    bot.send_action(senderID, 'mark_seen')
    # ataoko en train d'ecrire 
    bot.send_action(senderID, 'typing_on')
    # envoie de message
    # bot.send_message(senderID, "ito message nao takeo: " + message)
    # envoie du menu principale
    bot.send_quick_reply(senderID, MENU_PRINCIPALE=True)
    # anjanona le en train d ecrire
    bot.send_action(senderID, 'typing_off')



if __name__ == '__main__':
    app.run(port=6000)
