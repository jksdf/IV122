import math
import warnings

from PIL import Image

from Base import Base, AbstractFilenameProvider


def sigmoid(x, ):
    if math.isnan(x):
        warnings.warn("NaN")
        return 1
    return 1 / (1 + math.exp(-x))


def mandelbrot_simple(data, distance):
    if abs(data) <= 2:
        return 0, 0, 0


def mandelbrot_finaldist(data, distance):
    if abs(data) <= 2:
        return 0, 0, 0
    else:
        color = sigmoid(math.log(abs(data)) / 245)
        return int(255 * color), 255, 255


def mandelbrot_avgdist(data, distance):
    is_mandelbrot = abs(data) <= 2
    color = [255, 255, 255]
    if is_mandelbrot:
        c = distance / 2
    else:
        try:
            c = sigmoid(math.log(abs(distance)) / 250)
        except ValueError:
            c = 1
    c = int(255 * c)
    color[0 if is_mandelbrot else 1] = c
    return tuple(color)


MANDELBROT_COLORINGS = {"simple": mandelbrot_simple,
                        "simple+finaldist": mandelbrot_finaldist,
                        "avgdist": mandelbrot_avgdist}


def mandelbrot(n: int, res: int, coloring, mode: str, julius_init=None):
    assert coloring in MANDELBROT_COLORINGS.keys()

    def transform_coords(x, y):
        return (x - res / 2) / (res / 4) + (y - res / 2) / (res / 4) * 1j

    if mode == 'mandelbrot':
        def init(x, y):
            return 0 + 0j

        def c(x, y):
            return transform_coords(x, y)
    elif mode == 'julius':
        def init(x, y):
            return transform_coords(x, y)

        def c(x, y):
            return julius_init
    else:
        raise ValueError

    distances = [[0.] * res for _ in range(res)]
    data = [[init(x, y) for x in range(res)] for y in range(res)]
    for _ in range(n):
        for y in range(res):
            for x in range(res):
                old = data[y][x]
                data[y][x] = data[y][x] * data[y][x] + c(x, y)
                if math.isnan(data[y][x].imag) or math.isnan(data[y][x].real):
                    data[y][x] = old
                try:
                    distances[y][x] += abs(data[y][x])
                except OverflowError:
                    data[y][x] = complex(float('inf'), float('inf'))
                    distances[y][x] = float('inf')
    for y in range(res):
        for x in range(res):
            if math.isnan(distances[y][x]):
                distances[y][x] = float('inf')
            distances[y][x] /= n
    img = Image.new("RGB", (res, res), color=(255, 255, 255))
    fn = MANDELBROT_COLORINGS.get(coloring)
    for y in range(res):
        for x in range(res):
            try:
                val = fn(data[y][x], distances[y][x])
                if val is not None:
                    img.putpixel((x, y), val)
            except Exception as e:
                warnings.warn("issue in mandelbrot")
                raise e
    return img


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        res = 500
        mandelbrot(20, res, 'simple', 'mandelbrot').save(fnprovider.get_filename(".png", "mandelbrot", "Mandelbrot"))
        mandelbrot(15, res, 'simple+finaldist', 'mandelbrot').save(
            fnprovider.get_filename(".png", "mandelbrot_final_dist", "Mandelbrot with final distances"))
        mandelbrot(20, res, 'avgdist', 'mandelbrot').save(
            fnprovider.get_filename(".png", "mandelbrot_avgdist", "Mandelbrot with average distances"))

        julius_init = -0.13 + 0.75j
        mandelbrot(20, res, 'simple', 'julius', julius_init=julius_init).save(
            fnprovider.get_filename(".png", "julius", "Julius"))
        mandelbrot(15, res, 'simple+finaldist', 'julius', julius_init=julius_init).save(
            fnprovider.get_filename(".png", "julius_final_dist", "Julius with final distances"))
        mandelbrot(20, res, 'avgdist', 'julius', julius_init=julius_init).save(
            fnprovider.get_filename(".png", "julius_avgdist", "Julius with average distances"))
        return fnprovider.format_files()
