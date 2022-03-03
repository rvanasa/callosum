import prelude

from pydub import AudioSegment
import numpy as np
import pandas as pd
from youtube_dl import YoutubeDL
import librosa
import soundfile as sf
import warnings
import os
import time


# name = 'Test'
# artist = 'Test'
# song = 'Test'
# url = 'https://www.youtube.com/watch?v=Wch3gJG2GJ4'


def standardize(x):
    return (x - x.mean()) / x.std()


df = pd.read_csv('data/SpotifyFeatures.csv')
df.loc[df.genre == 'Children’s Music', 'genre'] = 'Children\'s Music'  # Consistent apostrophes
df = df[df.genre != 'Children\'s Music']
keys = ['danceability', 'energy', 'liveness', 'valence']
df = df[['genre', 'artist_name', 'track_name', 'popularity', *keys]].copy()
df = df.sort_values('popularity', ascending=False)
df.drop_duplicates(['artist_name', 'track_name'], keep='first', inplace=True)
df.liveness = np.log(df.liveness)

for key in keys:
    df[key] = standardize(df[key])

if __name__ == '__main__':

    while True:
        try:
            groups = df.sort_values('popularity', ascending=False).drop_duplicates(['artist_name']).groupby('genre')
            for genre, g in groups:
                for key, row in g[:15].iterrows():
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

                    # time.sleep(5)

        except Exception as err:
            print(err)
        # time.sleep(60)

        break
