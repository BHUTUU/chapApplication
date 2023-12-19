from modules.DatabaseManager import DatabaseManager
from modules.Login import Login

class GenderChange:
    @staticmethod
    def validateGender(gender):
        genderList = ["male", "female", "transgender", "lesbian", "gay", "bisexual", "queer", "intersex", "asexual", "other"]
        if gender:
            if gender in genderList:
                return [True, gender]
            else:
                return [False, "Not a valid gender"]
        else:
            return [False, "Empty"]
        
    def __init__(self, databaseCridentials, email, username, password):
        self.databaseCridentials = databaseCridentials
        self.email = email
        self.username = username
        self.password = password
        self.db = DatabaseManager(**self.databaseCridentials)
        self.tablename = "signed_members_table"
        self.db.disconnect()
    def changeGender(self, newGender):
        loginClassInstance = Login(self.databaseCridentials, self.email, self.username, self.password)
        loginResponse=loginClassInstance.doLoginTest()
        if loginResponse:
            validGenderResponse = GenderChange.validateGender(newGender.lower())
            if validGenderResponse[0] is True:
                self.db.connect()
                getUserSignedInfo = self.db.get_value_row(self.tablename, 'email', self.email)
                preGenderOfThisUser = getUserSignedInfo[0][5]
                if newGender.lower() == preGenderOfThisUser.lower():
                    return [False, "New gender must be different from current to change!"]
                idOfThisUser = getUserSignedInfo[0][0]
                numOfRowAffected = self.db.alter_value(self.tablename, 'gender', validGenderResponse[1], idOfThisUser)
                if numOfRowAffected:
                    if numOfRowAffected>0:
                        return [True, "Gender is changed Successfully"]
                    else:
                        return [True, "Something went wrong. try again!"]
            else:
                return [False, "Please specify a valid gender"]
        else:
            return [False, "Authentication failed for this request!"]