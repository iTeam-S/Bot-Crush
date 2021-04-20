# ********* SECTION IMPORTATION *******
import os, random
from flask import Flask, request
from threading import Thread

from scripts.getUserId import getUserId
from scripts.utils import encrypt, encode
from conf import ITEAMS_ACCESS_TOKEN
from conf import ITEAMS_LOGIN, ITEAMS_PASS
from messenger import Messenger
from scripts.requete import Requete
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


def send_codeConfirmation(destID, lien_profil):
    '''
        Fonction pour envoyer le code de confirmation
            a un utilisateur donnée en parametre
    '''
   
    bot.send_action(destID, 'mark_seen')
    # bot.send_message(destID, "Je suis arriver")
    lien_profil = lien_profil.lower()

    
    username = lien_profil.split('facebook.com/')[-1]
    if 'profile.php' not in username:
        username = username.split('?')[0]
    username = username[:-1] if username[-1] == '/' else username

    sexe = bot.get_gender(destID)
    code = random.randint(1000, 9999)
    message = "ATTENTION, ne donner à personne votre code ...\n"
    message += "\nVotre code de confirmation est: " + str(code)
    
    try:
        bot.send_action(destID, 'mark_seen')
        bot.send_action(destID, 'typing_on')
        req.updateCode(destID, username, code, None, sexe)
        req.insertTache(3, destID, message) 
        
    except Exception as err:
        print(err)     
        bot.send_message(destID, "❌❌❌Oh, une erreur s'est produite :-/")
        return

    else:
        bot.send_message(destID, "Nous vous informerons quand votre code de confirmation sera envoyé.")
        req.setAction(destID, None)
    bot.send_action(destID, 'typing_off')


def verif_codeConfirmation(destID, code, message, action):

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
        bot.send_message(destID, "❌Le code semble incorrect. Veuillez saisir un code valide ;-) .")
        bot.send_action(destID, 'typing_off')
        req.setAction(destID, None)
        return


def ajoutCrush(destID, lien_crush):

    bot.send_action(destID, 'mark_seen')
    lien_crush = lien_crush.lower()
    username = lien_crush.split('facebook.com/')[-1]
    if 'profile.php' not in username:
        username = username.split('?')[0]
    username = username[:-1] if username[-1] == '/' else username


    bot.send_action(destID, 'mark_seen')
    bot.send_action(destID, 'typing_on')
    bot.send_message(destID, "☺Cela peut prendre quelques secondes, veuillez patienter s'il vous plaît.")
    bot.send_action(destID, 'typing_off')
      
    req.insertTache (1, destID,
        "Félicitations :-*, une personne vient de nous informer qu'elle crush sur vous dans la page iTeam-$ Bot Crush :-)",
        f'{{"username_crush": "{encode(username)}" }}'
    )
   
    req.setAction(destID, None)
    
   

def verifnbcrush (senderID):
    bot.send_action(senderID, 'mark_seen')
    nb_crush=req.getNbCrush(encrypt(senderID))

    if (nb_crush>=3):
        bot.send_action(senderID, 'typing_on')
        bot.send_message(senderID, "😑😑😑Malheureusement vous avez atteint le nombre limite de crushs pour ce mois. Revenez le mois prochain.")
        bot.send_action(senderID, 'typing_off')
        req.setAction(senderID, None)
        return

    else :
        # verif_codeConfirmation(senderID, message,"Veuillez nous fournir le lien de son profil s'il vous plaît.","ATTENTE_LIEN_CRUSH")
        bot.send_action(senderID, 'typing_on')
        bot.send_message(senderID, "Veuillez nous fournir le lien de profil de votre crush❣ s'il vous plaît")         
        bot.send_action(senderID, 'typing_off')
        req.setAction(senderID,'ATTENTE_LIEN_CRUSH')

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
        verif_codeConfirmation(senderID, message,"✔Votre inscription a été confirmée :-) .", None)
        # a etudier
        # bot.send_codeConfirmation(senderID,"Souvenez vous votre code de confirmation. Vous allez en avoir besoin plutard.")
        return

    # elif statut=='ATTENTE_CODE_CRUSH':
    #     verif_codeConfirmation(senderID, message,"Veuillez nous fournir le lien de son profil s'il vous plaît.","ATTENTE_LIEN_CRUSH")
    #     return

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
            bot.send_message(senderID, "Veuillez saisir le code de confirmation qu'on vient de vous envoyer s'il vous plait.")
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

    req._close()


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    '''
        Route andefasany Facebook requete amntsika 
    '''

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

                senderID = message['sender']['id'] 
                if message['message'].get('quick_reply'):
                    traitement(senderID, message['message'].get('quick_reply').get('payload'))
                elif message['message'].get('text'):
                    traitement(senderID, message['message'].get('text'))
                
            # elif message.get('postback'): pass



if __name__ == '__main__':
    app.run(port=6000)
