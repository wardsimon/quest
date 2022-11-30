import numpy as np
from ai import BaseAI


class NeilWarrior(BaseAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, creator='Neil', kind='warrior', **kwargs)
        self.previous_position = [0, 0]
        self.previous_health = 0

    def run(self, t, dt, info):
        me = info['me']
        # flag_found = None
        # for friend in info['friends'].values():
        #     if (friend['message'] is not None) and ('flag'
        #                                             in friend['message']):
        #         flag_found = friend['message']['flag']

        if all(me['position'] == self.previous_position) or (
                me['health'] < self.previous_health):
            self.heading = np.random.random() * 360.0

        elif len(info['flags']) == 2:
            flag_pos = info['flags'][self.opposing_team]
            self.goto = flag_pos
            # self.message = {'flag': flag_pos}

        # elif flag_found:
        #     self.goto = flag_found

        elif len(info['enemies']) > 0 and (me['cooldown'] == 0):
            # name = list(info['enemies'].keys())[0]
            # name = info['enemies'][]
            target = info['enemies'][0]
            self.goto = [target['x'], target['y']]

        elif info['gems']:
            self.goto = [info['gems']['x'][0], info['gems']['y'][0]]

        elif t % 5 == 0:
            if me['team'] == 'red':
                if me['x'] < 56 * 32 - 200:
                    #     head = np.random.random() * 360.0
                    # else:
                    self.heading = 0
            else:
                if me['x'] > 200:
                    #     head = np.random.random() * 360.0
                    # else:
                    self.heading = 180
            # self.heading = head

        self.previous_position = me['position']
        self.previous_health = me['health']


class NeilScout(BaseAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, creator='Neil', kind='scout', **kwargs)
        self.previous_position = [0, 0]
        self.previous_health = 0

    def run(self, t, dt, info):
        # super().run(t, dt, info)
        me = info['me']
        # flag_found = None
        # for friend in info['friends'].values():
        #     if (friend['message'] is not None) and ('flag'
        #                                             in friend['message']):
        #         flag_found = friend['message']['flag']

        if all(me['position'] == self.previous_position) or (
                me['health'] < self.previous_health):
            self.heading = np.random.random() * 360.0

        elif len(info['flags']) == 2:
            flag_pos = info['flags'][self.opposing_team]
            self.goto = flag_pos
            # self.message = {'flag': flag_pos}

        # elif flag_found:
        #     self.goto = flag_found

        elif len(info['enemies']) > 0:
            # name = list(info['enemies'].keys())[0]
            # target = info['enemies'][name]
            target = info['enemies'][0]
            self.heading = (self.towards(target['x'], target['y']) + 180) % 360

        elif info['gems']:
            self.goto = [info['gems']['x'][0], info['gems']['y'][0]]

        elif t % 5 == 0:
            if me['team'] == 'red':
                if me['x'] < 56 * 32 - 200:
                    #     head = np.random.random() * 360.0
                    # else:
                    self.heading = 0
            else:
                if me['x'] > 200:
                    #     head = np.random.random() * 360.0
                    # else:
                    self.heading = 180
            # self.heading = head

        self.previous_position = me['position']
        self.previous_health = me['health']
        self.message = "I will end you!"


class NeilHealer(BaseAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, creator='Neil', kind='healer', **kwargs)
        self.previous_position = [0, 0]
        self.previous_health = 0

    def run(self, t, dt, info):
        # super().run(t, dt, info)
        me = info['me']
        # flag_found = None
        # for friend in info['friends'].values():
        #     if (friend['message'] is not None) and ('flag'
        #                                             in friend['message']):
        #         flag_found = friend['message']['flag']

        min_health = 1000
        friend_in_danger = None
        for friend in info['friends']:
            if friend['health'] < min_health:
                friend_in_danger = friend
                min_health = friend['health']

        if all(me['position'] == self.previous_position) or (
                me['health'] < self.previous_health):
            self.heading = np.random.random() * 360.0

        elif len(info['flags']) == 2:
            flag_pos = info['flags'][self.opposing_team]
            self.goto = flag_pos
            # self.message = {'flag': flag_pos}

        # elif flag_found:
        #     self.goto = flag_found
        elif (friend_in_danger
              is not None) and (friend_in_danger['health'] <
                                (friend_in_danger['max_health'] / 2)):
            self.goto = [friend_in_danger['x'], friend_in_danger['y']]

        elif len(info['enemies']) > 0 and (me['cooldown'] == 0):
            # name = list(info['enemies'].keys())[0]
            # target = info['enemies'][name]
            target = info['enemies'][0]
            self.goto = [target['x'], target['y']]

        elif info['gems']:
            self.goto = [info['gems']['x'][0], info['gems']['y'][0]]
        elif t % 5 == 0:
            if me['team'] == 'red':
                if me['x'] < 56 * 32 - 200:
                    #     head = np.random.random() * 360.0
                    # else:
                    self.heading = 0
            else:
                if me['x'] > 200:
                    #     head = np.random.random() * 360.0
                    # else:
                    self.heading = 180
            # self.heading = head

        self.previous_position = me['position']
        self.previous_health = me['health']


team = {'Arthur': NeilWarrior, 'Galahad': NeilHealer, 'Lancelot': NeilScout}
