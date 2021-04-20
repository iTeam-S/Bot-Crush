import os, time, json

from scripts.utils import *
from scripts.requete import Requete
from scripts.browser import WebBrowser
from scripts.sendMsg import sendMsg
from scripts.delMsg import delMsg
from scripts.getUserId import getUserId

from messenger import Messenger

from conf import ITEAMS_ACCESS_TOKEN
from conf import ITEAMS_LOGIN, ITEAMS_PASS


os.environ['ITEAMS_ACCESS_TOKEN'] = ITEAMS_ACCESS_TOKEN
os.environ['ITEAMS_LOGIN'] = ITEAMS_LOGIN
os.environ['ITEAMS_PASS'] = ITEAMS_PASS


def tache1(data):
	try:
		delMsg(driver.browser, req.getUserID(data[2]))
	except Exception as err:
		print(err)
		
	username_crush = decode(json.loads(data[-1]).get('username_crush'))
	crushId = getUserId(username_crush, driver)
	if not crushId:
		bot.send_action(data[2], 'mark_seen')
		bot.send_action(data[2], 'typing_on')
		bot.send_message(data[2], "❌Votre lien semble incorrect :-/")
		bot.send_action(data[2], 'typing_off')
		req.updateFinishJob(data[0])
		return
	try:
		sendMsg(driver.browser, crushId, data[3])
		req.ajoutCrush(encrypt(crushId), encrypt(data[2]))
		bot.send_action(data[2], 'mark_seen')
		bot.send_action(data[2], 'typing_on')
		bot.send_message(data[2], "✔Votre crush a été bien enregistrer. \n Merci pour votre confiance.")
		req.setAction(data[2], None)

	except Exception as err:
		print(err)     
		bot.send_message(data[2], "❌❌❌Oh, une erreur s'est produite :-/")
		return
	
	nb_crush = req.getNbCrush(encrypt(data[2]))

	if 3 - nb_crush == 0:
		reponse = "🙄🙄Vous avez atteint le nombre limite de crushs pour ce mois. Revenez le mois prochain"
	else :
		if (3 - nb_crush) > 1:
			reponse = "Vous pouvez encore crusher sur "+ str (3 - nb_crush) +" personnes pendant ce mois."
		else:
			reponse = "Vous pouvez encore crusher sur "+ str (3 - nb_crush) +" personne pendant ce mois."

	bot.send_message(data[2], reponse)        
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
			bot.send_message(v[0], msg, prio=0==i)
			bot.send_action(v[0],'typing_off')
			i += 1
		req.updateNotif(val[0][0], val[1][0])
	req.updateFinishJob(data[0])


	
def tache2(data):
	pass


def tache3(data): 
	username = req.getUserName(data[2])
	userId = getUserId(username, driver)
	print(userId)
	if not userId:
		bot.send_action(data[2], 'mark_seen')
		bot.send_action(data[2], 'typing_on')
		bot.send_message(data[2], "❌Votre Lien semble incorrecte :-/")
		bot.send_action(data[2], 'typing_off')
		req.setAction(data[2], None)
		req.updateFinishJob(data[0])
		return
	sexe = bot.get_gender(data[2])
	try:
		sendMsg(driver.browser, userId, data[3])
		print("sa aty?")
		req.setUserID(userId, data[2])
		bot.send_action(data[2], 'mark_seen')
		bot.send_action(data[2], 'typing_on')
		bot.send_message(data[2], "Verifier vos messages, votre code a été envoyé :-)")
		req.setAction(data[2], 'ATTENTE_CODE_CONFIRMATION')
		bot.send_message(data[2], "Veuillez saisir votre code de confirmation")
	except Exception as err:
		print(err)     
		#bot.send_message(data[2], "❌❌❌Oh, une erreur s'est produite :-/")
		return
	req.updateFinishJob(data[0])


if __name__ == '__main__':
	driver  =  WebBrowser()
	connexion(driver.browser)
	req = Requete()
	bot = Messenger(ITEAMS_ACCESS_TOKEN)

	while True:
		req = Requete()
		taches = req.getTaches()
		print(taches)
		for tch in taches:
			if tch[1] == 1: tache1(tch) 
			elif tch[1] == 2: tache2(tch)
			elif tch[1] == 3: tache3(tch)
			time.sleep(5)
		req._close()
		time.sleep(10)

	
