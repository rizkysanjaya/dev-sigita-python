from flask import Flask, render_template
from api.auth import auth
from api.kegiatan import kegiatan
from api.user import user
import os
app = Flask(__name__, template_folder="templates")

# Konfigurasi logging untuk debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Tetapkan kunci rahasia Flask app untuk keamanan sesi
app.config['SECRET_KEY'] = 'thisissecret'

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'media\\user_upload\\lampiran')
AVATAR_FOLDER = os.path.join(path, 'media\\user_upload\\avatar')
# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.isdir(AVATAR_FOLDER):
    os.mkdir(AVATAR_FOLDER)
app.config['AVATAR_FOLDER'] = AVATAR_FOLDER


# Register blueprint 
app.register_blueprint(kegiatan)  
app.register_blueprint(user)      
app.register_blueprint(auth)      

# Tentukan rute beranda
@app.route('/')
def home():
    """
    Tampilkan halaman beranda.

    Returns:
        str: Konten HTML halaman beranda.
    """
    return render_template('home.html')

if __name__ == '__main__':
    # Jalankan aplikasi dalam mode debug
    app.run(debug=True)
