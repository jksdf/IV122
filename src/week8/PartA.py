from Base import Base, AbstractFilenameProvider


class PartA(Base):
    name = 'A'

    def run(self, fnprovider: AbstractFilenameProvider):
        return fnprovider.format_files()
