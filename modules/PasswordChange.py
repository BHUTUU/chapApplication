from  modules.DatabaseManager import DatabaseManager
from modules.Login import Login
from hashlib import md5
class PasswordChange:
    def __init__(self, databasecridentials, email, username, password):
        self.databasecridentials = databasecridentials
        self.email = email
        self.username = username
        self.password = password
        self.db=DatabaseManager(**self.databasecridentials)
        self.tablename = "signed_members_table"
        self.db.disconnect()
    def setNewPassword(self, newPassword):
        if newPassword:
            if newPassword != self.password:
                pass
            else:
                return [False, "New password must be different form the old password"]
        else:
            return [False, "You must provide the new password that you want to set!. Try again!!"]
        loginClassInstance = Login(self.databasecridentials, self.email, self.username, self.password)
        loginResponse = loginClassInstance.doLoginTest()
        if loginResponse is True:
            self.db.connect()
            thisUserInfo = self.db.get_value_row(self.tablename, 'email', self.email)
            idOfThisUser = thisUserInfo[0][0]
            encryptedPassword = md5(newPassword.encode('UTF-8')).hexdigest()
            changeResponse = self.db.alter_value(self.tablename, 'password', encryptedPassword, idOfThisUser)
            if changeResponse:
                if changeResponse > 0:
                    self.db.disconnect()
                    return [True, "Password Changed successfully!!"]
            return [False, "Somewhere went wrong. Try again"]
        else:
            return [False, "Authentication Failed, Please try again with correct credentials!"]