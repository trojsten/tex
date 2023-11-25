import abc
from schema import Optional

import core.utilities.globals as glob
from core.builder.context import BuildableFilesystemContext, ContextModule
from core.utilities.schema import Schema
from .validators import NabojValidator
from .base import ContextNaboj
from .hierarchy import ContextCompetition, ContextVolume, ContextLanguage, ContextVenue
from .i18n import ContextI18nGlobal


class BuildableContextNaboj(BuildableFilesystemContext, ContextNaboj, metaclass=abc.ABCMeta):
    _schema = ContextNaboj._schema
    _validator_class = NabojValidator

    def populate(self, competition, volume):
        super().populate(competition)
        self.adopt('module', ContextModule('naboj'))
        self.adopt('competition', ContextCompetition(self.root, competition))
        self.adopt('volume', ContextVolume(self.root, competition, volume))


class BuildableContextLanguage(BuildableContextNaboj):
    target = 'language'
    subdir = 'languages'
    _schema = Schema({
        'language': {
            'id': str,
            'polyglossia': str,
            Optional('rtl', default=False): bool,
        }
    })

    def __init__(self, *args):
        self._schema = super()._schema | self._schema
        super().__init__(*args)

    def populate(self, competition, volume, language):
        super().populate(competition, volume)
        self.adopt('language', ContextLanguage(self.root, competition, volume, language))
        self.adopt('i18n', ContextI18nGlobal(self.root, competition))


class BuildableContextVenue(BuildableContextNaboj):
    target = 'venue'
    subdir = 'venues'
    _schema = Schema({
        'language': {
            'id': str,
            'polyglossia': str,
            Optional('rtl', default=False): bool,
        }
    })

    def __init__(self, *args):
        self._schema = super()._schema | self._schema
        super().__init__(*args)

    def populate(self, competition, volume, venue):
        super().populate(competition, volume)
        self.adopt('venue', ContextVenue(self.root, competition, volume, venue).override('start', self.data['volume']))
        self.adopt('i18n', ContextI18nGlobal(self.root, competition))
        self.add({
            'language': {
                'id': self.data['venue']['language'],
            } | glob.languages[self.data['venue']['language']]
        })

        if 'start' not in self.data['venue']:
            self.data['venue']['start'] = self.data['volume']['start']
