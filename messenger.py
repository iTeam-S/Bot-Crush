import requests



class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"


    def send_message_text(self, destId, message, prio=False):
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