from flask import Blueprint, request
from flask import jsonify
import psycopg2
import psycopg2.extras
from queries import common_db, kegiatan_db
from queries.kegiatan_db import addKegiatan
from config import SUPER_ADMIN_ROLE, ADMIN_ROLE, USER_ROLE
from queries.auth_db import token_required


kegiatan = Blueprint('kegiatan', __name__)

# CREATE KEAGIATAN
@kegiatan.route('/api/kegiatan', methods=['POST'])
def createKegiatan():
    try:

        jsonObject = request.json

        nama_kegiatan = jsonObject.get('nama_kegiatan')
        tanggal = jsonObject.get('tanggal')
        jam_mulai = jsonObject.get('jam_mulai')
        jam_selesai = jsonObject.get('jam_selesai')
        zona_waktu = jsonObject.get('zona_waktu')
        tempat = jsonObject.get('tempat')
        status = jsonObject.get('status')
        is_draft = jsonObject.get('is_draft')
        # Create a list of values to pass to 'addKegiatan'
        values = [nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft]

        # Call the 'addKegiatan' function with the extracted 'values'
        result, status_code = addKegiatan(values)

        # Return a response indicating success or failure
        return result, status_code
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500

# ASSIGN KEGIATAN
@kegiatan.route('/api/kegiatan/assign', methods=['POST'])
def assignKegiatan():
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

        # Define columns and values for Table B (e.g., detail_kegiatan)
        columns2 = ['kegiatan_id', 'jam_mulai', 'jam_selesai', 'tempat', 'status', 'is_draft']
        values2 = [generated_id, jam_mulai, jam_selesai, tempat, status, is_draft]

        # Call the 'addKegiatan' function with the extracted 'values'
        result, status_code = addKegiatan(values)

        # Return a response indicating success or failure
        return result, status_code
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
    
# UPDATE KEGIATAN by ID
@kegiatan.route('/api/kegiatan/<int:id>', methods=['PUT'])
def updateKegiatan(id):
    try:
        jsonObject = request.json

        nama_kegiatan = jsonObject.get('nama_kegiatan')
        tanggal = jsonObject.get('tanggal')
        jam_mulai = jsonObject.get('jam_mulai')
        jam_selesai = jsonObject.get('jam_selesai')
        zona_waktu = jsonObject.get('zona_waktu')
        tempat = jsonObject.get('tempat')
        status = jsonObject.get('status')
        is_draft = jsonObject.get('is_draft')

        values = [nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft]
        data = kegiatan_db.editKegiatan(values, (id))
        if data != 200:
            return data
        else:
            return jsonify({"message": "Kesalahan pada server."}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500



# GET ALL KEGIATAN
@kegiatan.route('/api/kegiatan', methods=['GET'])
def getKegiatan():
    data = common_db.selectAllData('kegiatan')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# GET KEGIATAN DRAFT    
@kegiatan.route('/api/kegiatan/draft', methods=['GET'])
def getDraftKegiatan():
    data = common_db.selectAllData('kegiatan', 'is_draft = 1')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# GET KEGIATAN by ID
@kegiatan.route('/api/kegiatan/<int:id>', methods=['GET'])
def getDetailKegiatan(id):
    data = common_db.selectAllData('kegiatan', f'id = {id}')

    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500
    

# CANCEL KEGIATAN (SET STATUS TO BATAL)
@kegiatan.route('/api/kegiatan/batal', methods=['POST'])
def batalKegiatan():
    
    _id = request.json['id_kegiatan']
    data = kegiatan_db.cancelKegiatan(_id)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# DELETE KEGIATAN by ID
@kegiatan.route('/api/kegiatan/<int:id>', methods=['DELETE'])
def hapusKegiatan(id):
    data = common_db.deleteData('kegiatan', (id))
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500
    
# Hapus lampiran kegiatan
@kegiatan.route('/api/lampiran-kegiatan/hapus/<int:id>', methods=['POST'])
@token_required([SUPER_ADMIN_ROLE, ADMIN_ROLE])
def hapusLampiran(id):
    data = kegiatan_db.deleteLampiran(id)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500