from flask import Blueprint, request, jsonify
from queries import user_db, common_db
from queries.auth_db import token_required
from flask import current_app as app
from werkzeug.utils import secure_filename
import os, time

user = Blueprint('user', __name__)

# User list
@user.route('/api/users', methods=['GET'])
@token_required
def getAllUser():
    data = common_db.selectAllData('users')
    
    if data != 200:
        return data  
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# User detail
@user.route('/api/users/<int:id>', methods=['GET'])
@token_required
def userDetail(id):
    data = user_db.selectUser(id)

    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# User update
@user.route('/api/users/<int:id>', methods=['PUT'])
@token_required
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
@token_required
def updateUserNoParam(current_user):
    try:
        app.logger.debug(f'Current user role: {current_user.get("role")}')

        user_role = current_user.get('role')

        jsonObject = request.json

        id = jsonObject.get('id')
        name = jsonObject.get('name')
        nip = jsonObject.get('nip')
        role = jsonObject.get('role')
        email = jsonObject.get('email')
        wa_number = jsonObject.get('wa_number')
        status = jsonObject.get('status')

        # Check if the user has the privilege to register the specified role
        # if auth_db.check_authorization(user_role, role):

        values = [name, nip, email, role, wa_number, status]

        data = user_db.editUser(values, (id))

        if data != 200:
            return data
        else:
            return jsonify({"message": "Kesalahan pada server."}), 500
        # else:
        #     # User doesn't have the privilege to register this role
        #     return jsonify({"message": "Otorisasi Gagal. Anda tidak bisa mendaftarkan user dengan kredensial ini.",
        #                     "Error" : "Wrong role credentials."}), 403
        
            
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500


# Delete user
@user.route('/api/users/<int:id>', methods=['DELETE'])
@token_required
def deleteUser(id):
    data = common_db.deleteData('users', (id))
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500
    
# Update user's FCM token
@user.route('/api/fcm', methods=['POST'])
@token_required
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
@token_required
def updateAvatar(id):
    avatar = request.files.get('file')

    filename = secure_filename(avatar.filename)
    timestamp = int(time.time())  # Get current timestamp
    filename, file_extension = os.path.splitext(filename)
    unique_filename = f"{filename}_{timestamp}{file_extension}"
    file_path = os.path.join(app.config['AVATAR_FOLDER'], unique_filename)
    avatar.save(file_path)


    data = user_db.updateAvaUser(unique_filename, id)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# Change password user
@user.route('/api/changepwd', methods=['POST'])
@token_required
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
@token_required
def resetPassword(id):
    data = user_db.resetUserPassword(id)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500