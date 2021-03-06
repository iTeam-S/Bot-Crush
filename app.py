# ********* SECTION IMPORTATION *******
import os
from datetime import datetime
import random
from threading import Thread
from datetime import datetime
import re

from conf import ITEAMS_ACCESS_TOKEN
from conf import ITEAMS_LOGIN, ITEAMS_PASS
from flask import Flask, request

from messenger import Messenger
from scripts.requete import Requete
from scripts.utils import encode

# **************************************


# ********* SECTION INSTANCIATION ******
VERIFY_TOKEN = 'jedeconne'
app = Flask(__name__)
bot = Messenger(ITEAMS_ACCESS_TOKEN)
req = Requete()
os.environ['ITEAMS_ACCESS_TOKEN'] = ITEAMS_ACCESS_TOKEN
os.environ['ITEAMS_LOGIN'] = ITEAMS_LOGIN
os.environ['ITEAMS_PASS'] = ITEAMS_PASS
os.environ['PROD'] = '0'
def send_add_friend (dest_id, lien_profil):
    lien_profil = lien_profil.lower()

    try:
        bot.send_action(dest_id, 'mark_seen')
        bot.send_action(dest_id, 'typing_on')  
        req.insertTache(2, dest_id, None)

    except Exception as err:
        print(err)
        bot.send_message(dest_id, "❌❌❌Oh, une erreur s'est produite :-/")
        return        


    


def send_code_confirmation(dest_id, lien_profil):
    """
        Fonction pour envoyer le code de confirmation
            a un utilisateur donnée en parametre
    """

    bot.send_action(dest_id, 'mark_seen')
    # bot.send_message(destID, "Je suis arriver")
    lien_profil = lien_profil.lower()

    username = lien_profil.split('facebook.com/')[-1]
    if 'profile.php' not in username:
        username = username.split('?')[0]
    username = username[:-1] if username[-1] == '/' else username

    sexe = bot.get_gender(dest_id)
    code = random.randint(1000, 9999)
    message_envoie_code = [
        {
            "mg" : "",
            "fr" : "Garder pour vous seul votre code." ,
            "ang" :"Rejoice it seems someone has feelings for you"
        },
        {
            "mg" : "",
            "fr" : "Ne partager à personne votre code." ,
            "ang" : ""
        },
        {
            "mg" : "",
            "fr" : "Assurer vous que vous seul est accès à ce code",
            "ang" : ""
        }
    ]
    message = message_envoie_code[random.randint(0, 2)]["fr"]
    message += "\nVotre code de confirmation est: " + str(code)

    try:
        bot.send_action(dest_id, 'mark_seen')
        bot.send_action(dest_id, 'typing_on')
        req.updateCode(dest_id, username, code, None, sexe)   
        req.insertTache(3, dest_id, message)

    except Exception as err:
        print(err)
        bot.send_message(dest_id, "❌❌❌Oh, une erreur s'est produite :-/")
        return

    else:
        bot.send_message(dest_id, "Nous vous informerons quand \
        votre code de confirmation sera envoyé.")
        req.setAction(dest_id, None)
    bot.send_action(dest_id, 'typing_off')


def verif_code_confirmation(dest_id, code, message, action):
    if req.verifCode(dest_id, code):
        req.validerInscription(dest_id)
        bot.send_action(dest_id, 'mark_seen')
        bot.send_action(dest_id, 'typing_on')
        bot.send_message(dest_id, message)
        bot.send_action(dest_id, 'typing_off')
        req.setAction(dest_id, action)
    else:
        bot.send_action(dest_id, 'mark_seen')
        bot.send_action(dest_id, 'typing_on')
        bot.send_message(dest_id, "❌Le code semble incorrect.\
            Veuillez saisir un code valide ;-) .")
        bot.send_action(dest_id, 'typing_off')
        req.setAction(dest_id, None)
        return


def ajout_crush(dest_id, lien_crush):
    bot.send_action(dest_id, 'mark_seen')
    lien_crush = lien_crush.lower()
    username = lien_crush.split('facebook.com/')[-1]
    if 'profile.php' not in username:
        username = username.split('?')[0]
    username = username[:-1] if username[-1] == '/' else username

    bot.send_action(dest_id, 'mark_seen')
    bot.send_action(dest_id, 'typing_on')
    bot.send_message(dest_id, "☺Cela peut prendre quelques secondes, \
    veuillez patienter s'il vous plaît.")
    bot.send_action(dest_id, 'typing_off')
    heure_actuel = datetime.now()
    heure_actuel = heure_actuel.replace(hour=(heure_actuel.hour+1) % 24).strftime("%H:%M")
    prevenir_crush = [
        {
            "mg" : "",
            "fr" : "Youhou :-), :-D Quelqu'un a des sentiments pour toi. C'était à \
            " + heure_actuel + " via notre page ITeam-$ Bot Crush.\n",
            "ang" : "Rejoice it seems someone has feelings for you"
        },
        {
            "mg" : "",
            "fr" : "Bonne nouvelle! quelqu'un vient de dire \
            à la page ITeam-$ Bot Crush \
            qu'il crush pour vous. C'était à " + heure_actuel,
            "ang" : ""
        },
        {
            "mg": "",
            "fr" : "Félicitation <3,\
            une personne vient de nous informer qu'elle crush \
            sur vous dans la page iTeam-$ Bot Crush :-)\
            à " + heure_actuel,
            "ang" : ""
        }
    ]
    messages = prevenir_crush[random.randint(0, 2)]["fr"]
    messages += "\n Visiter la page pour connaître le fonctionnement. Merci"
    # req.insertTache(1, dest_id, messages, f'{{"username_crush": "{encode(username)}" }}')
    # bot.send_quick_reply(dest_id, LIEN_PROFIL=messages)
    bot.send_quick_reply(dest_id, TEXTE_PERSONNALISER=messages, USERNAME= username)  
    req.setAction(dest_id, "ATTENTE_TEXTE")


