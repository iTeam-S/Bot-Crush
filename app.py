# ********* SECTION IMPORTATION *******
import os
import random
from threading import Thread

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


# **************************************


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
    message = "ATTENTION, ne donner à personne votre code ...\n"
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

    req.insertTache(1, dest_id, "Félicitations :-*, \
        une personne vient de nous informer qu'elle crush \
        sur vous dans la page iTeam-$ Bot Crush :-)\nhttps://web.facebook.com/iteamsbot",
         f'{{"username_crush": "{encode(username)}" }}')

    req.setAction(dest_id, None)


def verif_nb_crush(sender_id):
    bot.send_action(sender_id, 'mark_seen')
    nb_crush = req.getNbCrush(sender_id)

    if nb_crush >= 3:
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

    # ajout dans la base si non present
    req.verifUtilisateur(sender_id)

    # inona no tokony atao le utilisateur
    statut = req.getAction(sender_id)

    if statut == 'ATTENTE_LIEN_PROFIL':
        send_code_confirmation(sender_id, message)
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
    bot.send_quick_reply(
        sender_id, MENU_PRINCIPALE=True,
        INSCRIPTION=req.verifInscription(sender_id)
    )

    # anjanona le en train d ecrire
    bot.send_action(sender_id, 'typing_off')

    req.setAction(sender_id, None)

    req._close()


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
