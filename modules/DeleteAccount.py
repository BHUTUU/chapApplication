import json
from hashlib import md5
from modules.DatabaseManager import DatabaseManager
from modules.Login import Login

class DeleteAccount:
    def __init__(self, databasecridentials, email, username, password):
        self.databasecridentials = databasecridentials
        self.email = email
        self.username = username
        self.password = password
        self.db = DatabaseManager(**databasecridentials)
        self.encryptedPassword = md5(self.password.encode('UTF-8')).hexdigest()
        #login test [databasecridentails, email, username, password]
        #delete account
    def deleteAccount(self):
        loginClassInstance = Login(self.databasecridentials, self.email, self.username, self.password)
        loginResponse = loginClassInstance.doLoginTest()
        if loginResponse is True:
            self.db.connect()
            getSigninInfoOfUser = self.db.get_value_row('signed_members_table', 'email', self.email)
            idOfUser = getSigninInfoOfUser[0][0]
            response = self.db.delete_data('signed_members_table', 'id', idOfUser)
            self.db.disconnect()
            if response:
                return [True, "Account deleted"]
        else:
            return [False, "Invalid Account To Delete"]
        return [False, "Account Deletion Failed"]
    
