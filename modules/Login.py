import json
from hashlib import md5
from modules.DatabaseManager import DatabaseManager
class Login:
    def __init__(self,databasecridentials, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.db = DatabaseManager(**databasecridentials)
        self.db.disconnect()
        self.loggedInMembersTable = "logged_in_members_table"
        self.loggedMembersDetailingColumns=[
            'id BIGINT AUTO_INCREMENT PRIMARY KEY',
            'username LONGTEXT',
            'sessions BIGINT',
        ]
    def doLoginTest(self):
        if self.username:
            self.db.connect()
            SigningInfoOfThisUser = self.db.get_value_row("signed_members_table", "email", self.email)
            self.db.disconnect()
            if SigningInfoOfThisUser:
                signedUsername = SigningInfoOfThisUser[0][3]
                if signedUsername == self.username:
                    encryptedPassword = md5(self.password.encode('UTF-8')).hexdigest()
                    encryptedPasswordAtServer = SigningInfoOfThisUser[0][4]
                    if encryptedPassword == encryptedPasswordAtServer:
                        return True
        return False
    def logInByUser(self):
        self.db.connect()
        if not self.db.check_table_exists(self.loggedInMembersTable):
            self.db.create_table(self.loggedInMembersTable, self.loggedMembersDetailingColumns)
        thisUserLogDetail = self.db.get_value_row(self.loggedInMembersTable, 'username', self.username)
        if thisUserLogDetail == None:
            columns = ('username', 'sessions')
            values = (self.username, 1)
            self.db.add_data(self.loggedInMembersTable,columns, values)
            self.db.disconnect()
        else:
            idOfThisUser = thisUserLogDetail[0][0]
            preSessions = thisUserLogDetail[0][2]
            currentSessionNumber = int(preSessions) + 1
            response = self.db.alter_value(self.loggedInMembersTable,'sessions', currentSessionNumber, idOfThisUser)
            self.db.disconnect()
            if response > 0:
                return [True, "Login successful", currentSessionNumber]
            else:
                return [False, "Login failed", None]
    def logOutByUser(self):
        self.db.connect()
        if not self.db.check_table_exists(self.loggedInMembersTable):
            self.db.create_table(self.loggedInMembersTable, self.loggedMembersDetailingColumns)
        thisUserLogDetail = self.db.get_value_row(self.loggedInMembersTable, 'username', self.username)
        if thisUserLogDetail == None:
            self.db.disconnect()
            return [False, "NO ANY SESSION FOUND TO LOGOUT!"]
        else:
            idOfThisUser = thisUserLogDetail[0][0]
            response = self.db.alter_value(self.loggedInMembersTable, 'sessions', 0, idOfThisUser)
            self.db.disconnect()
            if response > 0:
                return [True, "Logged out all sessions!"]
            else:
                return [False, "Something went wrong!"]
