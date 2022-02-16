import sys
import os
import librosa
import numpy as np
import pandas as pd
import itertools as it
from numba import jit

from color_effects import choose_colors

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

# Fear not, for this will be properly commented.
# Waiting to document until after we refactor for the Arduino serial interface.

music_name = 'Abba' if len(sys.argv) < 2 else sys.argv[1]
start_time = 0 if len(sys.argv) < 3 else float(sys.argv[2])

font_path = 'Arial Rounded MT Bold.ttf'  # TODO: custom font

with open('wordsearch.txt') as f:
    lines = list(f.readlines())
    wordsearch = np.array([list(line.strip().upper()) for line in lines if line and not line.startswith('#')])

df_solutions = pd.read_csv('wordsearch_solution.csv').set_index('word')

width, height = 600, 600
x_count, y_count = 30, 30

# x_count, y_count = np.array(wordsearch.shape)[::-1]
grid_size = 600 / x_count
# x_count, y_count = 20, 20
# width, height = np.array([x_count, y_count]) * grid_size

hop_length = 512
# n_fft = 2048 * 4
n_fft = 1024 * 4
sr = 10000

dampen = .005
min_brightness = 0
audio_time_offset = .08

music_dir = 'music'
cache_dir = f'music_cache'
cache_subdir = f'{cache_dir}/{hop_length}_{n_fft}_{sr}'
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)
if not os.path.exists(cache_subdir):
    os.mkdir(cache_subdir)

music_path = f'{music_dir}/{music_name}.ogg'
spectrogram_path = f'{cache_subdir}/{music_name}.npy'
if os.path.exists(spectrogram_path):
    spectrogram = np.load(spectrogram_path)
else:
    print('Loading music...')
    # with warnings.catch_warnings():
    #     warnings.simplefilter('ignore')
    data, sr = librosa.load(music_path, sr=sr)  # , duration=30

    print('Computing STFT...')
    stft = np.abs(librosa.stft(data, hop_length=hop_length, n_fft=n_fft))

    print('Computing spectrogram...')
    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
    np.save(spectrogram_path, spectrogram)

df_features = pd.read_csv('music_features.csv').set_index('name').astype(float)
features = df_features.loc[music_name if music_name in df_features.index else 'default']

lyrics_path = music_path.replace('.ogg', '.csv')
lyrics = [row for _, row in pd.read_csv(lyrics_path).sort_values('start').iterrows()] \
    if os.path.exists(lyrics_path) else []
# lyrics = []

frequencies = librosa.core.fft_frequencies(n_fft=n_fft)
frequencies_index_ratio = len(frequencies) / frequencies[-1]

times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sr, hop_length=hop_length, n_fft=n_fft)
time_index_ratio = len(times) / times[len(times) - 1]

show_letters = False
show_timestamp = True


@jit(nopython=True)
def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio), int(target_time * time_index_ratio)]


@jit(nopython=True)
def get_spectrum(target_time):
    return spectrogram[:, int(target_time * time_index_ratio) % spectrogram.shape[1]]


@jit(nopython=True)
def get_decibel_range(spectrum, min_freq, max_freq, n_chunks=None):
    start = int(min_freq * frequencies_index_ratio)
    end = int(max_freq * frequencies_index_ratio)
    values = spectrum[start:end]
    if n_chunks is not None:
        return np.array([t.mean() for t in np.array_split(values, n_chunks)])
    return values


