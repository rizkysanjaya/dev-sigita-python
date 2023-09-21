from flask import jsonify
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
def assignKegiatan(values):
    try:
        jsonObject = request.json

        # Extract values from the JSON object
        nama_kegiatan = jsonObject.get('nama_kegiatan')
        tanggal = jsonObject.get('tanggal')
        jam_mulai = jsonObject.get('jam_mulai')
        jam_selesai = jsonObject.get('jam_selesai')
        zona_waktu = jsonObject.get('zona_waktu')
        tempat = jsonObject.get('tempat')
        status = jsonObject.get('status')
        is_draft = jsonObject.get('is_draft')

        # Define columns and values for Table A (e.g., kegiatan)
        columns1 = ['nama_kegiatan', 'tanggal', 'jam_mulai', 'zona_waktu']
        values1 = [nama_kegiatan, tanggal, jam_mulai, zona_waktu]

        # Insert data into Table A (e.g., kegiatan)
        sql_insert_a = f"INSERT INTO kegiatan ({', '.join(columns1)}) VALUES ({', '.join(['%s'] * len(values1))}) RETURNING id"
        cur.execute(sql_insert_a, values1)
        generated_id = cur.fetchone()[0]

        # Define columns and values for Table B (e.g., detail_kegiatan)
        columns2 = ['id_kegiatan', 'jam_mulai', 'jam_selesai', 'tempat', 'status', 'is_draft']
        values2 = [generated_id, jam_mulai, jam_selesai, tempat, status, is_draft]

        # Insert data into Table B (e.g., detail_kegiatan)
        sql_insert_b = f"INSERT INTO user_kegiatan ({', '.join(columns2)}) VALUES ({', '.join(['%s'] * len(values2))})"
        cur.execute(sql_insert_b, values2)

        # Commit the transaction
        cur.connection.commit()

        return jsonify({"message": "Data berhasil ditambahkan!"}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500


# Update kegiatan
# def editKegiatan(values, id):
#     try:

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