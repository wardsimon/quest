import numpy as np
from knight import Scout, Warrior, Healer


class NeilAI(BaseAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, creator='Neil', **kwargs)
        self.previous_position = [0, 0]
        self.previous_health = self.health

    def execute(self, t, info):
        # if self.cooldown >= 8:
        #     self.direction = -self.direction
        # elif all(self.position == self.previous_position):
        #     self.direction = np.random.choice([-1, 1],
        #                                       size=2) * np.random.random(2)
        if all(self.position == self.previous_position) or (
                self.health < self.previous_health):
            # self.vector = np.random.choice([-1, 1],
            #                                size=2) * np.random.random(2)
            self.heading = np.random.random() * 360.0

        elif len(info['flags']) == 2:
            enemy_team = 'red' if self.team == 'blue' else 'blue'
            flag_pos = info['flags'][enemy_team]
            # print(self, 'going to capture', enemy_team, 'flag at', flag_pos)
            self.goto(*flag_pos)

        elif len(info['enemies']) > 0:
            name = list(info['enemies'].keys())[0]
            target = info['enemies'][name]
            # print(self, 'going to kill', name)
            self.goto(target['x'], target['y'])

        elif info['gems']:
            # print(self, 'going to pick up gem at', info['gems']['x'][0],
            #       info['gems']['y'][0])
            # input('enter')
            self.goto(info['gems']['x'][0], info['gems']['y'][0])

        # print(info['gems'])

        # if self.name == 'Arthur':
        #     self.goto(10, 500)

        self.previous_position = self.position
        self.previous_health = self.health


team = {'Arthur': NeilWarrior, 'Galahad': NeilHealer, 'Lancelot': NeilScout}
# team = {'Arthur': Warrior}
