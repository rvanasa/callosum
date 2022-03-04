import prelude
from visualizer import load_spectrogram, has_spectrogram

import time
import pandas as pd
from tqdm import trange

if __name__ == '__main__':

    while True:
        df_features = pd.read_csv('music_features.csv')

        changed = False
        for i in trange(len(df_features)):
            row = df_features.iloc[i]
            name = row['name']
            if name == 'default' or has_spectrogram(name):
                continue
            changed = True
            print()
            print(name)
            load_spectrogram(name)

        if not changed:
            break
        time.sleep(600)
