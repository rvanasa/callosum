import prelude

import pandas as pd

if __name__ == '__main__':

    # df_spotify = pd.read_csv('data/SpotifyFeatures.csv')

    df_features = pd.read_csv('music_features.csv')

    for _, row in df_features.iterrows():
        name = row['name']

        try:
            # text = ''
            # with open(f'music/lyrics/{name}.txt') as f:
            #     lines = '\n'.join(line for line in f.readlines() if line)
            #     text = ''

            df = pd.DataFrame([
                dict(
                    start=5,
                    duration=2,
                    text='yeah'
                ),
                dict(
                    start=10,
                    duration=2,
                    text='rowdy'
                ),
                dict(
                    start=15,
                    duration=2,
                    text='day'
                )
            ])
            df.to_csv(f'music/words/{name}.csv', index=False)

        except Exception as err:
            print(err)
