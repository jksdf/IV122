from Base import Base, AbstractFilenameProvider
from common.lsystem.Examples import triangle, weed, square_sierpinsky, cantor, crystal


class PartD(Base):
    """Inspired by http://paulbourke.net/fractals/lsys/"""
    name = 'D'

    def run(self, fnprovider: AbstractFilenameProvider):
        triangle(fnprovider.get_filename('.svg', 'triangle', 'Triangle'))
        weed(fnprovider.get_filename('.svg', 'weed', 'Weed'))
        square_sierpinsky(fnprovider.get_filename('.svg', 'sq_sierp', 'Square Sierpinski'))
        cantor(fnprovider.get_filename('.svg', 'cantor', 'Cantor set'))
        crystal(fnprovider.get_filename('.svg', 'crystal', 'Crystal'))
        return fnprovider.format_files()
