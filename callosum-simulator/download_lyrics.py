import prelude

import os
import time
import numpy as np
import pandas as pd
import lyricsgenius

lg = lyricsgenius.Genius(os.getenv('GENIUS_KEY'))

if __name__ == '__main__':

    while True:
        try:
            df_features = pd.read_csv('music_features.csv')

            for _, row in df_features.iterrows():
                name = row['name']
                if name == 'default':
                    continue

                output_file = f'music/lyrics/{name}.txt'
                if os.path.exists(output_file):
                    continue

                lyric_results = lg.search_songs(f'{row.artist} - {row.song}')

                print()
                print(f'{row.artist} - {row.song} [{name}]')
                df_results = pd.DataFrame([r['result'] for r in lyric_results['hits']])
                if len(df_results):
                    print(df_results[:2][['artist_names', 'full_title']])  ##

                    lyric_result = df_results.iloc[0]
                    # lyric_result.to_dict()

                    title = lyric_result.full_title
                    lyrics = lg.lyrics(lyric_result['id']) or ''
                    lyrics = lyrics.encode('utf-8').decode('utf-8')  # Convert to UTF-8
                else:
                    title = ''
                    lyrics = ''

                with open(output_file, 'w+', encoding='utf-8') as f:
                    # f.write(f'{row.artist} - {row.song}')
                    if title:
                        f.write(title)
                        f.write('\n\n')
                    f.write(lyrics)

                time.sleep(10)  ###

        except Exception as err:
            print(err)

        break
        # time.sleep(300)  ###
