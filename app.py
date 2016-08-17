# -*- coding: utf-8 -*-
from datetime import datetime
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from pytz import timezone

app = Flask(__name__)
socketio = SocketIO(app)
thread = None


@app.route('/')
def index():
    tz = timezone('Asia/Tokyo')
    now = datetime.now(tz)
    return render_template(
            'index.html',
            hour=__make_clock_img_path('hours', now.hour),
            minute=__make_clock_img_path('minutes', now.minute)
            )


@socketio.on('connect', namespace='/socket')
def connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


def background_thread():
    while True:
        tz = timezone('Asia/Tokyo')
        before = datetime.now(tz)
        socketio.sleep(1)
        after = datetime.now(tz)

        if before.hour != after.hour:
            path = __make_clock_img_path('hours', after.hour)
            socketio.emit('change hour',
                          {'img_path': os.path.join('/static', path)},
                          namespace='/socket')

        if before.minute != after.minute:
            path = __make_clock_img_path('minutes', after.minute)
            socketio.emit('change minute',
                          {'img_path': os.path.join('/static', path)},
                          namespace='/socket')


def __make_clock_img_path(div, num):
    num_text = '%02d' % num
    return "img/%s/%s.png" % (div, num_text)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
