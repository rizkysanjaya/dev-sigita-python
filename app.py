from flask import Flask, render_template
from api.auth import auth
from api.kegiatan import kegiatan

app = Flask(__name__, template_folder="templates")

# debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Configure the app if needed (e.g., database settings)
app.config['SECRET_KEY'] = 'thisissecret'
# app.logger.debug(f'Secret Key: {app.config["SECRET_KEY"]}')

# Register the blueprints
app.register_blueprint(kegiatan)
# app.register_blueprint(user_api)
app.register_blueprint(auth)


# Home
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
     app.run(debug=True)

