from queries.auth_db import token_required
from flask import request, jsonify, Blueprint, current_app
import datetime, jwt
from datetime import timedelta, datetime
from queries import common_db, auth_db
from config import SUPER_ADMIN_ROLE, ADMIN_ROLE, USER_ROLE
# from app import app


auth = Blueprint('auth', __name__)


# User list
@auth.route('/api/users', methods=['GET'])
@token_required([SUPER_ADMIN_ROLE, ADMIN_ROLE])
def getAllUser():
    # check role admin
    # if not admin:

    # :
    data = common_db.selectAllData('users')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500
    
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
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'role' : user['role']
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'token': token,
                            'status': 200,
                            'WWW-Authenticate': 'User Authenticated!'}), 200
            
        else:
            return jsonify({'message': 'Authentication failed!',
                        'status': 401,
                        'WWW-Authenticate': 'Kredensial salah. Cek kembali akun Anda!'}), 401

