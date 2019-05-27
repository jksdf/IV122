from typing import List

from PIL import Image


def save_gif(imgs: List[Image.Image], fn: str, duration=100, loop=1):
    imgs[0].save(fn, format='GIF', append_images=imgs[1:], save_all=True, duration=duration, loop=loop)
