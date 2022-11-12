import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Knight:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = [-1, -0.5]
        self.speed = 2.0
        self.previous_position = [0, 0]

    @property
    def position(self):
        return np.array([self.x, self.y])

    @position.setter
    def position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def move(self, time):
        if all(self.position == self.previous_position):
            self.direction = np.random.choice([-1, 1],
                                              size=2) * np.random.random(2)
        self.previous_position = self.position

    def next_position(self, dt):
        vec = self.direction / np.linalg.norm(self.direction)
        new_pos = self.position + self.speed * vec * dt
        return new_pos.astype(int)
