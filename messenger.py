import requests

class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"


    def send_message(self, destId, message, prio=False):
        '''
            Cette fonction sert à envoyer une message texte
                à l'utilisateur en vue de répondre à un message
                                                                '''
        dataJSON = {
            'recipient':{
                "id": destId
            },

            'message':{
                "text": message
            }
        }

        if prio:
            dataJSON["messaging_type"] = "MESSAGE_TAG"
            dataJSON["tag"] = "ACCOUNT_UPDATE"

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)
    

    def send_action(self, destId, action):
        '''
            action doit etre un des suivants ['mark_seen', 'typing_on', 'typing_off']
        '''
        if action not in ['mark_seen', 'typing_on', 'typing_off']:
            return None

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient':{
                "id": destId
            },

            'sender_action': action
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)
    

    def send_quick_reply(self, destId, **kwargs):
        if kwargs.get('MENU_PRINCIPALE'):
            text = 'Quelle action voulez-vous faire?'
            if kwargs.get('INSCRIPTION'):
                quick_rep = [
                    {
                        "content_type":"text",
                        "title":"Nouveau Crush",
                        "payload":"_AJOUTER",
                        "image_url": "https://img.icons8.com/fluent/48/26e07f/heart-plus.png"
                    }
                ]
            else:
                quick_rep= [
                    {
                        "content_type":"text",
                        "title":"Inscription",
                        "payload":"_INSCRIPTION",
                        "image_url": "https://img.icons8.com/fluent/48/26e07f/inscription.png"
                    }
                ]
        elif kwargs.get('MENU_INSCRIPTION'):
            text = 'voulez-vous faire ...'
            quick_rep = [
                {
                    "content_type":"text",
                    "title":"Nouvelle inscription",
                    "payload":"_INSCRIPTION_NOUVEAU",
                    "image_url": "https://img.icons8.com/flat_round/64/26e07f/plus.png"
                },
                {
                    "content_type":"text",
                    "title":"Valider inscription",
                    "payload":"_INSCRIPTION_VALIDER",
                    "image_url": "https://img.icons8.com/wired/64/26e07f/check-all.png"
                }
            ]

        else:
            return 

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient':{
                "id": destId
            },

            'message': {
                'text' : text,
                'quick_replies': quick_rep
            }
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)

    def get_gender(self,userID):

        links="https://graph.facebook.com/"+userID+"?fields=gender&access_token="+self.token
        request=requests.get(links)

        sex= request.json()["gender"]

        if sex=="male":
            gender=1

        else:
            gender=0
        
        return gender



