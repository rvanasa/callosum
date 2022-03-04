import prelude
from visualizer import start_visualizer, end_visualizer

import os
import sys
import subprocess
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit

port = 5000

app = Flask('callosum-relay')
app.config['SECRET_KEY'] = app.name
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins='*')

process = None


@app.route('/static/features.csv')
@cross_origin()
def static_features():
    print(12345)
    return send_from_directory(os.getcwd(), 'music_features.csv')


@app.route('/current')
@cross_origin()
def current():
    return 'default'  ###


# @socketio.event
# def connect(data):
#     print('Connection:', data)  ##


@socketio.event
def msg(data):
    print('Message:', data)

    if not isinstance(data, dict):
        return

    if data.get('type') == 'select':
        name = data.get('name')
        print(name)
        # start_visualizer(name)  ###
        global process
        if process is not None:
            process.kill()
        process = subprocess.Popen(
            [sys.executable, 'visualizer.py', name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


if __name__ == '__main__':
    socketio.run(app, port=port)
