from queries.auth_db import token_required
from flask import request, jsonify, Blueprint
from flask import current_app as app
import datetime, jwt, psycopg2
from datetime import timedelta, datetime
from queries import auth_db
from  werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

    
# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG)
    
# Login page
@auth.route('/api/login', methods=['POST'])
def login():    
        # creates dictionary of form data
        # Parse JSON data from the request body
        jsonObject = request.json
        nip = jsonObject.get('nip')
        password = jsonObject.get('password')
        platform = jsonObject.get('platform')
        time_zone = jsonObject.get('time_zone')

        # app.logger.debug(f'Secret Key: {app.config["SECRET_KEY"]}')
        user = auth_db.checkUser(nip)
        app.logger.debug(f'User: {user}')
        
        if user is not None and 'password' in user and check_password_hash(user['password'], password):
            # Create a token
            payload = {
                'nip': nip,
                'exp': datetime.utcnow() + timedelta(minutes=300),
                'iat': datetime.utcnow(),
                'role' : user['role']
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'token': token,
                            'status': 200,
                            'WWW-Authenticate': 'Otentikasi Berhasil!'
                            }), 200
        else:
            return jsonify({
                            'message': 'Otentikasi Gagal!',
                            'status': 401,
                            'WWW-Authenticate': 'Kredensial salah. Cek kembali akun Anda!'
                            }), 401


# Register
@auth.route('/api/register', methods=['POST'])
@token_required
def register(current_user):
    try:

        # Check the role of the user making the request
        app.logger.debug(f'Current user role: {current_user.get("role")}')
        user_role = current_user.get('role')

        jsonObject = request.json
        nip = jsonObject.get('nip')
        name = jsonObject.get('name')
        email = jsonObject.get('email')
        wa_number = jsonObject.get('wa_number')
        role = jsonObject.get('role')

        # Check if the user has the privilege to register the specified role
        # if auth_db.check_authorization(user_role, role):
            # User has the privilege to register this role
        random_password = auth_db.generateRandomPassword()
        password = generate_password_hash(random_password, method='pbkdf2:sha256')
        avatar = 'defaultAvatarUrl'
        default_pass = 1
        status_user = 1

        values = [nip, name, email, wa_number, role, password, avatar, default_pass, status_user, random_password]

        result, status_code = auth_db.addUser(values)
        return result, status_code
        # else:
        #     # User doesn't have the privilege to register this role
        #     return jsonify({"message": "Otorisasi Gagal. Anda tidak bisa mendaftarkan user dengan kredensial ini.",
        #                     "Error" : "Wrong role credentials."}), 403
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500