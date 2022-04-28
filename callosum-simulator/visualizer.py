import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import prelude
from color_effects import choose_colors

import sys
import os
import librosa
import numpy as np
import pandas as pd
import itertools as it
import warnings

from threading import Thread
from queue import Queue
from time import sleep

os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

fullscreen = True

squares_per_letter = 2

music_format = 'mp3'

font_path = 'Arial Rounded MT Bold'

hop_length = 512
n_fft = 1024 * 4
sr = 10000

music_dir = 'music'
words_dir = f'{music_dir}/words'
cache_dir = f'music_cache'
cache_subdir = f'{cache_dir}/{hop_length}_{n_fft}_{sr}'

x_count, y_count = 21, 21

point_pixel_count = 2
point_spread = .4
points_per_square = 7

cover_alpha = .2
audio_time_offset = .09


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
            data, _ = librosa.load(music_path, sr=sr)

        print('Computing STFT...')
        stft = np.abs(librosa.stft(data, hop_length=hop_length, n_fft=n_fft))

        print('Computing spectrogram...')
        spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
        np.save(spectrogram_path, spectrogram)

    return spectrogram


music_queue = Queue()


def run_window():
    icon = pygame.image.load('assets/icon.png')

    pygame.init()
    pygame.mouse.set_visible(not fullscreen)
    pygame.display.set_icon(icon)
    pygame.display.set_caption(f'C A L L O S U M')
    info = pygame.display.Info()
    width, height = int(info.current_w / point_pixel_count), int(info.current_h / point_pixel_count)
    if not fullscreen:
        width = height
    else:
        height += 40  # Windows taskbar
    offset_x = max(0, int((width - height) / 2))
    offset_y = max(0, int((height - width) / 2))
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN if fullscreen else 0)
    time_font = pygame.font.SysFont(font_path, 24)

    grid_size = min(width // x_count, height // y_count)
    grid_width, grid_height = (grid_size, grid_size)

    xs, ys = np.arange(y_count), np.arange(x_count)

    xis, yis = zip(*it.product(xs, ys))
    xis = np.array(xis)
    yis = np.array(yis)

    xcs = (xis + .5) / len(xs) * 2 - 1
    ycs = (yis + .5) / len(ys) * 2 - 1

    angles = np.arctan2(ycs, xcs) / (2 * np.pi) % 1
    radii = np.hypot(xcs, ycs) / np.sqrt(2)

    while True:
        if music_queue.empty():
            sleep(.1)
            continue

        music_name, start_time = music_queue.get()

        screen.fill(0)
        pygame.display.flip()

        print('::', music_name, start_time)

        spectrogram = load_spectrogram(music_name)

        df_features = pd.read_csv('music_features.csv').drop_duplicates('name').set_index('name')
        features = df_features.loc[music_name if music_name in df_features.index else 'default']

        frequencies = librosa.core.fft_frequencies(n_fft=n_fft)
        frequencies_index_ratio = len(frequencies) / frequencies[-1]

        times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sr, hop_length=hop_length, n_fft=n_fft)
        time_index_ratio = len(times) / times[len(times) - 1]

        show_timestamp = False

        def get_spectrum(target_time):
            return spectrogram[:, int(target_time * time_index_ratio) % spectrogram.shape[1]]

        def get_decibel_range(spectrum, min_freq, max_freq, n_chunks=None):
            start = int(min_freq * frequencies_index_ratio)
            end = int(max_freq * frequencies_index_ratio)
            every_nth_sample = 10
            values = spectrum[start:end:every_nth_sample]
            if n_chunks is not None:
                return np.array([t.mean() for t in np.array_split(values, n_chunks)])
            return values

        print('Starting music...')
        pygame.mixer.music.load(_music_path(music_name))
        pygame.mixer.music.play(loops=3, start=start_time)

        color_grid = np.ones((x_count, y_count, 3), dtype=float)
        energy_grid = np.ones((x_count, y_count), dtype=float)

        cover = pygame.Surface((width, height))
        cover.set_alpha(int(cover_alpha * 255))
        cover.fill((0, 0, 0))

        print('Starting visualizer...')
        running = True
        paused = False
        i = 0
        while running:
            i += 1
            if i % 5 == 0 and not music_queue.empty():
                break

            time = start_time + pygame.mixer.music.get_pos() / 1000 + audio_time_offset
            spectrum = get_spectrum(time)
            spectrum -= np.min(spectrum)

            choose_colors(music_name, color_grid, xis, yis, angles, radii, spectrum, get_decibel_range, features)

            next_grid = color_grid
            next_grid *= color_grid  # Square
            for c in range(3):
                next_grid[:, :, c] *= energy_grid
            next_grid -= np.min(next_grid)
            next_grid /= max(1, np.max(next_grid))
            # next_grid *= 1.3  #######
            # next_grid[next_grid > 1] = 1  #########
            next_grid *= 255

            byte_grid = next_grid.astype(np.uint8)

            screen.blit(cover, (0, 0))

            if not paused:
                adjusted_point_spread = point_spread * np.exp2(features.liveness * .4)

                for y in ys:
                    for x in xs:
                        if show_timestamp and x < 1 and y < 1:
                            continue
                        xy_color = byte_grid[x, y]
                        if xy_color.max() < 220:
                            pass
                        for _ in range(points_per_square):
                            screen.set_at((
                                int(offset_x + (
                                        x + .5 + np.random.randn() * adjusted_point_spread) * grid_width) % width,
                                int(offset_y + (
                                        y + .5 + np.random.randn() * adjusted_point_spread) * grid_height) % height,
                            ), xy_color)

            if show_timestamp:
                img = time_font.render(f'{round(time, 1)}', True, (255, 255, 255))
                screen.blit(img, (10, 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        try:
                            pos = pygame.mixer.music.get_pos() / 1000
                            time_increase = 10
                            pygame.mixer.music.set_pos(pos + start_time + time_increase)
                            start_time += time_increase
                        except Exception as e:
                            print(e)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        if paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                elif event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit(0)


_thread = None


def request_visualizer_window():
    global _thread
    if _thread is None:
        _thread = Thread(target=run_window)
        _thread.start()


def start_visualizer(music_name, start_time=0):
    request_visualizer_window()
    music_queue.put((music_name, start_time))


def end_visualizer():
    pygame.quit()


if __name__ == '__main__':
    # Play a specific song from command-line argument
    start_visualizer('Bayraktar' if len(sys.argv) < 2 else sys.argv[1], 0)
