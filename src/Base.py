import abc
import tempfile


class AbstractFilenameProvider:
    @abc.abstractmethod
    def get_filename(self, suffix=None, name=None):
        pass


class Base:
    @abc.abstractmethod
    def run(self, fnprovider: AbstractFilenameProvider):
        pass

    @abc.abstractmethod
    def name(self):
        pass


class TmpFilenameProvider(AbstractFilenameProvider):
    def __init__(self, metadata=''):
        self.prefix = 'tmp433308' + metadata

    def get_filename(self, suffix=None, name=None):
        return tempfile.NamedTemporaryFile(prefix=self.prefix + (name if name else ''),
                                           suffix=suffix,
                                           delete=False).name
