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
@kegiatan.route('/api/kegiatan/new', methods=['POST'])
def assignKegiatan():
    # def insert_complex_data(data):
    try:
        nama_kegiatan = request.form.get('nama_kegiatan')
        tanggal = request.form.get('tanggal')
        tanggal_selesai = request.form.get('tanggal_selesai')
        jam_mulai = request.form.get('jam_mulai')
        jam_selesai = request.form.get('jam_selesai')
        zona_waktu = request.form.get('zona_waktu')
        tempat = request.form.get('tempat')
        status = request.form.get('status')
        is_draft = request.form.get('is_draft')

        # Convert is_draft to an integer
        is_draft = int(is_draft)

        # Assuming you have multiple users and protokoler in form-data
        users = request.form.getlist('users[]')
        protokoler = request.form.getlist('protokoler[]')

        # Assuming you have multiple files in form-data
        files = request.files.getlist('files[]')

        file_names = [file.filename for file in files if file]

        # # Save uploaded files to a directory on the server's file system
        # saved_files = []
        # for file in files:
        #     if file:
        #         filename = secure_filename(file.filename)
        #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(file_path)
        #         saved_files.append(file_path)

        # assign values to data
        data = [nama_kegiatan, tanggal, tanggal_selesai, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft, users, protokoler, file_names]

        result, status_code = kegiatan_db.assignKegiatan(data)

        return result, status_code

    except (Exception, psycopg2.DatabaseError) as error:
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