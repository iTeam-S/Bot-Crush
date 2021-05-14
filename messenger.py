import requests


class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"

    def send_message(self, dest_id, message, prio=False):
        """
            Cette fonction sert à envoyer une message texte
                à l'utilisateur en vue de répondre à un message
                                                                """
        data_json = {
            'recipient': {
                "id": dest_id
            },

            'message': {
                "text": message
            }
        }

        if prio:
            data_json["messaging_type"] = "MESSAGE_TAG"
            data_json["tag"] = "ACCOUNT_UPDATE"

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(self.url + '/messages', json=data_json, headers=header, params=params)

    def send_action(self, dest_id, action):
        """
            action doit etre un des suivants ['mark_seen', 'typing_on', 'typing_off']
        """
        if action not in ['mark_seen', 'typing_on', 'typing_off']:
            return None

        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },

            'sender_action': action
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(self.url + '/messages', json=data_json, headers= header, params=params)

    def send_quick_reply(self, dest_id, **kwargs):
        if kwargs.get('MENU_PRINCIPALE'):
            text = 'Quelle action voulez-vous faire?'
            if kwargs.get('INSCRIPTION'):
                quick_rep = [
                    {
                        "content_type": "text",
                        "title": "Nouveau Crush",
                        "payload": "_AJOUTER",
                        "image_url": "https://img.icons8.com/fluent/48/26e07f/heart-plus.png"
                    }
                ]
            else:
                quick_rep = [
                    {
                        "content_type": "text",
                        "title": "Inscription",
                        "payload": "_INSCRIPTION",
                        "image_url": "https://img.icons8.com/fluent/48/26e07f/inscription.png"
                    }
                ]
        elif kwargs.get('MENU_INSCRIPTION'):
            text = 'voulez-vous faire ...'
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Nouvelle inscription",
                    "payload": "_INSCRIPTION_NOUVEAU",
                    "image_url": "https://img.icons8.com/flat_round/64/26e07f/plus.png"
                },
                {
                    "content_type": "text",
                    "title": "Entrer Code",
                    "payload": "_INSCRIPTION_VALIDER",
                    "image_url": "https://img.icons8.com/wired/64/26e07f/check-all.png"
                }
            ]
        elif kwargs.get('LIEN_PROFIL'):
            text = 'Avez-vous accepter notre demande?'
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Oui",
                    "payload": kwargs.get('LIEN_PROFIL'),
                    "image_url": "https://img.icons8.com/flat_round/64/26e07f/plus.png"
                },
                {
                    "content_type": "text",
                    "title": "Non",
                    "payload": "DEMANDE_REJETER",
                    "image_url": "https://img.icons8.com/wired/64/26e07f/check-all.png"
                }
            ]
        elif kwargs.get('TEXTE_PERSONNALISER') and kwargs.get('USERNAME') : 
            text = "Vous voulez un texte personnalisé."
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Non",
                    "payload": "_TEXTE_PERSONNALISER_OUI" + "***" + kwargs.get('TEXTE_PERSONNALISER') + "***" + kwargs.get('USERNAME'),
                    "image_url": "https://img.icons8.com/flat_round/64/26e07f/plus.png"
                },
                {
                    "content_type": "text",
                    "title": "Oui",
                    "payload": "_TEXTE_PERSONNALISER_OUI" + "***" + kwargs.get('TEXTE_PERSONNALISER')+"***"+ kwargs.get('USERNAME') ,
                    "image_url": "https://img.icons8.com/wired/64/26e07f/check-all.png"
                }
            ] 


        else:
            return

        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },

            'message': {
                'text': text,
                'quick_replies': quick_rep
            }
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(self.url + '/messages', json=data_json, headers=header, params=params)

    def get_gender(self, user_id):

        links = "https://graph.facebook.com/" + user_id + "?fields=gender&access_token=" + self.token
        request = requests.get(links)

        sex = request.json().get("gender")

        if sex == "male":
            gender = 1
        elif sex == "female":
            gender = 0
        else:
            gender = None

        return gender
