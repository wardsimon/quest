import numpy as np
from knight import Scout, Warrior, Healer


class NeilWarrior(Warrior):

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


class NeilScout(Scout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, creator='Neil', **kwargs)
        self.previous_position = [0, 0]
        self.previous_health = self.health

    def execute(self, t, info):
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
            # diff = self.towards(target['x'], target['y']) - self.heading
            # if diff > 0:
            #     self.right(diff)
            # else:
            #     self.left(diff)
            self.heading = (self.towards(target['x'], target['y']) + 180) % 360

            # print(self, 'going to kill', name)
            # self.goto(target['x'], target['y'])

        # elif len(info['gems']) > 0:
        elif info['gems']:
            self.goto(info['gems']['x'][0], info['gems']['y'][0])

        # if self.name == 'Arthur':
        #     self.goto(10, 500)

        self.previous_position = self.position
        self.previous_health = self.health


class NeilHealer(Healer):

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

        min_health = 1000
        friend_in_danger = None
        for friend in info['friends'].values():
            if friend.health < min_health:
                friend_in_danger = friend
                min_health = friend.health

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

        elif (friend_in_danger
              is not None) and (friend_in_danger.health <
                                (friend_in_danger.max_health / 2)):
            self.goto(friend_in_danger.x, friend_in_danger.y)

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
