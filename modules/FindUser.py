from modules.DatabaseManager import DatabaseManager

class FindUser:
    @classmethod
    def byEmail(cls,databasCridentials, email):
        db = DatabaseManager(**databasCridentials)
        response = db.get_value_row('signed_members_table', 'email', email)
        db.disconnect()
        if response and response is not None:
            name=response[0][1]
            email=response[0][2]
            username=response[0][3]
            sexuality=response[0][5]
            data = '{"name": \"'+ name +'\","email": \"'+ email +'\","username": \"'+ username + '\", "sex": \"' + sexuality + '\"}'
            return [True, data]
        else:
            return [False, "User not found"]
    @classmethod
    def byUsername(cls, databasCridentials, username):
        db = DatabaseManager(**databasCridentials)
        response = db.get_value_row('signed_members_table', 'username', username)
        db.disconnect()
        if response and response is not None:
            name=response[0][1]
            email=response[0][2]
            username=response[0][3]
            sexuality=response[0][5]
            data = '{"name": \"'+ name +'\","email": \"'+ email +'\","username": \"'+ username + '\", "sex": \"' + sexuality + '\"}'
            return [True, data]
        else:
            return [False, "User not found"]
        