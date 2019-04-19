import random
from typing import List

import numpy as np
from PIL import Image

from Base import Base, AbstractFilenameProvider


def _rotate(vector, degrees):
    x, y = vector
    c, s = np.cos(np.deg2rad(degrees)), np.sin(np.deg2rad(degrees))
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])
    return np.array([m.T[0, 0], m.T[1, 0]])


def chaos_game(n, step, k, r, seed=None, size=400):
    random.seed(seed)
    imgs = [Image.new(mode="L", size=(size, size), color=255)]
    abc = [np.array([size / 2, size / 2]) + _rotate((0, -size / 2 * 0.9), i * 360 / n) for i in range(n)]
    x = np.array([size / 2, size / 2])
    for _ in range(k):
        img = imgs[-1].copy()
        imgs.append(img)
        for _ in range(step):
            x = x * (1-r) + random.choice(abc) * r
            img.putpixel((int(x[0]), int(x[1])), 0)
    return imgs


def save_gif(imgs: List[Image.Image], fn: str, duration=100, loop=1):
    imgs[0].save(fn, format='GIF', append_images=imgs[1:], save_all=True, duration=duration, loop=loop)


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        save_gif(chaos_game(3, 10000, 10, 1 / 2),
                 fnprovider.get_filename('.gif', 'chaos_triangle', 'Chaos triangle (n=3, r=1/2)'))
        save_gif(chaos_game(5, 10000, 50, 1 / 2),
                 fnprovider.get_filename('.gif', 'chaos_pentagon', 'Chaos pentagon (n=3, r=1/2)'),
                 duration=100)
        save_gif(chaos_game(5, 10000, 50, 1 / 3),
                 fnprovider.get_filename('.gif', 'chaos_pentagon_third', 'Chaos pentagon (n=3, r=1/3)'),
                 duration=100)
        return fnprovider.format_files()
