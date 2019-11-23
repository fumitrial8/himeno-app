# -*- coding: utf-8 -*-
from datetime import datetime
import os
from flask_socketio import SocketIO
from pytz import timezone
from flask import Flask,render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import keras, sys
from keras.models import Sequential, load_model
from PIL import Image
import numpy as np
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

classes = [ "himeno", "naoya"]
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)
thread = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            model = load_model("./animal_cnn_aug.h5")

            image = Image.open(filepath)
            image = image.convert("RGB")
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)

            return classes[predicted] + "確率:"+ str(percentage) + " %"
            # return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset='UTF-8'>
    <title>ファイルをアップロードして判定しよう</title></head>
    <body>
    <h1>ファイルをアップロードして判定しよう！</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type = file name = file></p>
    <input type = submit value = Upload>
    </form>
    </body>
    </html>
    '''


@socketio.on('connect', namespace='/socket')
def connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
