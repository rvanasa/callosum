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


# https://spotifycharts.com/regional/global/daily/latest/download
df_charts = pd.read_csv('data/regional-global-daily-latest.csv', skiprows=1)
df_charts['track_id'] = df_charts.URL.str[31:]
df_charts.set_index('track_id', inplace=True)

if __name__ == '__main__':

    for track_id, chart_row in df_charts.iterrows():
        try:
            name = f'charts/{track_id}'
            genre = 'Recent'
            artist = chart_row['Artist']
            song = chart_row['Track Name']

            row = get_features(name, genre, track_id)

            # genre = row.genre
            url = f'ytsearch:{artist} topic - {song}'  # 'topic' keyword prioritizes "Topic" music channels

            print(name)  ##
            if os.path.exists(f'music/{name}.mp3'):
                continue  # Already downloaded

            download_ext = 'm4a'
            download_file = f'music_cache/download/{name}.{download_ext}'
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
                print(f'{name} :: {artist} - {song}')
                print(info['title'])
                # print(info['description'])

                if not os.path.exists(download_file):
                    dl.extract_info(url, download=True)

                (AudioSegment
                 .from_file(download_file)
                 .export(f'music/{name}.mp3', format='mp3')
                 )

                df_features = pd.read_csv('music_features.csv')
                df_features = pd.concat([
                    df_features[df_features.name != name],
                    pd.DataFrame([row])
                ])
                df_features.to_csv('music_features.csv', index=False)

                load_spectrogram(name)  # Precompute spectrogram

        # time.sleep(5)

        except Exception as err:
            print(err)
            time.sleep(60)
