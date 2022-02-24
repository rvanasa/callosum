import prelude

import os
import numpy as np
import pandas as pd
import lyricsgenius

name = 'Surprise'

lg = lyricsgenius.Genius(os.getenv('GENIUS_KEY'))

lyric_results = lg.search_songs(f'Rick Astley - Never Gonna Give You Up')

df_results = pd.DataFrame([r['result'] for r in lyric_results['hits']])
print(df_results[:3])  ##
print()

lyric_result = df_results.iloc[1]
lyric_result.to_dict()

lyrics = lg.lyrics(lyric_result['id'])

print(lyrics)
