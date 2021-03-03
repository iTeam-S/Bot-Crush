import mysql.connector
from conf import Database


class Requete:
    def __init__(self):
        self.db = mysql.connector.connect(**Database)
        self.cursor = self.db.cursor()
    

    def getAction(self,userID):
        req = '''
            SELECT action FROM Utilisateur WHERE id = %s
        '''
        self.cursor.execute(req,(userID,))

        return self.cursor.fetchone()[0]



    def setAction(self, userID, action):
    	req = '''
    		UPDATE Utilisateur set action = %s
    		WHERE id = %s
    	'''
    	self.db.commit()


    def verifInscription(self, userID):
        req = '''
            SELECT inscrit FROM Utilisateur
            WHERE id = %s
        '''
        self.cursor.execute(req, (userID,))

        return self.cursor.fetchone()[0]


    def verifCode(self, userID, code):
        req = '''
            SELECT 1 FROM Utilisateur 
            WHERE id = %s AND code = %s
        '''
        self.cursor.execute(req, (userID,code))
        res = self.cursor.fetchall()

        return True if len(res)>0 else False


    def validerInscription(self, userID):
        req = '''
            UPDATE Utilisateur 
            SET inscrit = True, date_inscription = CURDATE()
            WHERE id = %s
        '''
        self.cursor.execute(req, (userID,))
        self.db.commit()


    def verifUtilisateur(self, userID):
        req = '''
            INSERT IGNORE INTO Utilisateur 
            (id) VALUES (%s)
        '''
        self.cursor.execute(req, (userID,))
        self.db.commit()


    def MajUtilisateur(self, userID, username, sexe):
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
        req = '''
            INSERT INTO Crush
            (recv, send) 
            VALUES
            (%s, %s)
        '''
        self.cursor.execute(req,( username_crush,ID_utilisateur))
        self.db.commit()
    

    def getNbCrush(self, ID_utilisateur):

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
        req = '''
            SELECT username_id FROM Utilisateur WHERE id=%s
        '''
        self.cursor.execute(req, (ID_utilisateur,))
        return self.cursor.fetchone()[0]
    

    def match(self, UserID):
        res = self.cursor.callproc('verification', (UserID,'@result'))
        self.cursor.execute('SELECT id, username FROM Utilisateur WHERE username_id = %s', (UserID,))
        val0 = self.cursor.fetchone()
        self.cursor.execute('SELECT id, username FROM Utilisateur WHERE id = %s', (res[1],))
        val1 = self.cursor.fetchone()
        val0, val1 = (val0[0], val1[1]), (val1[0], val0[1])
        return res, (val0, val1)

    


    def __close(self):
        self.db.close()
