from flask import jsonify, request, make_response
from config import db_params
import psycopg2
import psycopg2.extras
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import current_app
# import models
import logging
logging.basicConfig(level=logging.DEBUG)
# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



def token_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid'}), 401
            except Exception as e:
                current_app.logger.error(f'Token decoding error: {str(e)}')
                return jsonify({'message': 'Token decoding error'}), 401

            # Check if the user's role is in the required_roles list
            if data.get('role') not in required_roles:
                return jsonify({'message': 'Access forbidden'}), 403

            return f(*args, **kwargs)

        return decorated

    return decorator

# Check user in db
def checkUser(nip, password):
    try:
        query = "SELECT nip, name, role FROM users WHERE nip = %s AND password = %s"
        cur.execute(query, (nip, password))
        user_nip = cur.fetchone()

        current_app.logger.debug(f'SQL Query: {query}')
        current_app.logger.debug(f'Result: {user_nip}')

        if user_nip is None:
            return jsonify({"message": "NIP atau password salah!"}), 401
        else:
            user_info = {
                "nip": user_nip[0],
                "name": user_nip[1],
                "role": user_nip[2]
                # Add more user attributes as needed
            }
            return user_info  # User found in the database
            
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Handle the error here or log it, but don't jsonify the error here
        return jsonify({"Oops, there's an error.. ": str(error)}), 500
    

# find user by nip
def findUser(nip):
    try:
        query = "SELECT * FROM users WHERE nip = %s"
        cur.execute(query, (nip,))
        user_nip = cur.fetchone()

        cur.close()
        conn.close()

        current_app.logger.debug(f'SQL Query: {query}')
        current_app.logger.debug(f'Result: {user_nip}')

        if user_nip is None:
            return jsonify({"message": "User tidak ditemukan!"}), 404
        else:
            return jsonify(user_nip), 200
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Handle the error here or log it, but don't jsonify the error here
        return jsonify({"Oops, there's an error.. ": str(error)}), 500