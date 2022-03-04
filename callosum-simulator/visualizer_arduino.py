import prelude
from color_effects import choose_colors
from arduino import send_data, is_open

import sys
import os
import librosa
import numpy as np
import pandas as pd
import itertools as it
from numba import jit
import warnings

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

# pixels_per_letter = 2
# show_lyrics = False

music_format = 'mp3'

# font_path = 'Arial Rounded MT Bold'

hop_length = 512
n_fft = 1024 * 4
sr = 10000

music_dir = 'music'
words_dir = f'{music_dir}/words'
cache_dir = f'music_cache'
cache_subdir = f'{cache_dir}/{hop_length}_{n_fft}_{sr}'

current_screen = None


def _music_path(music_name):
    return f'{music_dir}/{music_name}.{music_format}'


def has_spectrogram(music_name):
    return os.path.exists(f'{cache_subdir}/{music_name.replace("/", "_")}.npy')


def load_spectrogram(music_name):
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    if not os.path.exists(cache_subdir):
        os.mkdir(cache_subdir)

    music_path = _music_path(music_name)
    spectrogram_path = f'{cache_subdir}/{music_name.replace("/", "_")}.npy'
    if os.path.exists(spectrogram_path):
        spectrogram = np.load(spectrogram_path)
    else:
        print('Loading music...')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            data, _ = librosa.load(music_path, sr=sr)  # , duration=30

        print('Computing STFT...')
        stft = np.abs(librosa.stft(data, hop_length=hop_length, n_fft=n_fft))

        print('Computing spectrogram...')
        spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
        np.save(spectrogram_path, spectrogram)

    return spectrogram


def start_visualizer(music_name, start_time=0):
    global current_screen
    if not music_name or music_name == 'default':
        return end_visualizer()
    if current_screen:
        end_visualizer()  # Replace visualizer

    # music_name = default_music_name# if len(sys.argv) < 2 else sys.argv[1]
    # start_time = default_start_time# if len(sys.argv) < 3 else float(sys.argv[2])

    with open('wordsearch.txt') as f:
        lines = list(f.readlines())
        wordsearch = np.array([list(line.strip().upper()) for line in lines if line and not line.startswith('#')])

    df_solutions = pd.read_csv('wordsearch_solutions.csv').set_index('word')

    width, height = 600, 600
    x_count, y_count = 30, 30

    dampen = .01
    min_brightness = 0
    audio_time_offset = .09

    pygame.init()

    spectrogram = load_spectrogram(music_name)

    df_features = pd.read_csv('music_features.csv').set_index('name')
    features = df_features.loc[music_name if music_name in df_features.index else 'default']

    frequencies = librosa.core.fft_frequencies(n_fft=n_fft)
    frequencies_index_ratio = len(frequencies) / frequencies[-1]

    times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sr, hop_length=hop_length, n_fft=n_fft)
    time_index_ratio = len(times) / times[len(times) - 1]

    show_letters = False
    show_timestamp = False

    def get_decibel(target_time, freq):
        return spectrogram[int(freq * frequencies_index_ratio), int(target_time * time_index_ratio)]

    def get_spectrum(target_time):
        return spectrogram[:, int(target_time * time_index_ratio) % spectrogram.shape[1]]

    def get_decibel_range(spectrum, min_freq, max_freq, n_chunks=None):
        start = int(min_freq * frequencies_index_ratio)
        end = int(max_freq * frequencies_index_ratio)
        # every_nth_sample = 2
        every_nth_sample = 10
        values = spectrum[start:end:every_nth_sample]
        if n_chunks is not None:
            return np.array([t.mean() for t in np.array_split(values, n_chunks)])
        return values

    grid_width, grid_height = width // x_count, height // y_count
    grid_margin = 4

    xs, ys = np.arange(y_count), np.arange(x_count)
    row_ys, col_xs = np.arange(y_count) * grid_height, np.arange(x_count) * grid_width

    xis, yis = zip(*it.product(xs, ys))
    xis = np.array(xis)
    yis = np.array(yis)

    xcs = (xis + .5) / len(xs) * 2 - 1
    ycs = (yis + .5) / len(ys) * 2 - 1

    # xcs +=  features.danceability * .5
    # ycs +=  features.liveness * .5

    angles = np.arctan2(ycs, xcs) / (2 * np.pi) % 1
    radii = np.hypot(xcs, ycs) / np.sqrt(2)

    print('Starting music...')
    pygame.mixer.music.load(_music_path(music_name))
    pygame.mixer.music.play(loops=3, start=start_time)

    color_grid = np.ones((x_count, y_count, 3), dtype=float)
    energy_grid = np.ones((x_count, y_count), dtype=float)

    # x_center = 2 * col_xs / width - 1
    # y_center = 2 * row_ys / height - 1
    # radius_grid = np.sqrt(x_center ** 2 + y_center ** 2)

    next_grid = np.zeros(color_grid.shape)

    print('Starting visualizer...')
    last_ticks = pygame.time.get_ticks()
    running = True
    while running:
        ticks = pygame.time.get_ticks()
        # delta_time = (ticks - last_ticks) / 1000
        last_ticks = ticks

        time = start_time + pygame.mixer.music.get_pos() / 1000 + audio_time_offset
        spectrum = get_spectrum(time)
        spectrum -= np.min(spectrum)

        choose_colors(music_name, color_grid, xis, yis, xcs, ycs, angles, radii, spectrum, get_decibel_range, features)

        if music_name in ['Ukraine', 'Cossack', 'Bayraktar']:
            color_grid[:, :, 1] = color_grid[:, :, 0]
            color_grid[:, :, 2] = color_grid[:, :, 0]

        # Compute next color values in place

        next_grid *= dampen / np.exp2(features.energy)
        next_grid += color_grid
        for c in range(3):
            next_grid[:, :, c] *= energy_grid
        next_grid -= np.min(next_grid)
        if show_letters:
            next_grid += np.max(next_grid) * .2  ###
        next_grid /= max(1, np.max(next_grid))
        next_grid *= 255 - min_brightness
        next_grid += min_brightness

        byte_grid = next_grid.astype(np.uint8)  ##

        color_max = np.max(next_grid[0, 0])
        color_prefix = ((next_grid[0, 0] / color_max) if color_max else np.zeros(3)).astype(np.uint8)
        print(color_prefix)
        assert len(color_prefix.tobytes()) == 3

        byte_grid = byte_grid[:, :, 0]  ####

        # if is_open():
        data = b'ABCDEFGH' + color_prefix.tobytes() + bytes(byte_grid.flatten().tobytes())  # [:150 * 3]  ########
        send_data(data)

    pygame.quit()


def end_visualizer():
    global current_screen
    if current_screen is not None:
        current_screen = None
        pygame.quit()


if __name__ == '__main__':
    # Play a specific song
    start_visualizer('ViolinDubstep' if len(sys.argv) < 2 else sys.argv[1], 0)
