import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import turtle


class Knight:

    def __init__(self, x, y, name, heading, team, castle, fountain):
        # self._x = int(x)
        # self._y = int(y)
        # self.vector = vector
        self.avatar = turtle.Turtle()
        self.avatar.speed(0)
        self.avatar.penup()

        self.avatar_circle = turtle.Turtle()
        self.avatar_circle.speed(0)
        self.avatar_circle.penup()
        self.avatar_circle.hideturtle()
        self.avatar_circle.setheading(270)

        self.avatar_name = turtle.Turtle()
        self.avatar_name.speed(0)
        self.avatar_name.penup()
        self.avatar_name.hideturtle()

        self.avatar.setx(x)
        self.avatar.sety(y)
        self.heading = heading
        self.speed = 2.0
        self.previous_position = [0, 0]
        self.max_health = 100
        self.health = self.max_health
        self.attack = 50
        self.team = team
        self.name = name
        self.cooldown = 0
        self.view_radius = 100
        self.avatar.color(self.team)
        self.avatar_circle.color(self.team)
        self.avatar_name.color(self.team)

        self.castle = castle
        self.fountain = fountain

    def __repr__(self):
        return f'{self.name}: {self.health}% {self.attack} {self.speed} at {self.x}, {self.y}'

    @property
    def x(self):
        return int(self.avatar.xcor())

    @property
    def y(self):
        return int(self.avatar.ycor())

    @property
    def position(self):
        # print(np.array(self.avatar.position()).astype(int))
        # print(type(np.array(self.avatar.position()).astype(int)))
        return np.array(self.avatar.position()).astype(int)

    # @position.setter
    # def position(self, pos):
    #     self._x = int(pos[0])
    #     self._y = int(pos[1])

    @property
    def heading(self):
        # head = np.arccos(np.dot(self.position, [1, 0])) * 180. / np.pi
        # print(head)
        # head = (np.arctan2(self.vector[1], self.vector[0]) * 180. / np.pi +
        #         360) % 360
        return self.avatar.heading()

    @heading.setter
    def heading(self, angle):
        return self.avatar.setheading(angle)

    @property
    def vector(self):
        h = self.heading * np.pi / 180.0
        return np.array([np.cos(h), np.sin(h)])

    def next_position(self, dt):
        # vec = self.vector / np.linalg.norm(self.vector)
        # print(np.linalg.norm(self.speed * vec * dt))
        # print(np.linalg.norm(vec), vec)
        # print(self.position, self.speed, self.vector, dt)
        new_pos = self.position + self.speed * self.vector * dt
        return new_pos.astype(int)

    def get_distance(self, pos):
        return np.sqrt((pos[0] - self._x)**2 + (pos[1] - self._y)**2)

    def advance_dt(self, time, dt):
        self.cooldown = max(self.cooldown - dt, 0)
        if self.avatar.distance(self.fountain['x'],
                                self.fountain['y']) <= self.fountain['size']:
            self.health = min(self.max_health, self.health + dt)

    def move(self, dt):
        self.avatar.forward(self.speed * dt)

        self.avatar_circle.clear()
        self.avatar_circle.goto(self.x - self.view_radius, self.y)
        self.avatar_circle.pendown()
        self.avatar_circle.circle(self.view_radius)
        self.avatar_circle.penup()

        self.avatar_name.clear()
        self.avatar_name.goto(self.x, self.y)
        self.avatar_name.pendown()
        self.avatar_name.write(self.name,
                               move=False,
                               align="center",
                               font=('Arial', 12, 'normal'))
        self.avatar_name.penup()

    def execute(self, time):
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
        self.previous_position = self.position
