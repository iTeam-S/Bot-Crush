from random import randint
import mysql.connector
from getUserId import getUserId
from datetime import datetime 
import os
'''
Les variables d'environnment nécessaire: Page acces token,host,user_name, password.
'''


#Récuperer le genre de l'utilisateur
def get_gender(userID):
    gender=1
    PAGE_ACCESS_TOKEN=os.environ.get("PAGE_ACCESS_TOKEN")
    links="https://graph.facebook.com/"+userID+"?fields=gender&access_token="+PAGE_ACCESS_TOKEN
    return gender

#connexion au base de données
def connexion_db():
	
    db = mysql.connector.connect(
        host = os.environ.get("HOST"),
        user = os.environ.get("ITEAMS_USER"),
        password =os.environ.get("ITEAMS_PASSWORD"),
        database="bot_crush"
    )
    return db

#generer le code de confirmation
def generate_code():
    return randint(1000,9999)

#Inserer les données dans la base de  donnée: Il retourne false s'il a pas réussi.
def insert_user(username):
    bdd=connexion_db()
    curseur=bdd.cursor()
    id_fb=getUserId(username)
    code = generate_code()
    date_d_inscription=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sexe=get_gender(id_fb)
    #requête:
    req_sql="INSERT INTO Utilisateur (id_fb,username_profile,code,date_inscription,sexe_utilisateur) VALUES (%s,%s,%s,%s,%s);"
    values=(id_fb,username,code,date_d_inscription,sexe)
    try:
        curseur.execute(req_sql,values)
        bdd.commit()
        return code
    except mysql.connector.Error as err:
        print (err)
        return False
    finally:
        curseur.close()
        bdd.close()