def verif_nb_crush(sender_id):
    bot.send_action(sender_id, 'mark_seen')
    nb_crush = req.verifNbCrush(sender_id)

    if nb_crush:
        bot.send_action(sender_id, 'typing_on')
        bot.send_message(sender_id, "😑😑😑Malheureusement vous avez atteint\
        le nombre limite de crushs pour ce mois. Revenez le mois prochain.")
        bot.send_action(sender_id, 'typing_off')
        req.setAction(sender_id, None)
        return

    else:
        bot.send_action(sender_id, 'typing_on')
        bot.send_message(sender_id, "Veuillez nous fournir le lien de profil \
        de votre crush❣ s'il vous plaît")
        bot.send_action(sender_id, 'typing_off')
        req.setAction(sender_id, 'ATTENTE_LIEN_CRUSH')

        return  # on empeche le code de continuer


def traitement(sender_id, message):
    """
        ATO ZAO NY FONCTION TENA IASA
        SATRIA NO MANAO TRAITEMENT ISIKA
    """

    print('ici')

    # ajout dans la base si non present
    req.verifUtilisateur(sender_id)

    # inona no tokony atao le utilisateur
    statut = req.getAction(sender_id)

    if statut == 'ATTENTE_LIEN_PROFIL':
        send_code_confirmation(sender_id, message)
        return
    elif statut == 'ATTENTE_TEXTE':
        if message.startswith('__TEXTE_PERSONNALISER_'):
            if message.startswith('_TEXTE_PERSONNALISER_NON'):
                mes = message.split("***")
                req.insertTache(1, sender_id , "Alors la vous ne voulez pas envoyer de \
                de texte personnaliser alors", f'{{"username_crush": "{encode(mes[2])}" }}')
            elif message.startswith('_TEXTE_PERSONNALISER_OUI'):
                mes = message.split("***")
                req.insertTache(1, sender_id , "Alors la vous voulez envoyer de \
                de texte personnaliser alors", f'{{"username_crush": "{encode(mes[2])}" }}')
            req.setAction(sender_id, None)
        return

    elif statut == 'ATTENTE_CODE_CONFIRMATION':
        verif_code_confirmation(sender_id, message, "✔Votre inscription \
            a été confirmée :-) .", None)
        return

    elif statut == "ATTENTE_LIEN_CRUSH":
        ajout_crush(sender_id, message)
        return

    # on enleve les espaces du devant et du derriere si present
    message = message.strip()
    if message.startswith('_INSCRIPTION'):
        # ENTRANT DANS LE MENU INSCRIPTION

        if message == '_INSCRIPTION_NOUVEAU':
            bot.send_action(sender_id, 'mark_seen')
            bot.send_action(sender_id, 'typing_on')
            bot.send_message(sender_id, "Veuillez fournir le lien de votre \
                profil s'il vous plait.")
            req.setAction(sender_id, 'ATTENTE_LIEN_PROFIL')
            bot.send_action(sender_id, 'typing_off')
            return

        elif message == '_INSCRIPTION_VALIDER':
            bot.send_action(sender_id, 'mark_seen')
            bot.send_action(sender_id, 'typing_on')
            bot.send_message(sender_id, "Veuillez saisir le code\
            de confirmation qu'on vient de vous envoyer s'il vous plait.")
            bot.send_action(sender_id, 'typing_off')
            req.setAction(sender_id, 'ATTENTE_CODE_CONFIRMATION')
            return

        else:
            bot.send_action(sender_id, 'mark_seen')
            bot.send_action(sender_id, 'typing_on')
            bot.send_quick_reply(sender_id, MENU_INSCRIPTION=True)
            bot.send_action(sender_id, 'typing_off')
            return

    elif message.startswith('_AJOUTER'):
        verif_nb_crush(sender_id)
        return


    # ataoko vue aloa le message
    bot.send_action(sender_id, 'mark_seen')

    # ataoko en train d'ecrire
    bot.send_action(sender_id, 'typing_on')

    # envoie du menu principale
    print(bot.send_quick_reply(
        sender_id, MENU_PRINCIPALE=True,
        INSCRIPTION=req.verifInscription(sender_id)
    ).text)

    # anjanona le en train d ecrire
    bot.send_action(sender_id, 'typing_off')

    req.setAction(sender_id, None)

    print('ici 2')


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    """
        Route andefasany Facebook requete amntsika
    """

    if request.method == 'GET':
        # Mandefa GET izy ra iverifier hoe mande ve le serveur
        token_sent = request.args.get("hub.verify_token")
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")

    elif request.method == "POST":
        # recuperena le json nalefany facebook
        body = request.get_json()
        # alefa any amn processus afa manao azy
        run = Thread(target=analyse, args=[body])
        run.start()

    return 'OK'


def analyse(body):
    for event in body['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):

                sender_id = message['sender']['id']
                if message['message'].get('quick_reply'):
                    traitement(
                        sender_id,
                        message['message'].get('quick_reply').get('payload')
                    )
                elif message['message'].get('text'):
                    traitement(sender_id, message['message'].get('text'))

            # elif message.get('postback'): pass


if __name__ == '__main__':
    app.run(port=6000)
