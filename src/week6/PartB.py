import random
from typing import List

import numpy as np
from PIL import Image

from Base import Base, AbstractFilenameProvider


class PartB(Base):
    name = 'B'

    def run(self, fnprovider: AbstractFilenameProvider):

        return fnprovider.format_files()

    pass
