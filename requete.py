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


    def __close(self):
        self.db.close()