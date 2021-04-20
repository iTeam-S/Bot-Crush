import mysql.connector
from conf import Database


class Requete:
	def __init__(self):
		self.db = mysql.connector.connect(**Database)
		self.cursor = self.db.cursor()

	def __verif(self):
		if not self.db.is_connected():
			self.db.reconnect()

	def getAction(self, userID):
		self.__verif()
		req = '''
		    SELECT action FROM Utilisateur WHERE id = %s
		'''
		self.cursor.execute(req, (userID,))

		return self.cursor.fetchone()[0]



	def setAction(self, userID, action):
		self.__verif()
		req = '''
			UPDATE Utilisateur set action = %s
			WHERE id = %s
		'''
		self.cursor.execute(req, (action, userID))
		self.db.commit()


	def verifInscription(self, userID):
		self.__verif()
		req = '''
		    SELECT inscrit FROM Utilisateur
		    WHERE id = %s
		'''
		self.cursor.execute(req, (userID,))

		return self.cursor.fetchone()[0]


	def verifCode(self, userID, code):
		self.__verif()
		req = '''
		    SELECT 1 FROM Utilisateur 
		    WHERE id = %s AND code = %s
		'''
		self.cursor.execute(req, (userID,code))
		res = self.cursor.fetchall()

		return True if len(res)>0 else False


	def validerInscription(self, userID):
		self.__verif()
		req = '''
		    UPDATE Utilisateur 
		    SET inscrit = True, date_inscription = CURDATE()
		    WHERE id = %s
		'''
		self.cursor.execute(req, (userID,))
		self.db.commit()


	def verifUtilisateur(self, userID):
		self.__verif()
		req = '''
		    INSERT IGNORE INTO Utilisateur 
		    (id) VALUES (%s)
		'''
		self.cursor.execute(req, (userID,))
		self.db.commit()


	def MajUtilisateur(self, userID, username, sexe):
		self.__verif()
		req = '''
		    UPDATE Utilisateur
		    SET username = %s,
		        date_inscription = CURDATE(),
		        sexe = %s 
		    WHERE 
		        id = %s
		'''
		self.cursor.execute(req,(username,sexe,userID))
		self.db.commit()


	def updateCode(self, userID, username, code,id_username,sexe):
		self.__verif()
		req = '''
		    UPDATE Utilisateur
		        SET code = %s,
		         username = %s,
		         username_id = %s,
		         date_inscription = CURDATE(),
		         sexe=%s
		    WHERE id = %s
		'''
		self.cursor.execute(req, (code, username,id_username, sexe, userID))
		self.db.commit()



	def ajoutCrush(self, username_crush, ID_utilisateur):
		self.__verif()
		req = '''
		    INSERT INTO Crush
		    (recv, send) 
		    VALUES
		    (%s, %s)
		'''
		self.cursor.execute(req, (username_crush, ID_utilisateur))
		self.db.commit()
    

	def getNbCrush(self, ID_utilisateur):
		self.__verif()
		req = '''
		    SELECT COUNT(*) AS nb_crush
		    FROM Crush
		    WHERE send = %s
		    AND MONTH(date) = MONTH(CURDATE())
		    AND YEAR(date) = YEAR(CURDATE())
		'''
		self.cursor.execute(req, (ID_utilisateur,))
		return self.cursor.fetchone()[0]
    

	def getUserID(self, ID_utilisateur):
		self.__verif()
		req = '''
		    SELECT username_id FROM Utilisateur WHERE id=%s
		'''
		self.cursor.execute(req, (ID_utilisateur,))
		return self.cursor.fetchone()[0]
	

	def setUserID(self, fbID, userPageID):
		self.__verif()
		req = '''
		    UPDATE Utilisateur SET username_id = %s WHERE id=%s
		'''
		self.cursor.execute(req, (fbID, userPageID))
		self.db.commit()


	def getUserName(self, ID_utilisateur):
		self.__verif()
		req = '''
		    SELECT username FROM Utilisateur WHERE id=%s
		'''
		self.cursor.execute(req, (ID_utilisateur,))
		return self.cursor.fetchone()[0]
    

	def match(self, UserID):
		self.__verif()
		res = self.cursor.callproc('verification', (UserID,'@result'))
		if not res[1]: return res, None
		self.cursor.execute('SELECT id, username FROM Utilisateur WHERE username_id = %s', (UserID,))
		val0 = self.cursor.fetchone()
		self.cursor.execute('SELECT id, username FROM Utilisateur WHERE id = %s', (res[1],))
		val1 = self.cursor.fetchone()
		val0, val1 = (val0[0], val1[1]), (val1[0], val0[1])
		return res, (val0, val1)


	def insertTache (self,types, user, texte = " ", donnee=None):
		self.__verif()
		req = '''
		    INSERT  INTO Tache
		    	(idType, idUser, texte, donnee)
		    VALUES 
		    	(%s, %s, %s, %s)
		'''
		self.cursor.execute(req, (types, user, texte, donnee))
		self.db.commit()  


	def getTaches(self):
		self.__verif()
		req = '''
			SELECT id, idType, idUser, texte, donnee
			FROM Tache WHERE fini = 0 ORDER BY date
		'''   
		self.cursor.execute(req, ())        
		return self.cursor.fetchall() 	
		

	def updateFinishJob(self, idtache):
		self.__verif()
		req = '''
			UPDATE Tache Set fini = 1 
			WHERE id = %s
		'''
		self.cursor.execute(req, (idtache, ))
		self.db.commit()
	

	def updateNotif(self, user0, user1):
		self.__verif()
		req = '''
			UPDATE Crush Set notification = 1 
			WHERE ( recv = SHA2(%s, 224) AND send = SHA2(%s, 224) )
			OR ( recv = SHA2(%s, 224) AND send = SHA2(%s, 224) )
		'''
		self.cursor.execute(req, 
			(self.getUserID(user0), user1, self.getUserID(user1), user0)
		)
		self.db.commit()
		

	def _close(self):
		self.db.close()