def main():
    global show_letters
    pygame.init()
    screen = pygame.display.set_mode([width, height])
    time_font = pygame.font.SysFont(font_path, 24)  ####

    ws_size = 48
    ws_font = pygame.font.SysFont(font_path, ws_size)  ####

    grid_width, grid_height = width // x_count, height // y_count
    grid_margin = 2

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

    rectangles = np.array([
        [pygame.Rect(x, y, grid_width, grid_height).inflate(-grid_margin, -grid_margin)
         for y in row_ys] for x in col_xs])

    time_rect = pygame.Rect(0, 0, grid_width * 3, grid_height * 2)

    print('Starting music...')
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loops=3, start=start_time)

    color_grid = np.ones((x_count, y_count, 3), dtype=float)
    energy_grid = np.ones((x_count, y_count), dtype=float)

    x_center = 2 * col_xs / width - 1
    y_center = 2 * row_ys / height - 1
    # radius_grid = np.sqrt(x_center ** 2 + y_center ** 2)

    next_grid = np.zeros(color_grid.shape)

    print('Starting visualizer...')
    last_ticks = pygame.time.get_ticks()
    running = True
    while running:
        ticks = pygame.time.get_ticks()
        delta_time = (ticks - last_ticks) / 1000
        last_ticks = ticks

        time = start_time + pygame.mixer.music.get_pos() / 1000 + audio_time_offset
        spectrum = get_spectrum(time)
        spectrum = spectrum - np.min(spectrum)  ########

        choose_colors(color_grid, xis, yis, xcs, ycs, angles, radii, spectrum, get_decibel_range, features)

        # color_grid[yi, xi] = colorsys.hsv_to_rgb(hue, sat, val)
        # energy_grid[yi, xi] = 1  # + radii_center[i, j]

        # for y in ys:
        #     yf = y / len(ys)
        #     yc = yf * 2 - 1
        #
        #     fy = f[y]
        #     # print(f_col)  ###
        #     for theta, r in zip(thetas, radii):
        #         xf = x / len(xs)
        #         xc = xf * 2 - 1
        #
        #         r = np.hypot(xc, yc)

        # Compute next color values in place

        next_grid *= dampen
        next_grid += color_grid
        for c in range(3):
            next_grid[:, :, c] *= energy_grid
        next_grid -= np.min(next_grid)
        next_grid /= max(1, np.max(next_grid))
        next_grid *= 255 - min_brightness
        next_grid += min_brightness
        next_grid = next_grid

        screen.fill((0, 0, 0))

        # if show_text:
        #     np.random.seed(0)  ####

        text = None
        solution = None
        if lyrics:
            row = lyrics[0]
            if time >= row.start:
                text = row.text.upper()
                if text in df_solutions.index:
                    solution = df_solutions.loc[text]
                if time >= row.start + row.duration:
                    lyrics.pop(0)

        for y in ys:
            for x in xs:
                if show_timestamp and x < 1 and y < 1:
                    continue
                letter = wordsearch[y, x] if x < wordsearch.shape[0] and y < wordsearch.shape[1] else ''
                xy_color = next_grid[x, y].astype(int)
                if text is not None and solution is not None:
                    flag = True
                    for i in range(len(text)):
                        if y == solution.x + solution.dx * i and x == solution.y + solution.dy * i:
                            flag = False
                            break
                    if flag:
                        xy_color = (0, 0, 0)
                if show_letters:
                    img = ws_font.render(letter, True, xy_color)
                    screen.blit(img, (
                        col_xs[x] + (grid_size - img.get_width()) / 2,
                        row_ys[y] + (grid_size - img.get_height()) / 2,
                    ))
                else:
                    screen.fill(xy_color, rectangles[x, y])

        # screen.fill((0, 0, 0), time_rect)

        if show_timestamp:
            img = time_font.render(f'{round(time, 1)}', True, (255, 255, 255))
            screen.blit(img, (10, 10))

        # if lyrics:
        #     row = lyrics[0]
        #     if time >= row.start:
        #         screen_size = np.asarray((width, height)) - 5
        #         text = row.text.upper()
        #         if lyric_img is None:
        #             font_size = 180
        #             while lyric_img is None or np.any(np.asarray(lyric_img.get_size()) > screen_size):
        #                 lyric_font = pygame.font.SysFont('C:\\Windows\\Fonts\\Arial.ttf', font_size)  ####
        #                 font_size -= 4
        #                 lyric_img = lyric_font.render(f'{text}', True, (0, 0, 0))
        #
        #         # img_bg = lyric_font.render(f'{text}', True, (0, 0, 0))
        #         img_width, img_height = lyric_img.get_size()
        #         img_x = (width - img_width) / 2
        #         img_y = (height - img_height) / 2
        #         # screen.blit(img_bg, (img_x + 2, img_y + 2))
        #         screen.blit(lyric_img, (img_x, img_y))
        #
        #         if time >= row.start + row.duration:
        #             lyric_img = None
        #             lyrics.pop(0)

        pygame.display.flip()

        # if i % 10 == 0:
        #     pygame.image.save(screen, f'output/{}.jpg')
        # i += 1

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_letters = not show_letters
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    main()
