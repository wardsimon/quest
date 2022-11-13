import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Knight:

    def __init__(self, x, y, name, direction, team):
        self._x = int(x)
        self._y = int(y)
        self.direction = direction
        self.speed = 2.0
        self.previous_position = [0, 0]
        self.health = 100
        self.attack = 50
        self.team = team
        self.name = name
        self.cooldown = 0
        self.view_radius = 100

    def __repr__(self):
        return f'{self.name}: {self.health}% {self.attack} {self.speed} at {self._x}, {self._y}'

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def position(self):
        return np.array([self._x, self._y])

    @position.setter
    def position(self, pos):
        self._x = int(pos[0])
        self._y = int(pos[1])

    def next_position(self, dt):
        vec = self.direction / np.linalg.norm(self.direction)
        new_pos = self.position + self.speed * vec * dt
        return new_pos.astype(int)

    def get_distance(self, pos):
        return np.sqrt((pos[0] - self._x)**2 + (pos[1] - self._y)**2)

    def advance_dt(self, time, dt):
        self.cooldown = max(self.cooldown - dt, 0)

    def execute(self, time):
        # if self.cooldown >= 8:
        #     self.direction = -self.direction
        # elif all(self.position == self.previous_position):
        #     self.direction = np.random.choice([-1, 1],
        #                                       size=2) * np.random.random(2)
        if all(self.position == self.previous_position) or (self.cooldown >=
                                                            9):
            self.direction = np.random.choice([-1, 1],
                                              size=2) * np.random.random(2)
        self.previous_position = self.position
