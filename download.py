import prelude

from pydub import AudioSegment
import numpy as np
import pandas as pd
from youtube_dl import YoutubeDL
import librosa
import soundfile as sf
import warnings
import os

name = 'Alternative'
artist = 'Linkin Park'
song = 'In the End'
url = 'https://www.youtube.com/watch?v=eVTXPUF4Oz4'

# name = 'Arty'
# artist = 'ARTY'
# song = 'Save Me Tonight'
# url = 'https://www.youtube.com/watch?v=TRXod9ILSBk'


def standardize(x):
    return (x - x.mean()) / x.std()


df = pd.read_csv('data/SpotifyFeatures.csv')
df.loc[df.genre == 'Children’s Music', 'genre'] = 'Children\'s Music'  # Consistent apostrophes
keys = ['danceability', 'energy', 'liveness', 'valence']
df = df[['genre', 'artist_name', 'track_name', *keys]].copy()
df.drop_duplicates(['artist_name', 'track_name', *keys], inplace=True)
df.liveness = np.log(df.liveness)

for key in keys:
    df[key] = standardize(df[key])

if __name__ == '__main__':
    download_ext = 'mp4'
    download_file = f'music_cache/_download_{name}.{download_ext}'
    with YoutubeDL({
        'extract-audio': True,
        'audio-format': download_ext,
        'outtmpl': f'music_cache/_download_{name}',
    }) as dl:
        df_rel = df[(df.artist_name == artist) & (df.track_name == song)]
        assert len(df_rel) == 1, f'Relevant options: {df_rel[["genre", "track_name", "artist_name"]]}'
        row = df_rel.iloc[0]

        info = dl.extract_info(url, download=False)
        # print(list(info.keys()))
        print(f'{name} :: {artist} - {song}')
        print(info['title'])
        # print(info['description'])

        if not os.path.exists(download_file):
            dl.extract_info(url, download=True)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            audio, sr = librosa.load(download_file, sr=16000)

        # Convert from .{download_ext} -> .wav -> .mp3
        sf.write(f'music/{name}.wav', audio, sr)
        AudioSegment.from_wav(f'music/{name}.wav').export(f'music/{name}.mp3', format='mp3')
        os.remove(f'music/{name}.wav')

        # AudioSegment.from_file(download_file, format=download_ext).export(f'music/{name}.mp3', format='mp3')

        # sf.write(f'music/{name}.ogg', audio, sr)

        df_features = pd.read_csv('music_features.csv')
        df_features = pd.concat([
            df_features[df_features.name != name],
            pd.DataFrame([dict(
                name=name,
                artist=artist,
                song=song,
                **{key: row[key] for key in keys}
            )])
        ])
        df_features.to_csv('music_features.csv', index=False)
