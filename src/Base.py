import abc
import os
import tempfile
from collections import defaultdict


class AbstractFilenameProvider:
    def __init__(self, metadata=''):
        self.dict = {}

    def get_filename(self, suffix=None, name=None, printable=None):
        fn = self._get_filename(suffix, name)
        if printable is not None:
            self.dict[printable] = fn
        if not fn.startswith('file://'):
            fn = fn
        return fn

    def format_files(self, **extra):
        f = '\n'.join('{}: file:///{}'.format(k, os.path.abspath(v).replace('\\', '/')) for k, v in self.dict.items())
        e = '\n'.join(f'{k}: {v}' for k, v in extra.items())
        return '\n'.join([f, e])

    @abc.abstractmethod
    def _get_filename(self, suffix=None, name=None):
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

    def _get_filename(self, suffix=None, name=None):
        return tempfile.NamedTemporaryFile(prefix=self.prefix + (name if name else ''),
                                           suffix=suffix,
                                           delete=False).name


class RealFilenameProvider(AbstractFilenameProvider):
    def __init__(self, folder, metadata=''):
        super().__init__(metadata)
        self.folder = folder
        self.prefix = metadata
        self.count = defaultdict(int)

    def _get_filename(self, suffix=None, name=None):
        self.count[name] += 1
        return os.path.join(self.folder,
                            'w{}_{}_{}{}'.format(self.prefix, name if name else '', self.count[name], suffix))
