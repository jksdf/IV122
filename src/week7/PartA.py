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


def mandelbrot(n: int, res: int, coloring):
    assert coloring in MANDELBROT_COLORINGS.keys()
    distances = [[0.] * res for _ in range(res)]
    data = [[0 + 0j for _ in range(res)] for _ in range(res)]
    for _ in range(n):
        for y in range(res):
            for x in range(res):
                old = data[y][x]
                data[y][x] = data[y][x] * data[y][x] + ((x - res / 2) + (y - res / 2) * 1j) / (res / 4)
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
        mandelbrot(20, 500, 'simple').save(fnprovider.get_filename(".png", "mandelbrot", "Mandelbrot"))
        mandelbrot(15, 500, 'simple+finaldist').save(
            fnprovider.get_filename(".png", "mandelbrot_final_dist", "Mandelbrot with final distances"))
        mandelbrot(20, 500, 'avgdist').save(
            fnprovider.get_filename(".png", "mandelbrot_avgdist", "Mandelbrot with average distances"))
        return fnprovider.format_files()
