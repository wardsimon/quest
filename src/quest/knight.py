import numpy as np
import turtle
import uuid

SPEED = {'scout': 1.5, 'warrior': 2.0, 'healer': 2.0}
MAX_SPEED = {'scout': 3, 'warrior': 5, 'healer': 7}
MAX_HEALTH = {'scout': 70, 'warrior': 100, 'healer': 100}
ATTACK = {'scout': 20, 'warrior': 30, 'healer': 10}
VIEW_RADIUS = {'scout': 150, 'warrior': 100, 'healer': 100}


class Knight:

    def __init__(self, x, y, name, heading, team, castle, fountain, number,
                 AI):
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
        self.team = team
        self.name = name
        self.cooldown = 0
        self.avatar.color(self.team)
        self.avatar_circle.color(self.team)
        self.avatar_name.color(self.team)

        self.castle = castle
        self.fountain = fountain
        self.number = number

        self.ai = AI(team=team)

        self.speed = SPEED[self.ai.kind]
        self.max_speed = MAX_SPEED[self.ai.kind]
        self.max_health = MAX_HEALTH[self.ai.kind]
        self.attack = ATTACK[self.ai.kind]
        self.view_radius = VIEW_RADIUS[self.ai.kind]
        self.health = self.max_health
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return (f'{self.name}: H:{self.health}/{self.max_health} '
                f'A:{self.attack} S:{self.speed} at {self.x}, {self.y}')

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
        return np.array(self.avatar.position()).astype(int)

    @property
    def heading(self):
        return self.avatar.heading()

    @heading.setter
    def heading(self, angle):
        return self.avatar.setheading(angle)

    @property
    def vector(self):
        h = self.heading * np.pi / 180.0
        return np.array([np.cos(h), np.sin(h)])

    def ray_trace(self, dt):
        vt = self.speed * dt
        ray = self.vector.reshape((2, 1)) * np.linspace(1, vt, int(vt) + 1)
        return (np.array(self.avatar.position()).reshape(
            (2, 1)) + ray).astype(int)

    def get_distance(self, pos):
        return np.sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2)

    def advance_dt(self, t, dt, info):
        self.cooldown = max(self.cooldown - dt, 0)
        if self.avatar.distance(self.fountain['x'],
                                self.fountain['y']) <= self.fountain['size']:
            self.heal(0.5 * dt)
        if self.ai.kind == 'healer':
            for friend in info['friends']:
                if self.get_distance(friend.position) < self.view_radius:
                    friend.heal(0.5 * dt)

    def execute_ai(self, t, dt, info):
        self.ai.exec(t, dt, info)
        if sum([
                bool(self.ai.heading),
                bool(self.ai.goto),
                bool(self.ai.left),
                bool(self.ai.right)
        ]) > 1:
            print('Warning, more than one AI property is set, '
                  'results may be unpredictable!')
        if self.ai.heading is not None:
            self.heading = self.ai.heading
        if self.ai.goto is not None:
            self.goto(*self.ai.goto)
        if self.ai.left is not None:
            self.left(self.ai.left)
        if self.ai.right is not None:
            self.right(self.ai.right)

    def heal(self, value):
        self.health = min(self.max_health, self.health + value)

    def move(self, dt, show_messages=False):
        self.avatar.forward(self.speed * dt)

        self.avatar_circle.clear()
        self.avatar_circle.goto(self.x - self.view_radius, self.y)
        self.avatar_circle.pendown()
        self.avatar_circle.circle(self.view_radius)
        self.avatar_circle.penup()

        self.avatar_name.clear()
        self.avatar_name.goto(self.x, self.y)
        self.avatar_name.pendown()
        text = self.name
        if self.ai.message is not None and show_messages:
            message = str(self.ai.message)
            if len(message) >= 50:
                message = message[:50]
            text += '\nsays: ' + message
        self.avatar_name.write(text,
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
