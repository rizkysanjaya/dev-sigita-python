from flask import jsonify, request
from config import db_params
import psycopg2
import psycopg2.extras

# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# # Kegiatan Database Route

# Creaate kegiatan
def addKegiatan(values):
    try:
        placeholders = ', '.join(['%s'] * len(values))
        columns = 'nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft'
        sql = f"INSERT INTO kegiatan ({columns}) VALUES ({placeholders})"
        cur.execute(sql, values)
        # If the execution is successful, commit the transaction
        cur.connection.commit()
        return jsonify({"message": "Data kegiatan berhasil ditambahkan!"}), 200

    except psycopg2.Error as error:
        # Capture and log the actual error message from the database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal ditambahkan!", "Error Message": error_message}), 500
    
# assign kegiatan
def assignKegiatan(data):
    try:

        # Extract data for the primary table (kegiatan)
        nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft, users, protokoler, files = data


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
            INSERT INTO user_kegiatan (id_kegiatan, id_user, is_protokoler)
            VALUES (%s, %s, %s);
        """
        for user_id in users:
            cur.execute(user_kegiatan_sql, (kegiatan_id, user_id, 1))  # Set is_protokoler to 0

        # Insert data into the related table (user_kegiatan) for protokoler users
        for protokoler_id in protokoler:
            cur.execute(user_kegiatan_sql, (kegiatan_id, protokoler_id, 0))  # Set is_protokoler to 1

        # Insert data into the related table (lampiran) using a loop
        lampiran_sql = """
            INSERT INTO lampiran (id_kegiatan, path, nama_file)
            VALUES (%s, %s, %s);
        """
        for file_name in files:
            cur.execute(lampiran_sql, (kegiatan_id, f'/path/to/file/{file_name}', file_name))


        # Commit the transaction
        conn.commit()

        return jsonify({"message": "Data berhasil ditambahkan!"}), 200

    except (Exception, psycopg2.DatabaseError) as error:
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500


# Update kegiatan
def editKegiatan(values, id):
    try:

        # values = [nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft]
        placeholders = ', '.join(['%s'] * len(values))
        columns = 'nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft'

        # Update the record in the database
        sql = f"UPDATE kegiatan SET ({columns}) = ({placeholders}) WHERE id = {id}"
        cur.execute(sql, values)
        cur.connection.commit()
        return jsonify({"message": "Data kegiatan berhasil diupdate!"}), 200

    except psycopg2.Error as error:
        # Capture and log the actual error message from the database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal ditambahkan!", "Error Message": error_message}), 500

# Cancel kegiatan
def cancelKegiatan(id):
    try:
        query = f"UPDATE kegiatan SET status='BATAL' WHERE id={id}"
        cur.execute(query)
        cur.connection.commit()
        return jsonify({"message": "Data kegiatan berhasil dibatalkan!"}), 200
    except psycopg2.Error as error:
        # Capture and log the actual error message from the database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal dibatalkan!", "Error Message": error_message}), 500
        
# Delete kegiatan

# Delete Lampiran Kegiatan
def deleteLampiran(id):
    try:
        query = f"DELETE FROM lampiran WHERE id = {id}"
        cur.execute(query)
        conn.commit()
        response_data = {"message": "Lampiran berhasil dihapus!"}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500