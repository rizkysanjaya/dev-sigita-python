from flask import jsonify, request
from flask import current_app 
import psycopg2
import psycopg2.extras
import jwt, secrets, string
from functools import wraps
from config import db_params



# debug log
import logging
logging.basicConfig(level=logging.DEBUG)
# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



def token_required(f):
    """
    Dekorator untuk memeriksa token otentikasi yang diberikan dalam header permintaan.

    Args:
        f (function): Fungsi yang akan diberi dekorasi.

    Returns:
        function: Fungsi yang diberi dekorasi.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token is None or not token.startswith('Bearer '):
            return jsonify({'message': 'Token hilang atau tidak valid'}), 401

        token = token.split(' ')[1]  # Hapus kata kunci "Bearer"

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = {
                'nip': data.get('nip'),
                'role': data.get('role'),
                # Tambahkan atribut pengguna lainnya jika diperlukan
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token telah kadaluarsa'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token tidak valid'}), 401
        except Exception as e:
            return jsonify({'message': 'Error dalam decoding token', 'error': str(e)}), 401

        # Teruskan current_user sebagai argumen ke fungsi yang diberi dekorasi
        return f(current_user, *args, **kwargs)

    return decorated


# Check user in db
def checkUser(nip):
    """
    Memeriksa keberadaan pengguna berdasarkan NIP.

    Parameters:
        nip (str): Nomor Induk Pegawai (NIP) pengguna yang akan diperiksa.

    Returns:
        dict or None: Dictionary berisi data pengguna (nip, password, role) jika ditemukan dalam database,
                      atau None jika pengguna tidak ditemukan.
    """
    try:
        query = "SELECT nip, password, role FROM users WHERE nip = %s"
        cur.execute(query, (nip,))
        user_data = cur.fetchone()

        if user_data is not None:
            user = {
                "nip": user_data[0],
                "password": user_data[1],
                "role": user_data[2]
            }
            return user  # Pengguna ditemukan dalam database
        else:
            return None  # Pengguna tidak ditemukan
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Buat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

    

# register user
def addUser(values):
    """
    Menambahkan data pengguna baru ke dalam database.

    Parameters:
        values (tuple): Tuple yang berisi data pengguna yang akan ditambahkan (nip, nama, email, wa_number, role, password, avatar_url, is_default_password, status, random_password).

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika data pengguna berhasil ditambahkan.
               Status HTTP 500 digunakan jika terjadi kesalahan server.
    """
    try:

        nip, nama, email, wa_number, role, password, avatar_url, is_default_password, status, random_password = values
        sql = """
            INSERT INTO users (nip, name, email, wa_number, role, password, avatar_url, is_default_password, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (nip, nama, email, wa_number, role, password, avatar_url, is_default_password, status))
        # Jika eksekusi berhasil, commit transaksi
        cur.connection.commit()
        return jsonify({"message": "Data user berhasil ditambahkan!"},
                {
                "password": random_password,  
                "avatar": values[6],    
                "wa_number": values[3]  
                }), 200
    
    except (Exception, psycopg2.DatabaseError) as error:
        # Buat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

def generateRandomPassword(length=16):
    """
    Menghasilkan kata sandi acak dengan panjang tertentu.

    Parameters:
        length (int): Panjang kata sandi yang akan dihasilkan. Default adalah 16 karakter.

    Returns:
        str: Kata sandi acak yang dihasilkan.
    """
    # Tentukan set karakter untuk kata sandi
    characters = string.ascii_letters + string.digits

    # Gunakan modul secrets untuk menghasilkan kata sandi acak dengan aman
    random_password = ''.join(secrets.choice(characters) for _ in range(length))

    return random_password


# def check_authorization(user_role, target_role):
#     # Check if the user has the privilege to register the specified role
#     if (
#         (user_role == SUPER_ADMIN_ROLE and target_role in [SUPER_ADMIN_ROLE, ADMIN_ROLE, USER_ROLE]) or
#         (user_role == ADMIN_ROLE and target_role in [ADMIN_ROLE, USER_ROLE])
#     ):
#         return True
#     else:
#         return False
    
    