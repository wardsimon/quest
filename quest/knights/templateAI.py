__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import abc
from quest.core.ai import BaseAI
from quest.core.team import Team


class TemplateAI(BaseAI):

    def __init__(self, *args, creator: str = None, kind: str = None, **kwargs):
        if creator is None or not isinstance(creator, str):
            raise AttributeError('The AI needs a `creator`')
        if kind is None or not isinstance(kind, str):
            raise AttributeError('The warrior needs a `kind`')
        super().__init__(*args, creator=creator, kind=kind, **kwargs)

    @abc.abstractmethod
    def run(self, t: float, dt: float, info: dict):
        pass
