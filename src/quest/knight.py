import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import turtle


class Knight:

    def __init__(self, x, y, name, heading, team, castle, fountain, creator,
                 number, AI):
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
        self.health = self.max_health
        self.team = team
        self.name = name
        self.creator = creator
        self.cooldown = 0
        self.avatar.color(self.team)
        self.avatar_circle.color(self.team)
        self.avatar_name.color(self.team)

        self.castle = castle
        self.fountain = fountain
        self.number = number

        self.ai = AI()

    def __repr__(self):
        return f'{self.name}: H:{self.health}/{self.max_health} A:{self.attack} S:{self.speed} at {self.x}, {self.y}'

    def __str__(self):
        return repr(self)

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
        new_pos = np.array(
            self.avatar.position()) + self.speed * self.vector * dt
        return new_pos.astype(int)

    def get_distance(self, pos):
        return np.sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2)

    def advance_dt(self, t, dt, info):
        self.cooldown = max(self.cooldown - dt, 0)
        if self.avatar.distance(self.fountain['x'],
                                self.fountain['y']) <= self.fountain['size']:
            self.heal(dt)

    def heal(self, value):
        self.health = min(self.max_health, self.health + value)

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

    def goto(self, x, y):
        angle = self.avatar.towards(x, y)
        self.heading = angle

    def towards(self, x, y):
        return self.avatar.towards(x, y)

    def right(self, angle):
        self.avatar.right(angle)

    def left(self, angle):
        self.avatar.left(angle)


class Scout(Knight):

    def __init__(self, *args, **kwargs):
        self.speed = 1.5
        self.max_speed = 3
        self.max_health = 70
        self.attack = 20
        self.view_radius = 150
        super().__init__(*args, **kwargs)


class Warrior(Knight):

    def __init__(self, *args, **kwargs):
        self.speed = 2.0
        self.max_speed = 4  # 5
        self.max_health = 100
        self.attack = 30
        self.view_radius = 100
        super().__init__(*args, **kwargs)


class Healer(Knight):

    def __init__(self, *args, **kwargs):
        self.speed = 2.0
        self.max_speed = 5  # 7
        self.max_health = 100
        self.attack = 10
        self.view_radius = 100
        super().__init__(*args, **kwargs)

    def advance_dt(self, t, dt, info):
        super().advance_dt(t, dt, info)
        for friend in info['friends'].values():
            if self.get_distance(friend.position) < self.view_radius:
                friend.heal(dt)
