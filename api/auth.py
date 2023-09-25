from queries.auth_db import token_required
from flask import request, jsonify, Blueprint, current_app
import datetime, jwt
from datetime import timedelta, datetime
from queries import common_db, auth_db
from config import SUPER_ADMIN_ROLE, ADMIN_ROLE, USER_ROLE
# from app import app


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

        current_app.logger.debug(f'Secret Key: {current_app.config["SECRET_KEY"]}')
        user = auth_db.checkUser(nip, password)
        
        if user != 401 or user != 500:
            payload = {
                'nip': nip,
                'exp': datetime.utcnow() + timedelta(minutes=300),
                'iat': datetime.utcnow(),
                'role' : user['role']
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
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
# @token_required([SUPER_ADMIN_ROLE, ADMIN_ROLE])
def register():
    try:
        jsonObject = request.json
        nip = jsonObject.get('nip')
        name = jsonObject.get('name')
        email = jsonObject.get('email')
        wa_number = jsonObject.get('wa_number')
        role = jsonObject.get('role')

        # set default values
        password  = auth_db.generateRandomPassword()
        avatar = 'defaultAvatarUrl'
        default_pass = 1
        status_user = 1

        values = [nip, name, email, wa_number, role, password, avatar, default_pass, status_user]

        result, status_code = auth_db.addUser(values)
        return result, status_code
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500