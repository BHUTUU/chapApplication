from modules.DatabaseManager import DatabaseManager
from modules.Login import Login

class Username:
    def __init__(self,databaseCridentials,username):
        self.databaseCridentials = databaseCridentials
        self.username = username
        self.db = DatabaseManager(**databaseCridentials)
        self.db.disconnect()
    
    def isUserAlreadyExist(self):
        self.db.connect()
        preExistingUserNames = self.db.get_value('signed_members_table', 'username')
        if preExistingUserNames:
            for user in preExistingUserNames:
                if self.username in user:
                    self.db.disconnect()
                    return True
        self.db.disconnect()
        return False
    def changeUsername(self, email, password, newUsername):
        loginClassInstance = Login(self.databaseCridentials, email, self.username, password)
        loginResponse = loginClassInstance.doLoginTest()
        if loginResponse is True:
            previousUsername = self.username
            self.username = newUsername
            newUsernameAlreadyTaken = self.isUserAlreadyExist()
            self.username = previousUsername
            if newUsernameAlreadyTaken is True:
                return [False, "Username already taken. Try another"]
            self.db.connect()
            thisUserRow = self.db.get_value_row('signed_members_table', 'email', email)
            thisUserRowId = thisUserRow[0][0]
            response=self.db.alter_value('signed_members_table','username', newUsername,thisUserRowId)
            self.db.disconnect()
            if(response>0):
                return [True, "Username changed successfully"]    
        return [False, "falied at Authentication for username change"]
