import prelude
from visualizer import request_visualizer_window, start_visualizer, end_visualizer

import os
import sys
import subprocess
import numpy as np
import pandas as pd
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
    return send_from_directory(os.getcwd(), 'music_features_dedupe.csv')


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
        start_visualizer(name)

        # global process
        # if process is not None:
        #     process.kill()
        # process = subprocess.Popen(
        #     [sys.executable, 'visualizer.py', name],
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        # )


if __name__ == '__main__':
    df_features = pd.read_csv('music_features.csv')

    # for i, row in df_features.iterrows():
    #     key = row['name']
    #     if key == row.song:
    #         features=get_features(key,row.genre, )
    #         if len(sub):
    #             row['name'] = f'charts/{sub.iloc[0].}'
    #
    # df_features.to_csv('music_features.csv')

    # print(len(df_features[df_features.name == df_features.song]))  ###
    # df_features = df_features[df_features.name != df_features.song]  ## TODO

    df_features.drop_duplicates(['song', 'artist'], keep='first', inplace=True)
    df_features.to_csv('music_features_dedupe.csv')

    request_visualizer_window()

    socketio.run(app, port=port)
