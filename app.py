from flask import Flask 
from scripts.sendMsg import sendMsg
from scripts.getUserId import getUserId


app = Flask(__name__)


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


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
        body = request.get_json()
        print(body)

    return "Voray ry Facebook fa Misoatra a!", 200



if __name__ == '__main__':
    app.run()