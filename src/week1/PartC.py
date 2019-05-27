import numpy as np
from PIL import Image

from Base import Base
from common.math.Fibonacci import Fibonacci
from common.math.factorization import isprime
from common.math.ulam import create_ulam


class PartC(Base):
    name = 'C'

    def run(self, fnprovider):
        size = 500
        ulam = create_ulam(size)

        Image.fromarray(np.uint8(np.vectorize(isprime)(ulam)) * 255, 'L').save(fnprovider.get_filename('.png', 'prime'))

        Image.fromarray(np.uint8(ulam % 5 == 0) * 255, 'L').save(fnprovider.get_filename('.png', 'div5'))

        Image.fromarray(np.uint8(ulam % 8 == 0) * 255, 'L').save(fnprovider.get_filename('.png', 'div8'))

        fib = Fibonacci()
        Image.fromarray(np.uint8(np.vectorize(fib.__contains__)(ulam)) * 255, 'L').save(
            fnprovider.get_filename('.png', 'fib'))

        small_ulam = create_ulam(50)
        Image.fromarray(np.uint8(np.vectorize(fib.__contains__)(small_ulam)) * 255, 'L').save(
            fnprovider.get_filename('.png', 'fib_small'))

        return fnprovider.format_files()
