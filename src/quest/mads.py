import numpy as np
from ai import BaseAI


class MadsWarrior(BaseAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, creator='Mads', kind='warrior', **kwargs)
        self.previous_position = [0, 0]
        self.previous_health = 0

    def run(self, t, dt, info):
        # super().run(t, dt, info)
        me = info['me']

        if all(me['position'] == self.previous_position) or (
                me['health'] < self.previous_health):

            self.heading = np.random.random() * 360.0

        elif len(info['flags']) == 2:
            flag_pos = info['flags'][self.opposing_team]
            self.goto = flag_pos

        elif len(info['enemies']) > 0:
            name = list(info['enemies'].keys())[0]
            target = info['enemies'][name]
            self.goto = [target['x'], target['y']]

        elif info['gems']:
            self.goto = [info['gems']['x'][0], info['gems']['y'][0]]

        self.previous_position = me['position']
        self.previous_health = me['health']


team = {
    'Caspar': MadsWarrior,
    'Balthazar': MadsWarrior,
    'Melchior': MadsWarrior
}
