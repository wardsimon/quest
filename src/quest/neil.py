import numpy as np
from knight import Knight


class Warrior(Knight):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, kind='warrior', creator='Neil', **kwargs)

    def execute(self, time, intel):
        # if self.cooldown >= 8:
        #     self.direction = -self.direction
        # elif all(self.position == self.previous_position):
        #     self.direction = np.random.choice([-1, 1],
        #                                       size=2) * np.random.random(2)
        if all(self.position == self.previous_position) or (self.cooldown >=
                                                            49):
            # self.vector = np.random.choice([-1, 1],
            #                                size=2) * np.random.random(2)
            self.heading = np.random.random() * 360.0

        elif len(intel['flags']) == 2:
            enemy_team = 'red' if self.team == 'blue' else 'blue'
            flag_pos = intel['flags'][enemy_team]
            # print(self, 'going to capture', enemy_team, 'flag at', flag_pos)
            self.goto(*flag_pos)

        elif len(intel['enemies']) > 0:
            name = list(intel['enemies'].keys())[0]
            target = intel['enemies'][name]
            # print(self, 'going to kill', name)
            self.goto(target['x'], target['y'])

        elif intel['gems']:
            # print(self, 'going to pick up gem at', intel['gems']['x'][0],
            #       intel['gems']['y'][0])
            # input('enter')
            self.goto(intel['gems']['x'][0], intel['gems']['y'][0])

        # print(intel['gems'])

        # if self.name == 'Arthur':
        #     self.goto(10, 500)

        self.previous_position = self.position


class Warrior2(Knight):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, kind='warrior', creator='Neil', **kwargs)

    def execute(self, time, intel):
        if all(self.position == self.previous_position) or (self.cooldown >=
                                                            49):
            # self.vector = np.random.choice([-1, 1],
            #                                size=2) * np.random.random(2)
            self.heading = np.random.random() * 360.0

        elif len(intel['flags']) == 2:
            enemy_team = 'red' if self.team == 'blue' else 'blue'
            flag_pos = intel['flags'][enemy_team]
            # print(self, 'going to capture', enemy_team, 'flag at', flag_pos)
            self.goto(*flag_pos)

        elif len(intel['enemies']) > 0:
            name = list(intel['enemies'].keys())[0]
            target = intel['enemies'][name]
            diff = self.towards(target['x'], target['y']) - self.heading
            if diff > 0:
                self.right(diff)
            else:
                self.left(diff)
            # print(self, 'going to kill', name)
            # self.goto(target['x'], target['y'])

        # elif len(intel['gems']) > 0:
        elif intel['gems']:
            self.goto(intel['gems']['x'][0], intel['gems']['y'][0])

        # if self.name == 'Arthur':
        #     self.goto(10, 500)

        self.previous_position = self.position


team = {'Arthur': Warrior, 'Galahad': Warrior2, 'Lancelot': Warrior}
# team = {'Arthur': Warrior}
