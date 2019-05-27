import numpy as np
from PIL import Image

from Base import Base
from common.math.factorization import gcd_mod, gcd_sub


class PartD(Base):
    name = 'D'

    def run(self, fnprovider):
        fns = {}

        size = 1500

        fn = fnprovider.get_filename('.png', 'pairwise')
        fns['Are pairwise divisible'] = fn
        Image.fromarray(
            np.fromfunction(lambda x, y: 255 * np.uint8(np.gcd(x + 1, y + 1) != 1), shape=(size, size),
                            dtype=np.uint32),
            'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcd')
        fns['GCD / MAX'] = fn
        Image.fromarray(
            np.fromfunction(lambda x, y: np.uint8(np.gcd(x + 1, y + 1) * 255 / np.maximum(x + 1, y + 1)),
                            shape=(size, size), dtype=np.uint32),
            'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcdmod')
        fns['GCD mod time'] = fn
        stepsmod: np.ndarray = np.fromfunction(lambda x, y: np.vectorize(gcd_mod)(x + 1, y + 1), shape=(size, size),
                                               dtype=np.uint32)
        stepsmod_n = stepsmod * 255 / np.max(stepsmod)
        Image.fromarray(np.uint8(stepsmod_n), 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcdsub')
        fns['GCD sub time'] = fn
        stepssub: np.ndarray = np.fromfunction(lambda x, y: np.vectorize(gcd_sub)(x + 1, y + 1), shape=(size, size),
                                               dtype=np.uint32)
        stepssub_n = stepssub * 255 / np.max(stepssub)  # Normalize the step counts
        Image.fromarray(np.uint8(stepssub_n), 'L').save(fn)

        fn = fnprovider.get_filename('.png', 'gcdboth')
        fns['both GCD (blue = SUB, red = MOD) (log scale)'] = fn
        stepssub = np.log(stepssub)
        stepsmod = np.log(stepsmod)
        mx = max(np.max(stepssub), np.max(stepsmod))
        stepssub_n2 = np.uint8(stepssub * 255 / mx)
        stepsmod_n2 = np.uint8(stepsmod * 255 / mx)
        Image.fromarray(np.dstack((stepssub_n2, np.zeros((size, size), dtype=np.uint8), stepsmod_n2)), 'RGB').save(fn)

        return ',\n'.join('{}: {}'.format(i, j) for i, j in fns.items())
