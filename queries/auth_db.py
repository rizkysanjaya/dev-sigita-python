from flask import jsonify, request, current_app
from config import db_params
import psycopg2
import psycopg2.extras
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt, secrets, string
from functools import wraps



# debug log
import logging
logging.basicConfig(level=logging.DEBUG)
# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



def token_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # token = None
            token = request.headers.get('Authorization')
            if token is not None and token.startswith('Bearer '):
                token = token.split(' ')[1]  # Remove "Bearer" keyword
            # if 'x-access-token' in request.headers:
            #     token = request.headers['x-access-token']

            if not token:
                return jsonify({'message': 'Token tidak ditemukan!'}), 401

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token sudah kadaluwarsa. Siahkan login kembali.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token tidak valid!'}), 401
            except Exception as e:
                # current_app.logger.error(f'Token decoding error: {str(e)}')
                return jsonify({'message': 'Token decoding error'}), 401

            # Check if the user's role is in the required_roles list
            if data.get('role') not in required_roles:
                return jsonify({'message': 'Anda tidak bisa akses halaman ini.'}), 403

            return f(*args, **kwargs)

        return decorated

    return decorator

# Check user in db
def checkUser(nip, password):
    try:
        query = "SELECT nip, name, role FROM users WHERE nip = %s AND password = %s"
        cur.execute(query, (nip, password))
        user_nip = cur.fetchone()

        # debug
        # current_app.logger.debug(f'SQL Query: {query}')
        # current_app.logger.debug(f'Result: {user_nip}')

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
        return jsonify({"Oops, terdapat kesalahan.. ": str(error)}), 500
    

# register user
def addUser(values):
    try:
        placeholders = ', '.join(['%s'] * len(values))
        columns = 'nip, name, email, wa_number, role, password, avatar_url, is_default_password, status'
        sql = f"INSERT INTO users ({columns}) VALUES ({placeholders})"
        cur.execute(sql, values)
        # If the execution is successful, commit the transaction
        cur.connection.commit()
        return jsonify({"message": "Data user berhasil ditambahkan!"},
                {
                "password": values[5],  
                "avatar": values[6],    
                "wa_number": values[3]  
                }), 200
    
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
    



def generateRandomPassword(length=16):
    # Define the character set for the password
    characters = string.ascii_letters + string.digits

    # Use secrets module to securely generate a random password
    random_password = ''.join(secrets.choice(characters) for _ in range(length))

    return random_password

