import os
from flask import Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/shipw/OneDrive/Desktop/Dojo_Python/Final Project/flask_app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "Do you even hunt bro?"