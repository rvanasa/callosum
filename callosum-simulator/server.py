import prelude
from visualizer import start_visualizer

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
    df_features.drop_duplicates(['name'], keep='first', inplace=True)
    df_features.drop_duplicates(['song', 'artist'], keep='first', inplace=True)
    df_features.to_csv('../callosum-webapp/public/data/features.csv', index=False)

    sio.connect(host)
