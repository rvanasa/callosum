import prelude
from visualizer import load_spectrogram
from spotify import get_features

from pydub import AudioSegment
import numpy as np
import pandas as pd
from youtube_dl import YoutubeDL
import librosa
import soundfile as sf
import warnings
import os
import time


def standardize(x):
    return (x - x.mean()) / x.std()


df_features = pd.read_csv('music_features.csv').drop_duplicates('name').set_index('name')

if __name__ == '__main__':

    for track_id, row in df_features.iterrows():
        try:
            # key = f'charts/{track_id}'
            key=row.name
            genre = row.genre
            artist = row.artist
            song = row.song

            if not key.startswith('charts/'):
                continue

            # row = get_features(key, genre, track_id)

            # genre = row.genre
            url = f'ytsearch:{artist} topic - {song}'  # 'topic' keyword prioritizes "Topic" music channels

            print(key)
            if os.path.exists(f'music/{key}.mp3'):
                continue  # Already downloaded

            download_ext = 'm4a'
            download_file = f'music_cache/download/{key}.{download_ext}'
            with YoutubeDL({
                # 'extract-audio': True,
                'format': 'bestaudio[ext=m4a]',
                # 'outtmpl': f'music_cache/download_{name}',
                'outtmpl': download_file,
            }) as dl:
                # df_rel = df[(df.artist_name == artist) & (df.track_name == song)]
                # row = df_rel.iloc[0]

                info = dl.extract_info(url, download=False)
                if info.get('_type') == 'playlist':
                    info = info['entries'][0]

                # print(list(info.keys()))
                print(f'{key} :: {artist} - {song}')
                print(info['title'])
                # print(info['description'])

                if not os.path.exists(download_file):
                    dl.extract_info(url, download=True)

                (AudioSegment
                 .from_file(download_file)
                 .export(f'music/{key}.mp3', format='mp3')
                 )

                # df_features = pd.read_csv('music_features.csv')
                # df_features = pd.concat([
                #     df_features[df_features.index != key],
                #     pd.DataFrame([row])
                # ])
                # df_features.to_csv('music_features.csv', index=False)

                load_spectrogram(key)  # Precompute spectrogram

        # time.sleep(5)

        except Exception as err:
            print(err)
            time.sleep(60)
