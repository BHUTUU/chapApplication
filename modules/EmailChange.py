from modules.DatabaseManager import DatabaseManager
from modules.Login import Login
import re, requests

class EmailChange:
    @staticmethod
    def validateEmail(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):
            try:
                resp = requests.get("https://ssl-checker.io/api/v1/check/"+email.split('@')[1], timeout=4)
                jsonResponse = resp.json()
                status = jsonResponse["status"]
                # print(status)
                if status == 'ok':
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False
    def __init__(self, databasecridentials,email, username, password):
        self.databasecridentials = databasecridentials
        self.email = email
        self.username = username
        self.password = password
        self.tablename = 'signed_members_table'
        self.db = DatabaseManager(**databasecridentials)
        self.db.disconnect()
    def changeEmail(self, newEmail):
        loginClassInstance = Login(self.databasecridentials,self.email, self.username, self.password)
        loginResponse=loginClassInstance.doLoginTest()
        if loginResponse:
            if not EmailChange.validateEmail(newEmail):
                return [False, "This Email is not a valid email!"]
            if not newEmail:
                return [False, "You must provide a new email!"]
            self.db.connect()
            getUserSignedInfo = self.db.get_value_row(self.tablename, 'email', self.email)
            preEmailOfThisUser = getUserSignedInfo[0][2]
            if newEmail == preEmailOfThisUser:
                return [False, "New email must be different from current to change!"]
            idOfThisUser = getUserSignedInfo[0][0]
            numOfRowAffected = self.db.alter_value(self.tablename, 'email', newEmail, idOfThisUser)
            if numOfRowAffected:
                if numOfRowAffected>0:
                    return [True, "Email is changed Successfully"]
            else:
                return [True, "Something went wrong. try again!"]
        else:
            return [False, "Authentication failed for this request!"]