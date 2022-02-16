import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv

load_dotenv('.env.local')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_ID'),
    client_secret=os.getenv('SPOTIFY_SECRET'),
))

df_tracks = pd.DataFrame(sp.search('', type='track')['tracks']['items'])
# df_tracks[:3]

track = df_tracks.iloc[0]

artist = track.artists[0]['name']
name = track['name']

print(artist, '-', name)

# features = sp.audio_features(track.id)
# analysis = sp.audio_analysis(track.id)
