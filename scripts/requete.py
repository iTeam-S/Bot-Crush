import mysql.connector

from conf import Database
class Requete:
    def __init__(self):
        self.db = mysql.connector.connect(**Database)
        self.cursor = self.db.cursor()
    def getAction(self,userID):
        req = '''
            SELECT statut FROM Action WHERE id_fb = %s
        '''
        self.cursor.execute(req,(userID,))

        return self.cursor.fetchone()[0]


    def setAction(self, userID, statut):
    	req = '''
    		UPDATE Action set statut = %s
    		WHERE id_fb = %s
    	'''
    	self.cursor.execute(req, (statut, userID))
    	self.db.commit()
    def insertUser(self,id_fb,username,code,date_d_inscription,sexe):
        req_sql='''
                INSERT INTO 
                Utilisateur (id_fb,username_profile,code,date_inscription,sexe_utilisateur) 
                VALUES (%s,%s,%s,%s,%s)
            '''
        self.cursor.execute(req_sql,(id_fb,username,code,date_d_inscription,sexe))
        self.db.commit()
    def __close(self):
        self.db.close()