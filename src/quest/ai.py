import numpy as np


class BaseAI:

    def __init__(self, team, kind, creator=None):
        self.team = team
        self.opposing_team = 'red' if self.team == 'blue' else 'blue'
        self.kind = kind.lower()
        self.heading = None
        self.goto = None
        self.message = None
        self.creator = creator
        self.stop = False

    def run(self, t, dt, info):
        self.heading = None
        self.goto = None
        self._params = info['me']

    def get_distance(self, x, y=None):
        if y is None:
            y = x[1]
            x = x[0]
        return np.sqrt((self._params['x'] - x)**2 + (self._params['y'] - y)**2)

    def towards(self, x, y=None):
        if y is None:
            y = x[1]
            x = x[0]
        return ((np.arctan2(y - self._params['y'], x - self._params['x']) *
                 180 / np.pi) + 360) % 360
