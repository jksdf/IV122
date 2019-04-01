import math
import warnings

from PIL import Image

from Base import Base, AbstractFilenameProvider


def sigmoid(x, ):
    if math.isnan(x):
        warnings.warn("NaN")
        return 1
    return 1 / (1 + math.exp(-x))


def mandelbrot(n: int, res: int, coloring):
    distances = [[0] * res for _ in range(res)]
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
    for y in range(res):
        for x in range(res):
            try:
                if coloring == 'simple':
                    if abs(data[y][x]) <= 2:
                        img.putpixel((x, y), (0, 0, 0))
                elif coloring == 'simple+finaldist':
                    if abs(data[y][x]) <= 2:
                        img.putpixel((x, y), (0, 0, 0))
                    else:
                        color = sigmoid(math.log(abs(data[y][x])) / 245)
                        img.putpixel((x, y), (int(255 * color), 255, 255))
                elif coloring == 'avgdist':
                    is_mandelbrot = abs(data[y][x]) <= 2
                    color = [255, 255, 255]
                    if is_mandelbrot:
                        c = distances[y][x] / 2
                        print(c)
                    else:
                        try:
                            c = sigmoid(math.log(abs(distances[y][x])) / 250)
                        except ValueError:
                            c = 1
                    c = int(255 * c)
                    color[0 if is_mandelbrot else 1] = c
                    img.putpixel((x, y), tuple(color))
                else:
                    raise Exception("Bad coloring " + coloring)
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
