# ********* SECTION IMPORTATION *******
import os
from flask import Flask, request
from threading import Thread

from scripts.sendMsg import sendMsg
from scripts.getUserId import getUserId
from conf import ITEAMS_ACCESS_TOKEN
from messenger import Messenger

# **************************************


# ********* SECTION INSTANCIATION ******

VERIFY_TOKEN = 'jedeconne'

app = Flask(__name__)
bot = Messenger(ITEAMS_ACCESS_TOKEN)

os.environ['ITEAMS_ACCESS_TOKEN'] = ITEAMS_ACCESS_TOKEN

# **************************************


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Diso ooo'


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
