#Inserer les données dans la base de  donnée: Il retourne le code de confirmation
from random import randint
import mysql.connector
from getUserId import getUserId
from datetime import datetime 
from requete import Requete
def insert_user(username):
	id_fb=getUserId(username)
	code = randint(1000,9999)
	date_d_inscription=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#messenger=Messenger()
	#sexe=messenger.get_gender(id_fb)

	#On la fonctionnalité n'est pas encore dispo
	sexe=1
	req =Requete()
	req.insertUser(id_fb,username,code,date_d_inscription,sexe)
	return code