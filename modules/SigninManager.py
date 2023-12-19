import json
from hashlib import md5
from modules.DatabaseManager import DatabaseManager
from modules.UsernameManager import Username
class SigninManager:
    def __init__(self, databaseCridential,name, email, username, password, gender):
        self.name=name
        self.email=email
        self.username=username
        self.password=password
        self.gender=gender
        self.userNameClass=Username(databaseCridential, username)
        self.db=DatabaseManager(**databaseCridential)
        self.db.connect()
        self.signedMembersTable = "signed_members_table"
        self.signedMembersDetailingColumns=[
            'id BIGINT AUTO_INCREMENT PRIMARY KEY',
            'name TEXT',
            'email TEXT',
            'username LONGTEXT',
            'password LONGTEXT',
            'gender TEXT',
        ]
        if not self.db.check_table_exists(self.signedMembersTable):
            self.db.create_table(self.signedMembersTable, self.signedMembersDetailingColumns)
        self.db.disconnect()
    def doSignin(self):
        if not self.email:
            return [ False, "email is required!"]
        if not self.password:
            return [ False, "password is required!"]
        if not self.name:
            return [ False, "name is required!"]
        if not self.gender:
            return [ False, "gender is required!"]
        self.db.connect()
        preSignedMembersEmailList = self.db.get_value(self.signedMembersTable, 'email')
        # print(preSignedMembersEmailList)
        if preSignedMembersEmailList:
            for ids in preSignedMembersEmailList:
                if self.email in ids:
                    self.db.disconnect()
                    return [False, "Email already in use"]
            if self.userNameClass.isUserAlreadyExist():
                return [False, "username already taken!"]
            encryptedPassword = md5(self.password.encode('UTF-8')).hexdigest()
            columns = ('name', 'email', 'username', 'password', 'gender')
            values = (self.name, self.email, self.username, encryptedPassword, self.gender)
            self.db.add_data(self.signedMembersTable,columns, values)
            self.db.disconnect()
            return [True, "signed in Successfully"]
        else:
            encryptedPassword = md5(self.password.encode('UTF-8')).hexdigest()
            columns = ('name', 'email', 'username', 'password', 'gender')
            values = (self.name, self.email, self.username, encryptedPassword, self.gender)
            self.db.add_data(self.signedMembersTable,columns, values)
            self.db.disconnect()
            return [True, "signed in Successfully"]
        
"""
Validate username if already exists or not ---completed
"""