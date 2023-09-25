from flask import jsonify, request
from config import db_params
import psycopg2
import psycopg2.extras
from queries import auth_db 

# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Select user by id
def selectUser(id):
    try:
        query = f"SELECT * FROM users WHERE id = {id}"
        cur.execute(query)
        rows = cur.fetchall()

        if not rows:  # Check if rows is empty (no records found)
            # Return a "no record available" message
            response_data = {"message": "Data masih kosong!"}
            return jsonify(response_data), 200  # Use 404 to indicate "Not Found" 

        # Create a JSON response with a list of records
        response_data = {"data": rows}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
    
# Edit user by id
def editUser(data, id):
    try:

        name, nip, email, role, wa_number, status = data
        # Update the user record in the database
        user_sql = """
            UPDATE users
            SET name=%s, nip=%s, email=%s, role=%s, wa_number=%s, status=%s
            WHERE id=%s
        """
        user_data = (name, nip, email, role, wa_number, status, id)
        cur.execute(user_sql, user_data)

        # Commit the transaction
        conn.commit()

        response_data = {"message": "Data berhasil diubah!"}
        return jsonify(response_data), 200

    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
    
# Reset password
def resetUserPassword(id):
    try:
        # Update the user record in the database
        user_sql = """
            UPDATE users
            SET password=%s, is_default_password=%s
            WHERE id=%s
        """
        new_password = auth_db.generateRandomPassword()
        user_data = (new_password, 1, id)
        cur.execute(user_sql, user_data)

        # Commit the transaction
        conn.commit()

        response_data = {"message": "Password berhasil direset!",
                         "password": new_password}
        return jsonify(response_data), 200

    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500
    
def updateAvaUser(data, id):
    try:
        avatar_url = data
        # Update the user record in the database
        user_sql = """
            UPDATE users
            SET avatar_url=%s
            WHERE id=%s
        """
        user_data = (f'/path/to/file/{avatar_url}', id)
        cur.execute(user_sql, user_data)

        # Commit the transaction
        conn.commit()

        response_data = {"message": "Avatar berhasil diubah!"}
        return jsonify(response_data), 200

    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, terdapat kesalahan.. ": str(error)}
        return jsonify(error_message), 500