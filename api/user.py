from flask import Blueprint, Flask, render_template, request, redirect, url_for, make_response, jsonify
from queries import common_db
from config import SUPER_ADMIN_ROLE, ADMIN_ROLE, USER_ROLE
from queries.auth_db import token_required


user = Blueprint('user', __name__)

# User list
@user.route('/api/users', methods=['GET'])
@token_required([SUPER_ADMIN_ROLE, ADMIN_ROLE])
def getAllUser():
    data = common_db.selectAllData('users')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# User detail
# @user.route('/api/user/<int:id>', methods=['GET'])