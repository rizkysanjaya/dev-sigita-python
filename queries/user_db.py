from flask import jsonify, current_app as app
from config import db_params
import psycopg2, os
from queries import auth_db 
from  werkzeug.security import generate_password_hash

# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Select user by id
def selectUser(id):
    """
    Memilih pengguna berdasarkan ID.

    Parameters:
        id (int): ID pengguna yang akan dipilih.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi data pengguna yang sesuai atau pesan kesalahan jika tidak ditemukan.
               Status HTTP 200 digunakan walaupun data tidak ditemukan (kosong).
               Status HTTP 500 digunakan jika terjadi kesalahan server.
    """
    try:
        query = f"SELECT * FROM users WHERE id = {id}"
        cur.execute(query)
        rows = cur.fetchall()

        if not rows:  # Periksa apakah tidak ada data (tidak ada rekaman ditemukan)
            # Mengembalikan pesan "Data masih kosong!"
            response_data = {"message": "Data masih kosong!"}
            return jsonify(response_data), 200  # Gunakan 200 untuk menunjukkan "Tidak Ditemukan"

        # Membuat respons JSON dengan daftar rekaman
        response_data = {"data": rows}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Membuat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
    
# Edit user by id
def editUser(data, id):
    """
    Mengedit data pengguna berdasarkan ID.

    Parameters:
        data (tuple): Tuple yang berisi data pengguna yang akan diubah (name, nip, email, role, wa_number, status).
        id (int): ID pengguna yang akan diubah.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika data berhasil diubah.
               Status HTTP 500 digunakan jika terjadi kesalahan server.
    """
    try:
        name, nip, email, role, wa_number, status = data

        # Perbarui rekaman pengguna dalam database
        user_sql = """
            UPDATE users
            SET name=%s, nip=%s, email=%s, role=%s, wa_number=%s, status=%s
            WHERE id=%s
        """
        user_data = (name, nip, email, role, wa_number, status, id)
        cur.execute(user_sql, user_data)

        # Commit transaksi
        conn.commit()

        response_data = {"message": "Data berhasil diubah!"}
        return jsonify(response_data), 200

    except (Exception, psycopg2.DatabaseError) as error:
        # Buat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

# Reset password
def resetUserPassword(id):
    """
    Mereset kata sandi pengguna berdasarkan ID.

    Parameters:
        id (int): ID pengguna yang akan mereset kata sandi.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil dan kata sandi acak yang dihasilkan.
               Status HTTP 200 digunakan jika kata sandi berhasil direset.
               Status HTTP 500 digunakan jika terjadi kesalahan server.
    """
    try:
        # Perbarui rekaman pengguna dalam database
        user_sql = """
            UPDATE users
            SET password=%s, is_default_password=%s
            WHERE id=%s
        """

        random_password = auth_db.generateRandomPassword()
        new_password = generate_password_hash(random_password, method='pbkdf2:sha256')
        user_data = (new_password, 1, id)
        cur.execute(user_sql, user_data)

        # Commit transaksi
        conn.commit()

        response_data = {"message": "Password berhasil direset!",
                         "password": random_password}
        return jsonify(response_data), 200

    except (Exception, psycopg2.DatabaseError) as error:
        # Buat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

    
def updateAvaUser(data, id):
    """
    Memperbarui avatar pengguna berdasarkan ID.

    Parameters:
        data (str): Nama file avatar baru yang akan diperbarui.
        id (int): ID pengguna yang akan diperbarui avatar-nya.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil.
               Status HTTP 200 digunakan jika avatar berhasil diperbarui.
               Status HTTP 500 digunakan jika terjadi kesalahan server.
    """
    try:
        avatar_url = data

        # Perbarui rekaman pengguna dalam database
        user_sql = """
            UPDATE users
            SET avatar_url=%s
            WHERE id=%s
        """
        file_path = os.path.join(app.config['AVATAR_FOLDER'], avatar_url)
        user_data = (file_path, id)
        cur.execute(user_sql, user_data)

        # Commit transaksi
        conn.commit()

        response_data = {"message": "Avatar berhasil diubah!"}
        return jsonify(response_data), 200

    except (Exception, psycopg2.DatabaseError) as error:
        # Buat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
