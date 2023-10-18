from flask import jsonify, current_app
from config import db_params
import psycopg2, os, time
from werkzeug.utils import secure_filename
# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# # Kegiatan Database Route

# Creaate kegiatan
def addKegiatan(data):
    """
    Menambahkan data kegiatan baru ke dalam tabel 'kegiatan' dalam database.

    Parameters:
        data (tuple): Tuple yang berisi data kegiatan yang akan ditambahkan (nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft).

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika data kegiatan berhasil ditambahkan.
               Status HTTP 500 digunakan jika terjadi kesalahan server atau kesalahan dalam database.
    """
    try:
        nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft = data

        
        sql = """
            INSERT INTO kegiatan (nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft))
        # Jika eksekusi berhasil, commit transaksi
        conn.commit()
        
        return jsonify({"message": "Data kegiatan berhasil ditambahkan!"}), 200

    except psycopg2.Error as error:
        # Tangkap dan log pesan kesalahan aktual dari database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal ditambahkan!", "Error Message": error_message}), 500

    
# assign kegiatan
def assignKegiatan(data):
    try:
        # Extract data for the primary table (kegiatan)
        nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft, users, protokoler, files = data

        # default values
        is_read = 0


        # Insert data into the primary table (kegiatan)
        kegiatan_sql = """
            INSERT INTO kegiatan (nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        cur.execute(kegiatan_sql, (nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft))
        kegiatan_id = cur.fetchone()[0]  # Get the generated ID
        conn.commit()
        # Insert data into the related table (user_kegiatan) using a loop
        user_kegiatan_sql = """
            INSERT INTO user_kegiatan (id_kegiatan, id_user, is_protokoler, is_read, is_ignore)
            VALUES (%s, %s, %s);
        """
        for user_id in users:
            cur.execute(user_kegiatan_sql, (kegiatan_id, user_id, 1, 0, 0))  # Set is_protokoler to 0

        # Insert data into the related table (user_kegiatan) for protokoler users
        for protokoler_id in protokoler:
            cur.execute(user_kegiatan_sql, (kegiatan_id, protokoler_id, 0, 0, 0))  # Set is_protokoler to 1

        # Insert data into the related table (lampiran) using a loop
        lampiran_sql = """
            INSERT INTO lampiran (id_kegiatan, path, nama_file)
            VALUES (%s, %s, %s);
        """
        
        for file_name in files:
            timestamp = int(time.time())  # Get current timestamp
            filename, file_extension = os.path.splitext(file_name)
            unique_filename = f"{filename}_{timestamp}{file_extension}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(unique_filename))
            cur.execute(lampiran_sql, (kegiatan_id, file_path, secure_filename(file_name)))


        # Commit the transaction
        conn.commit()

        return jsonify({"message": "Data berhasil ditambahkan!"}), 200

    except (Exception, psycopg2.DatabaseError) as error:
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

# Edit kegiatan
def editKegiatan(data, id):
    """
    Mengubah data kegiatan dalam database berdasarkan ID.

    Parameters:
        data (tuple): Tuple yang berisi data kegiatan yang akan diubah.
                      Data yang diubah meliputi (nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft, users, protokoler, files).
        id (int): ID kegiatan yang akan diubah.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika kegiatan berhasil diubah.
               Status HTTP 500 digunakan jika terjadi kesalahan server atau kesalahan dalam database.
    """
    try:
        nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft, users, protokoler, files = data

        # Mulai transaksi
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Mengupdate rekaman kegiatan dalam database
        kegiatan_sql = """
            UPDATE kegiatan
            SET nama_kegiatan=%s, tanggal=%s, tanggal_selesai=%s, jam_mulai=%s, jam_selesai=%s, 
            zona_waktu=%s, tempat=%s, status=%s, is_draft=%s
            WHERE id=%s
        """
        kegiatan_data = (nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status,
                        is_draft, id)
        cur.execute(kegiatan_sql, kegiatan_data)

        # Hapus dan masukkan rekaman user_kegiatan untuk pengguna
        user_kegiatan_sql = """
            DELETE FROM user_kegiatan WHERE id_kegiatan = %s;
        """
        cur.execute(user_kegiatan_sql, (id,))
        for user_id in users:
            cur.execute(user_kegiatan_sql, (id,))  # Hapus rekaman yang sudah ada

        user_kegiatan_sql = """
            INSERT INTO user_kegiatan (id_kegiatan, id_user, is_protokoler)
            VALUES (%s, %s, %s);
        """
        for user_id in users:
            cur.execute(user_kegiatan_sql, (id, user_id, 1))  # Masukkan rekaman baru

        # Hapus dan masukkan rekaman user_kegiatan untuk protokoler
        protokoler_sql = """
            DELETE FROM user_kegiatan WHERE id_kegiatan = %s;
        """
        cur.execute(protokoler_sql, (id,))
        for protokoler_id in protokoler:
            cur.execute(protokoler_sql, (id,))  # Hapus rekaman yang sudah ada

        protokoler_sql = """
            INSERT INTO user_kegiatan (id_kegiatan, id_user, is_protokoler)
            VALUES (%s, %s, %s);
        """
        for protokoler_id in protokoler:
            cur.execute(protokoler_sql, (id, protokoler_id, 0))  # Masukkan rekaman baru

        # Hapus dan masukkan rekaman lampiran untuk file
        lampiran_sql = """
            DELETE FROM lampiran WHERE id_kegiatan = %s;
        """
        cur.execute(lampiran_sql, (id,))
        for file_name in files:
            cur.execute(lampiran_sql, (id,))  # Hapus rekaman yang sudah ada

        lampiran_sql = """
            INSERT INTO lampiran (id_kegiatan, path, nama_file)
            VALUES (%s, %s, %s);
        """

        for file_name in files:
            timestamp = int(time.time())  # Dapatkan timestamp saat ini
            filename, file_extension = os.path.splitext(file_name)
            unique_filename = f"{filename}_{timestamp}{file_extension}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(unique_filename))
            cur.execute(lampiran_sql, (id, file_path, secure_filename(file_name)))

        # Commit transaksi
        conn.commit()
        return jsonify({"message": "Kegiatan berhasil diupdate!"}), 200

    except (Exception, psycopg2.DatabaseError) as error:
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

    
# Edit kegiatan
def editAssignKegiatan(data, id):
    try:
        nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft, users, = data

        # Start a transaction
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Update the kegiatan record in the database
        kegiatan_sql = """
            UPDATE kegiatan
            SET nama_kegiatan=%s, tanggal=%s, tanggal_selesai=%s, jam_mulai=%s, jam_selesai=%s, 
            zona_waktu=%s, tempat=%s, status=%s, is_draft=%s
            WHERE id=%s
        """
        kegiatan_data = (nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status,
                        is_draft, id)
        cur.execute(kegiatan_sql, kegiatan_data)

        # Delete and insert user_kegiatan records for users
        user_kegiatan_sql = """
            DELETE FROM user_kegiatan WHERE id_kegiatan = %s;
        """
        cur.execute(user_kegiatan_sql, (id,))
        for user_id in users:
            cur.execute(user_kegiatan_sql, (id,))  # Delete existing records

        user_kegiatan_sql = """
            INSERT INTO user_kegiatan (id_kegiatan, id_user, is_protokoler)
            VALUES (%s, %s, %s);
        """
        for user_id in users:
            cur.execute(user_kegiatan_sql, (id, user_id, 1))  # Insert new records

        # Commit the transaction
        conn.commit()
        return jsonify({"message": "Kegiatan berhasil diupdate!"}), 200

    except (Exception, psycopg2.DatabaseError) as error:
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

# Update kegiatan
# def updateKegiatan(data, id):
#     try:

#         # values = [nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft]
#         placeholders = ', '.join(['%s'] * len(values))
#         columns = 'nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft'

#         # Update the record in the database
#         sql = f"UPDATE kegiatan SET ({columns}) = ({placeholders}) WHERE id = {id}"
#         cur.execute(sql, values)
#         conn.commit()
#         return jsonify({"message": "Data kegiatan berhasil diupdate!"}), 200

#     except psycopg2.Error as error:
#         # Capture and log the actual error message from the database
#         error_message = str(error)
#         print("Database Error:", error_message)
#         return jsonify({"message": "Data kegiatan gagal ditambahkan!", "Error Message": error_message}), 500

# Cancel kegiatan
def cancelKegiatan(id):
    """
    Membatalkan kegiatan berdasarkan ID dengan mengubah status kegiatan menjadi 'BATAL'.

    Parameters:
        id (int): ID kegiatan yang akan dibatalkan.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika kegiatan berhasil dibatalkan.
               Status HTTP 500 digunakan jika terjadi kesalahan server atau kesalahan dalam database.
    """
    try:
        query = f"UPDATE kegiatan SET status='BATAL' WHERE id={id}"
        cur.execute(query)
        conn.commit()
        return jsonify({"message": "Data kegiatan berhasil dibatalkan!"}), 200
    except psycopg2.Error as error:
        # Tangkap dan log pesan kesalahan aktual dari database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal dibatalkan!", "Error Message": error_message}), 500


# Delete Lampiran Kegiatan
def deleteLampiran(id):
    """
    Menghapus lampiran berdasarkan ID.

    Parameters:
        id (int): ID lampiran yang akan dihapus.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika lampiran berhasil dihapus.
               Status HTTP 500 digunakan jika terjadi kesalahan server atau kesalahan dalam database.
    """
    try:
        query = f"DELETE FROM lampiran WHERE id = {id}"
        cur.execute(query)
        conn.commit()
        response_data = {"message": "Lampiran berhasil dihapus!"}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Buat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

    

# update status read
def updateStatusRead(id):
    """
    Mengupdate status 'is_read' menjadi 1 (read) pada data kegiatan pengguna tertentu.

    Parameters:
        id (int): ID kegiatan pengguna yang status 'is_read'nya akan diupdate.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika status berhasil diupdate.
               Status HTTP 500 digunakan jika terjadi kesalahan server atau kesalahan dalam database.
    """
    try:
        query = f"UPDATE user_kegiatan SET is_read=1 WHERE id_kegiatan = {id}"
        cur.execute(query)
        conn.commit()
        response_data = {"message": "Status read berhasil diupdate!"}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Buat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
    
def updateHadir(data):
    try:
        keterangan, is_ignore, kehadiran, id_kegiatan, id_user = data

        # Update the record in the database
        user_sql = """ UPDATE user_kegiatan SET reason=%s, is_ignore=%s, status_kehadiran=%s WHERE id_kegiatan=%s AND id_user=%s """
        user_data = (keterangan, is_ignore, kehadiran, id_kegiatan, id_user)
        # logging.debug(f"Executing SQL: {user_sql}, Data: {user_data}")
        current_app.logger.info(f"Executing SQL: {user_sql}, Data: {user_data}")
        cur.execute(user_sql, user_data)
        conn.commit()
        return jsonify({"message": "Data kehadiran berhasil diupdate!"}), 200

    except psycopg2.Error as error:
        # Capture and log the actual error message from the database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kehadiran gagal diupdate!", "Error Message": error_message}), 500

# get kegiatan per user id
def getKegiatanUser(id, status):
    try:
        # Establish a database connection and create a cursor
         
        # Define the SQL query to select events for a specific user with a given status
        query = """
            SELECT K.ID,
                K.nama_kegiatan,
                K.tanggal,
                K.jam_mulai,
                K.jam_selesai,
                K.zona_waktu,
                K.tempat,
                K.status,
                K.is_draft,
                K.tanggal_selesai 
            FROM
                kegiatan
                K INNER JOIN user_kegiatan uk ON K.ID = uk.id_kegiatan 
            WHERE
                uk.id_user = %s 
                AND K.status = %s
        """

        # Execute the query with user_id and event_status as parameters
        cur.execute(query, (id, status))
        rows = cur.fetchall()

        for row in rows:
                row['jam_mulai'] = row['jam_mulai'].strftime("%H:%M")
                row['jam_selesai'] = row['jam_selesai'].strftime("%H:%M")
        # Check if any events were found
        if not rows:
            return jsonify({"message": "No events found for the user with the given status."}), 404

        # Create a response JSON with event data
        response_data = {"data": rows}
        return jsonify(response_data), 200

    except (Exception, psycopg2.DatabaseError) as error:
        # Handle database errors or other exceptions
        return jsonify({"message": f"Error: {str(error)}"}), 500