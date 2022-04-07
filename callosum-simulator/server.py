import prelude
from visualizer import request_visualizer_window, start_visualizer, end_visualizer

import os
import sys
import subprocess
import numpy as np
import pandas as pd
import socketio

host = 'https://room-relay.herokuapp.com'

sio = socketio.Client()


@sio.on('connect')
def on_connect():
    sio.emit('join', 'callosum')


@sio.on('msg')
def on_msg(sid, data):
    try:
        print('Message:', data)
        if not isinstance(data, dict):
            return

        if data.get('type') == 'select':
            name = data.get('name')
            print(name)
            start_visualizer(name)
    except Exception as err:
        print(err)


@sio.on('*')
def on_any(*args):
    print(*args)


process = None

if __name__ == '__main__':
    df_features = pd.read_csv('music_features.csv')

    # from spotify import sp, get_features
    # for i, row in df_features.iterrows():
    #     key = row['name']
    #     if key == row.song:
    #         results = sp.search(f'{row.artist} - {row.song}')['tracks']['items']
    #         if not len(results):
    #             print('No results:', f'{row.artist} - {row.song}')
    #             continue
    #         print(results[0]['id'])  ####
    #         df_features.loc[i, 'name'] = f'charts/{results[0]["id"]}'
    # df_features.to_csv('music_features_fix.csv', index=False)

    df_features.drop_duplicates(['name'], keep='first', inplace=True)
    df_features.drop_duplicates(['song', 'artist'], keep='first', inplace=True)
    df_features.to_csv('../callosum-webapp/public/data/features.csv', index=False)

    request_visualizer_window()

    sio.connect(host)
