from flask import *
from waitress import serve
import json
from flask_cors import CORS
from modules.DatabaseManager import DatabaseManager
from modules.SigninManager import SigninManager
from modules.UsernameManager import Username
from modules.Login import Login
from modules.DeleteAccount import DeleteAccount
from modules.PasswordChange import PasswordChange
from modules.NameChange import NameChange
from modules.GenderChange import GenderChange
from modules.EmailChange import EmailChange
from modules.FindUser import FindUser
app = Flask(__name__)
CORS(app)
#<<<-------Database connection------->>>
with open("config.json", 'r') as config_file:
    jsonContent = json.load(config_file)
    config_file.close()
databaseCridential=jsonContent["mysql"][0]
db=DatabaseManager(**databaseCridential)
if not db.check_database_exists():
    db.create_database()
db.disconnect()
# <<<-------Application Routes ---------->>
@app.route('/', methods=['GET'])
def home_page():
    response = '{ "status": 200 }'
    jsonResponse = json.loads(response)
    return jsonResponse
@app.route('/signin', methods=['POST'])
def signin():
    global databaseCridential
    name = request.args.get('name')
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    gender = request.args.get('gender')
    signer = SigninManager(databaseCridential, name, email, username, password,gender)
    response = signer.doSignin()
    if response[0] is True:
        return '{"Status": "Successful", "Response": \"' + response[1] + '\" }'
    else:
        return '{"Status": "Failed", "Response": \"' + response[1] + '\" }'
@app.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    global databaseCridential
    email = request.args.get('email')
    password = request.args.get('password')
    username = request.args.get('username')
    deleteAccountInstance = DeleteAccount(databaseCridential, email, username, password)
    response=deleteAccountInstance.deleteAccount()
    return '{"status": "'+str(response[0])+'",'+' "Response": "'+response[1]+'"}'
@app.route('/login', methods=['GET', 'POST'])
def login():
    global databaseCridential
    email = request.args.get('email')
    password = request.args.get('password')
    username = request.args.get('username')
    loginObj = Login(databaseCridential, email, username, password)
    response=loginObj.logInByUser()
    if response[0] is True:
        return '{"status": "Successfull",'+' "Response": \"'+str(response[1])+'\", "sessions": '+str(response[2])+'}'
    else:
        return '{"status": "Failed",'+' "Response": \"'+str(response[1])+'\", "sessions": \"'+str(response[2])+'\"}'

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global databaseCridential
    email = request.args.get('email')
    password = request.args.get('password')
    username = request.args.get('username')
    loginObj = Login(databaseCridential, email, username, password)
    response=loginObj.logOutByUser()
    if response[0] is True:
        return '{"status": "Successfull",'+' "Response": \"'+str(response[1])+'\"}'
    else:
        return '{"status": "Failed",'+' "Response": \"'+str(response[1])+'\"}'

@app.route('/changeUsername', methods=['PUT'])
def changeUsername():
    global databaseCridential
    email = request.args.get('email')
    password = request.args.get('password')
    username = request.args.get('username')
    newUsername = request.args.get('new_username')
    if not email:
        return '{"Status": "Failed", "Response": "email is required"}'
    if not password:
        return '{"Status": "Failed", "Response": "password is required"}'
    if not username:
        return '{"Status": "Failed", "Response": "username is required"}'
    if not newUsername:
        return '{"Status": "Failed", "Response": "new_username is required"}'
    usernameClassInstance = Username(databaseCridential, username)
    response = usernameClassInstance.changeUsername(email, password, newUsername)
    return '{"Status": \"'+str(response[0])+'\", "Response": \"'+response[1]+'\"}'
@app.route('/changePassword', methods=['PUT'])
def changePassword():
    global databaseCridential
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    newPassword = request.args.get('new_password')
    passwordChangeClassInstance = PasswordChange(databaseCridential, email, username, password)
    response = passwordChangeClassInstance.setNewPassword(newPassword)
    if response:
        if response[0] is True:
            return '{"Status": "Successful", "Response": \"'+response[1]+'\"}'
        else:
            return '{"Status": "Failed", "Response": \"'+response[1]+'\"}'
    else:
        return '{"Status": "Failed", "Response": "Something went wrong, try again later."}'
@app.route('/changeName', methods=['PUT'])
def changeName():
    global databaseCridential
    name = request.args.get('name')
    newName = request.args.get('new_name')
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    nameChangeClassInstance = NameChange(databaseCridential, name, email, username, password)
    response = nameChangeClassInstance.changeName(newName)
    if response:
        if response[0] is True:
            return '{"Status": "Successful", "Response": \"'+response[1]+'\"}'
        else:
            return '{"Status": "Failed", "Response": \"'+response[1]+'\"}'
    else:
        return '{"Status": "Failed", "Response": "Something went wrong, try again later."}'
@app.route('/changeGender', methods=['PUT'])
def changeGender():
    global databaseCridential
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    gender = request.args.get('gender')
    newGender = request.args.get('new_gender')
    genderChangeClassInstance = GenderChange(databaseCridential, email, username, password)
    response = genderChangeClassInstance.changeGender(newGender)
    if response:
        if response[0] is True:
            return '{"Status": "Successful", "Response": \"'+response[1]+'\"}'
        else:
            return '{"Status": "Failed", "Response": \"'+response[1]+'\"}'
    else:
        return '{"Status": "Failed", "Response": "Something went wrong, try again later."}'
@app.route('/changeEmail', methods=['PUT'])
def changeEmail():
    global databaseCridential
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    newEmail = request.args.get('new_email')
    emailChangeClassInstance = EmailChange(databaseCridential, email, username, password)
    response = emailChangeClassInstance.changeEmail(newEmail)
    if response:
        if response[0] is True:
            return '{"Status": "Successful", "Response": \"'+response[1]+'\"}'
        else:
            return '{"Status": "Failed", "Response": \"'+response[1]+'\"}'
    else:
        return '{"Status": "Failed", "Response": "Something went wrong, try again later."}'
@app.route('/findUserByEmail', methods=['GET'])
def findUserByEmail():
    global databaseCridential
    emailTOFind = request.args.get('email')
    response = FindUser.byEmail(databaseCridential, emailTOFind)
    if response[0] is True:
        return '{"Status": "Successful", "Response": ['+str(response[1])+']}'
    else:
        return '{"Status": "Failed", "Response": ['+str(response[1])+']}'
@app.route('/findUserByUsername', methods=['GET'])
def findUserByUsername():
    global databaseCridential
    usernameTOFind = request.args.get('username')
    response = FindUser.byUsername(databaseCridential, usernameTOFind)
    if response[0] is True:
        return '{"Status": "Successful", "Response": ['+str(response[1])+']}'
    else:
        return '{"Status": "Failed", "Response": ['+str(response[1])+']}'
if __name__ == '__main__':
    print("Server started on Host: 127.0.0.1 port: 8080")
    serve(app,host="127.0.0.1", port=8080)