import prelude
from visualizer import load_spectrogram

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


df_charts = pd.read_csv('https://spotifycharts.com/regional/global/daily/latest/download')

print(df_charts)

if __name__ == '__main__':

    groups = df.sort_values('popularity', ascending=False).drop_duplicates(['artist_name']).groupby('genre')
    for genre, g in groups:
        for key, row in g[:40].iterrows():
            try:
                name = f'spotify/{key}'
                genre = row.genre
                artist = row.artist_name
                song = row.track_name
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
                    df_rel = df[(df.artist_name == artist) & (df.track_name == song)]
                    row = df_rel.iloc[0]

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
                        pd.DataFrame([dict(
                            name=name,
                            genre=genre,
                            artist=artist,
                            song=song,
                            **{key: row[key] for key in keys}
                        )])
                    ])
                    df_features.to_csv('music_features.csv', index=False)

                    load_spectrogram(name)  # Precompute spectrogram

            # time.sleep(5)

            except Exception as err:
                print(err)
                time.sleep(60)
