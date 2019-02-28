import abc
import os
import tempfile
from collections import defaultdict


class AbstractFilenameProvider:
    def __init__(self, metadata=''):
        pass

    @abc.abstractmethod
    def get_filename(self, suffix=None, name=None):
        pass


class Base:
    @abc.abstractmethod
    def run(self, fnprovider: AbstractFilenameProvider):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class TmpFilenameProvider(AbstractFilenameProvider):
    def __init__(self, metadata=''):
        super().__init__(metadata)
        self.prefix = 'tmp433308' + metadata

    def get_filename(self, suffix=None, name=None):
        return tempfile.NamedTemporaryFile(prefix=self.prefix + (name if name else ''),
                                           suffix=suffix,
                                           delete=False).name


class RealFilenameProvider(AbstractFilenameProvider):
    def __init__(self, folder, metadata=''):
        super().__init__(metadata)
        self.folder = folder
        self.prefix = metadata
        self.count = defaultdict(int)

    def get_filename(self, suffix=None, name=None):
        self.count[name] += 1
        return os.path.join(self.folder,
                            'w{}_{}_{}{}'.format(self.prefix, name if name else '', self.count[name], suffix))
