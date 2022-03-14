import prelude

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_ID'),
    client_secret=os.getenv('SPOTIFY_SECRET'),
))


def get_features(name, genre, track_id):
    # df_tracks = pd.DataFrame(sp.search('Conrad Sewell Hold Me Up Throttle', type='track')['tracks']['items'])
    # df_tracks[:3]

    # print(len(df_tracks))  ##

    # track = df_tracks.iloc[0]

    track = pd.Series(sp.track(track_id))

    artist = track['artists'][0]['name']
    name = track['name']

    # print(artist, '-', name)

    # df_features = pd.read_csv('music_features.csv')

    # print(','.join(track[[df_features.columns]]))

    all_features = sp.audio_features(track_id)
    # print(len(all_features))
    features = pd.Series(all_features[0])

    row = pd.Series(dict(
        name=name,
        genre=genre,
        artist=artist,
        song=name,
        **{k: features[k] for k in ['danceability', 'energy', 'liveness', 'valence']}
    ))
    return row


if __name__ == '__main__':
    df_tracks = pd.DataFrame(sp.search('Conrad Sewell Hold Me Up Throttle', type='track')['tracks']['items'])
    # df_tracks[:3]

    print(len(df_tracks))  ##

    track = df_tracks.iloc[0]

    artist = track.artists[0]['name']
    name = track['name']

    print(artist, '-', name)

    df_features = pd.read_csv('music_features.csv')

    # print(','.join(track[[df_features.columns]]))

    all_features = sp.audio_features(track.id)
    print(len(all_features))
    features = all_features[0]

    print(','.join(str(features[s]) for s in ['danceability', 'energy', 'liveness', 'valence']))

    # analysis = sp.audio_analysis(track.id)
