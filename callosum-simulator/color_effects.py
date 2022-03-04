import numpy as np
from numba import jit

import colorsys

last_freqs = None
offset = 0
offset_rate = .1

min_frequency = 1000
max_frequency = 8000
n_radial_bands = 20
band_offset_scale = 5
band_offset_rate = .5

special_bands = {
    'Cossack': 7,
    'Bayraktar': 12,
}


def choose_colors(music_name, color_grid, xis, yis, xcs, ycs, angles, radii, spectrum, get_decibel_range, features):
    global last_freqs, offset
    # last_freqs = _globals['last_freqs']
    # offset = _globals['offset']

    f_bands = special_bands.get(music_name) or int(
        n_radial_bands + band_offset_scale * np.sin(offset * band_offset_rate))
    freqs = get_decibel_range(spectrum, min_frequency, max_frequency, f_bands)

    if last_freqs is not None:
        m = np.max(freqs)
        # m = np.max(last_freqs) * np.mean(freqs) / (np.mean(last_freqs) or 1)
        if m > 0:
            freqs /= m

        offset += max(0, np.mean(freqs) - np.mean(last_freqs)) * offset_rate * max(features.danceability * 10, 0)
    # offset -= abs(features.danceability) * offset_rate * .2  #####
    last_freqs = freqs

    spokes = min(6, int(max(0, 1 + features.energy * 5))) if music_name != 'Bayraktar' else 8

    # Optimized parameters
    A = .8 + np.cos(offset * 1.5) * .2
    B = np.sin(offset * 10)
    C = np.sin(offset * 5)

    for xi, yi, angle, r in zip(xis, yis, angles, radii):
        color_grid[xi, yi] = choose_color(spokes, angle, r, freqs, features, A, B, C)

    color_grid **= (2 + features.liveness * .5)  ###


def choose_color(spokes, angle, r, freqs, features, A, B, C):
    # offset = _globals['offset']  #####

    spoke_factor = np.sin((angle * spokes + offset * 5) * 2 * np.pi)

    r += spoke_factor * .2 * A  ####

    # af = freqs[min(int(angle * len(freqs)), len(freqs) - 1)]
    rf = freqs[min(int(r * len(freqs)), len(freqs) - 1)]
    # xf = freqs[min(int(abs(x) * len(freqs)), len(freqs) - 1)]
    # yf = freqs[min(int(abs(y) * len(freqs)), len(freqs) - 1)]

    # hue = angle - (offset + r) * .2  ####
    hue = (290 + np.clip(features.valence * 120 + B * 20, -120, 120)) / 360  ####
    sat = r * .75 + C * .1  # * (.75 + features.valence * 1)
    val = rf ** (2 + features.danceability * .5) + np.sin((angle * 3 + offset * 2) * 2 * np.pi) ** 2 * .1

    # if(rf):
    #     print(rf)

    # print(xi, yi, x, y, theta, r)  ####
    # print(hue, sat, val)

    return colorsys.hsv_to_rgb(hue % 1, np.clip(sat, 0, 1), np.clip(val, 0, 1))
