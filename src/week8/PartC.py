from Base import Base, AbstractFilenameProvider


class PartC(Base):
    name = 'C'

    def run(self, fnprovider: AbstractFilenameProvider):
        return fnprovider.format_files()
