import os
import re
from flask import Flask, flash, jsonify
from flask import request
app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# home route

UPLOAD_FOLDER = './images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return "Hello World"
    if request.method == 'POST':
        app.logger.debug('Headers: %s', request.files)
        if request.files:
            img = request.files['image']
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
            print("Image saved")
            return "Uploaded Successfully"
        else:
            return "no file"




