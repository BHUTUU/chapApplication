from modules.DatabaseManager import DatabaseManager
from modules.Login import Login
class NameChange:
    def __init__(self, databaseCridentials,name, email, username, password):
        self.databaseCridentials = databaseCridentials
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.db = DatabaseManager(**self.databaseCridentials)
        self.tablename = "signed_members_table"
        self.db.disconnect()

    def changeName(self, newName):
        if newName == None:
            return [False, "Provide a new name!"]
        if newName == self.name:
            return [False, "New name must not be same as existing name!"]
        loginClassInstance = Login(self.databaseCridentials, self.email, self.username, self.password)
        loginResponse = loginClassInstance.doLoginTest()
        if loginResponse:
            if loginResponse is True:
                self.db.connect()
                userSignedDetails = self.db.get_value_row(self.tablename, 'email', self.email)
                idOfUser = userSignedDetails[0][0]
                nameChangeResponse = self.db.alter_value(self.tablename, 'name', newName, idOfUser)
                if nameChangeResponse:
                    if nameChangeResponse > 0:
                        self.db.disconnect()
                        return [True, "Name changed successfully"]
                return [False, "Something went wrong during name change! Try again later!!"]
        else:
            return [False, "Authentication Failed, Please try again with correct credentials!"]
        
