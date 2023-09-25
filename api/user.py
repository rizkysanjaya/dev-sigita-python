from flask import Blueprint, Flask, render_template, request, redirect, url_for, make_response, jsonify
from queries import user_db, common_db
from config import SUPER_ADMIN_ROLE, ADMIN_ROLE, USER_ROLE
from queries.auth_db import token_required


user = Blueprint('user', __name__)

# User list
@user.route('/api/users', methods=['GET'])
@token_required([SUPER_ADMIN_ROLE, ADMIN_ROLE])
def getAllUser():
    data = common_db.selectAllData('users')
    
    if data != 200:
        return data  
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# User detail
@user.route('/api/users/<int:id>', methods=['GET'])
def userDetail(id):
    data = user_db.selectUser(id)

    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# User update
@user.route('/api/users/<int:id>', methods=['PUT'])
def updateUser(id):
    jsonObject = request.json

    name = jsonObject.get('name')
    nip = jsonObject.get('nip')
    role = jsonObject.get('role')
    email = jsonObject.get('email')
    wa_number = jsonObject.get('wa_number')
    status = jsonObject.get('status')

    values = [name, nip, email, role, wa_number, status]

    data = user_db.editUser(values, (id))

    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# User update without parameter
@user.route('/api/update-user', methods=['POST'])
def updateUserNoParam():
    jsonObject = request.json

    id = jsonObject.get('id')
    name = jsonObject.get('name')
    nip = jsonObject.get('nip')
    role = jsonObject.get('role')
    email = jsonObject.get('email')
    wa_number = jsonObject.get('wa_number')
    status = jsonObject.get('status')

    values = [name, nip, email, role, wa_number, status]

    data = user_db.editUser(values, (id))

    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500


# Delete user
@user.route('/api/users/<int:id>', methods=['DELETE'])
@token_required([SUPER_ADMIN_ROLE, ADMIN_ROLE])
def deleteUser(id):
    data = common_db.deleteData('users', (id))
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500
    
# Update user's FCM token
@user.route('/api/fcm', methods=['POST'])
def updateFCM():
    jsonObject = request.json

    id = jsonObject.get('id')
    fcm_token = jsonObject.get('fcm_token')

    data = user_db.updateFCMToken(id, fcm_token)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# Update avatar user by id
@user.route('/api/update-avatar/<int:id>', methods=['POST'])
def updateAvatar(id):
    avatar = request.files.get('file')

    filename = avatar.filename

    data = user_db.updateAvaUser(filename, id)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# Change password user
@user.route('/api/changepwd', methods=['POST'])
def changePass():
    jsonObject = request.json

    id = jsonObject.get('id')
    old_password = jsonObject.get('old_password')
    new_password = jsonObject.get('new_password')

    data = user_db.changePassword(id, old_password, new_password)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500


# Reset password user
@user.route('/api/resetpwd/<int:id>', methods=['POST'])
def resetPassword(id):
    data = user_db.resetUserPassword(id)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500