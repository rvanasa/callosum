import numpy as np
import pandas as pd
from youtube_dl import YoutubeDL
import librosa
import soundfile as sf
import warnings
import os

artist = 'David Bowie'
song = 'Starman - 2012 Remastered Version'
url = 'https://www.youtube.com/watch?v=aBKEt3MhNMM'

name = 'Starman'


def standardize(x):
    return (x - x.mean()) / x.std()


df = pd.read_csv('data/SpotifyFeatures.csv')
keys = ['danceability', 'energy', 'liveness', 'valence']  # , 'popularity'
df = df[['genre', 'artist_name', 'track_name', *keys]].copy()
df.drop_duplicates(['artist_name', 'track_name', *keys], inplace=True)
df.liveness = np.log(df.liveness)

for key in keys:
    df[key] = standardize(df[key])

if __name__ == '__main__':
    download_ext = 'mkv'
    download_file = f'music_cache/_download.{download_ext}'
    with YoutubeDL({
        'extract-audio': True,
        # 'audio-format': f'bestaudio[ext={download_ext}]',
        # 'audio-format': f'bestaudio[ext={download_ext}]',
        'outtmpl': 'music_cache/_download',
    }) as dl:
        df_rel = df[(df.artist_name == artist) & (df.track_name == song)]
        assert len(df_rel) == 1, f'Relevant options: {df_rel[["genre", "track_name", "artist_name"]]}'
        row = df_rel.iloc[0]

        info = dl.extract_info(url, download=False)
        # print(list(info.keys()))
        print(f'{name} ({artist} - {song})')
        print(info['title'])
        # print(info['description'])

        # input('Press ENTER to download:')
        # dl.extract_info(url, download=True)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            audio, sr = librosa.load(download_file, sr=16000)

        sf.write(f'music/{name}.wav', audio, sr)
        # sf.write(f'music/{name}.ogg', audio, sr)

        df_features = pd.read_csv('music_features.csv')
        df_features = pd.concat([
            df_features[df_features.name != name],
            pd.DataFrame([dict(
                name=name,
                **{key: row[key] for key in keys}
            )])
        ])
        df_features.to_csv('music_features.csv', index=False)
