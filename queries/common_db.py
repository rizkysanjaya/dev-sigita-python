from flask import jsonify
from config import db_params
import psycopg2
import psycopg2.extras


# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# GET ALL z DATA
def selectAllData(table, condition=None):
    """
    Memilih semua data dari tabel tertentu dalam database.

    Parameters:
        table (str): Nama tabel yang akan dipilih.
        condition (str, optional): Kondisi tambahan untuk pemilihan data. Default adalah None.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi data dari tabel yang dipilih atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika data berhasil ditemukan.
               Status HTTP 500 digunakan jika terjadi kesalahan server.
    """
    try:
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        query += " ORDER BY id ASC"
        # print(query)
        cur.execute(query)
        rows = cur.fetchall()

        if not rows:  # Periksa apakah tidak ada data (tidak ada rekaman ditemukan)
            # Mengembalikan pesan "Data masih kosong!"
            response_data = {"message": "Data masih kosong!"}
            return jsonify(response_data), 200  # Gunakan 200 untuk menunjukkan "Not Found" 

        if table == 'kegiatan':
            for row in rows:
                row['jam_mulai'] = row['jam_mulai'].strftime("%H:%M")
                row['jam_selesai'] = row['jam_selesai'].strftime("%H:%M")
                # format tanggal ke 'Hari, DD-MM-YYYY'
                row['tanggal'] = row['tanggal'].strftime("%A, %d-%m-%Y")

        # Membuat respons JSON dengan daftar rekaman
        response_data = {"data": rows}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Membuat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500


# reusable delete data function
def deleteData(table, id):
    """
    Menghapus data dari tabel tertentu dalam database berdasarkan ID.

    Parameters:
        table (str): Nama tabel dari mana data akan dihapus.
        id (int): ID data yang akan dihapus.

    Returns:
        tuple: Sebuah tuple yang berisi JSON response dan status HTTP.
               JSON response berisi pesan berhasil atau pesan kesalahan jika terjadi masalah.
               Status HTTP 200 digunakan jika data berhasil dihapus.
               Status HTTP 500 digunakan jika terjadi kesalahan server.
    """
    try:
        query = f"DELETE FROM {table} WHERE id = {id}"
        cur.execute(query)
        conn.commit()
        response_data = {"message": "Data berhasil dihapus!"}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Membuat pesan kesalahan kustom
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
