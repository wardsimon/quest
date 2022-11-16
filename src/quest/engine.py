from game_map import Map
from graphics import Graphics
from knight import Knight
from fight import fight

from dataclasses import dataclass
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import time

# @dataclass
# class Gem:
#     x: int
#     y: int
#     kind: int

# def generate_gems(n, game_map):
#     possible_locations = np.where(np.logical_not(game_map.array.ravel()))[0]
#     inds = np.random.choice(possible_locations, size=n)
#     # posx = np.random.random(n) * game_map.nx
#     # posy = np.random.random(n) * game_map.ny
#     kind = np.random.choice([1, 2, 3], size=n)
#     array = np.zeros_like(game_map.array)
#     for i in range(n):
#         array[inds[i] % game_map.nx, inds[i] // game_map.nx] = kind[i]
#     return array


class Engine:

    def __init__(self):

        self.ng = 32
        self.nx = self.ng * 56
        self.ny = self.ng * 30
        self.graphics = Graphics(nx=self.nx, ny=self.ny, ng=self.ng)
        self.map = Map(nx=self.nx, ny=self.ny, ng=self.ng)

        self.graphics.add_obstacles(self.map._obstacles)
        self.graphics.add_castles(self.map._castles)
        self.graphics.add_fountains(self.map._fountains)
        self.graphics.add_gems(self.map._gems)
        sec = input('Let us wait for user input.')

        # self.gems = generate_gems(n=100, game_map=self.map)

        # inds = np.where(self.gems == 1)[0].ravel()
        # if np.sum(inds) > 0:
        #     self._gems_1 = self.map.ax.plot([g.x for g in self.gems],
        #                                     [g.y for g in self.gems], '^')
        # knights = [
        #     Knight(x=nx - 1, y=800, direction=[-1, -0.5], name='Arthur'),
        #     Knight(x=1, y=100, direction=[1, 0.5], name='Lancelot')
        # ]
        team_names = {
            'red': ['Arthur', 'Galahad', 'Lancelot'],
            'blue': ['Caspar', 'Balthazar', 'Melchior']
        }

        self.knights = []
        for team, names in team_names.items():
            for n, name in enumerate(names):
                self.knights.append(
                    Knight(x=self.map._castles[team]['x'] +
                           self.map._castles['dx'] * (1 - 2.0 *
                                                      (int(team == 'blue'))),
                           y=int(self.map._castles[team]['y'] -
                                 0.5 * self.map._castles['dx'] +
                                 (n * 0.5 * self.map._castles['dx'])),
                           heading=180 - (180 * int(team == 'red')),
                           name=name,
                           team=team,
                           castle=self.map._castles[team],
                           fountain=self.map._fountains[team]))

        #     Knight(x=10,
        #            y=800,
        #            heading=0,
        #            name='Lancelot',
        #            team='blue',
        #            castle=self.map._castles['blue'],
        #            fountain=self.map._fountains['blue'])
        # ]
        # self.knights[1].health = 110
        # self.graphics.add_knights(self.knights)

        # self.circles = {}
        # for k in self.knights:
        #     knight_circle = patches.Circle(k.position, 15, color=k.team)
        #     view_circle = patches.Circle(k.position,
        #                                  k.view_radius,
        #                                  ec='w',
        #                                  fc='None')
        #     self.map.ax.add_patch(knight_circle)
        #     self.map.ax.add_patch(view_circle)
        #     # line, = self.map.ax.plot(k.x, k.y, 'o')
        #     self.circles[k.name] = (knight_circle, view_circle)

        # # circle = patches.Circle(pos, 15)
        # # m.ax.add_patch(circle)
        # sec = input('Let us wait for user input.')

    def get_intel(self, knight):
        dx = knight.view_radius // 2
        local_map = self.map.array[knight.x - dx:knight.x + dx,
                                   knight.y - dx:knight.y + dx]
        friends = {
            k.name: k
            for k in self.knights
            if (k.team == knight.team) and (k.name != knight.name)
        }
        enemies = {}
        for k in self.knights:
            if k.team != knight.team:
                dist = knight.get_distance(k.position)
                if dist < knight.view_radius:
                    enemies[k.name] = {
                        'x': k.x,
                        'y': k.y,
                        'attack': k.attack,
                        'health': k.health,
                        'speed': k.speed,
                        'vector': k.vector,
                        'cooldown': k.cooldown,
                        'view_radius': k.view_radius
                    }

        gems

        return {'local_map': local_map, 'friends': friends, 'enemies': enemies}

    def pickup_gem(self, x, y, team):
        kind_mapping = {0: ('attack', 5), 1: ('health', 5), 2: ('speed', 0.5)}
        kind = np.random.choice([0, 1, 2])
        bonus = np.random.random() * kind_mapping[kind][1]
        for k in self.knights:
            if k.team == team:
                if kind == 0:
                    k.attack += bonus
                elif kind == 1:
                    k.health += bonus
                elif kind == 2:
                    k.speed += bonus

    def move(self, knight, time, dt):
        pos = knight.next_position(dt=dt)
        # print(pos)
        if (pos[0] >= 0) and (pos[0] < self.map.nx) and (pos[1] >= 0) and (
                pos[1] < self.map.ny) and (self.map.array[pos[0], pos[1]] !=
                                           1):
            # knight.position = pos
            knight.move(dt)
            # self.graphics.move_knight(knight)

        # self.circles[knight.name][0].center = (knight.x, knight.y)
        # self.circles[knight.name][1].center = (knight.x, knight.y)
        # if self.map.array[pos[0], pos[1]] == 2:
        #     self.pickup_gem(x=pos[0], y=pos[1], team=knight.team)
        #     self.map.array[pos[0], pos[1]] == 0

    def run(self):

        # time = 0
        dt = 1.0
        sec = True
        for t in range(3000):
            # vec = k.direction / np.linalg.norm(k.direction)
            # new_pos = k.position + k.speed * vec
            # ix = int(new_pos[0])
            # iy = int(new_pos[1])
            # self.map.ax.set_title(f'time = {time}')
            for k in self.knights:
                k.advance_dt(time=t, dt=dt)
                k.execute(time=t)
                self.move(knight=k, time=t, dt=dt)
                # # local_env=get_local_environment(knight=k, ))
                # pos = k.next_position(dt=dt)
                # # print(pos)
                # if (pos[0] >= 0) and (pos[0] < self.map.nx) and (
                #         pos[1] >= 0) and (pos[1] < self.map.ny) and (
                #             self.map.array[pos[1], pos[0]] != 1):
                #     k.position = pos
                # self.circles[k.name][0].center = (k.x, k.y)
                # self.circles[k.name][1].center = (k.x, k.y)

            dead_bodies = fight(knights=self.knights, game_map=self.map)
            for k in dead_bodies:
                k.avatar.color('black')
                k.avatar_circle.clear()
                # self.circles[k.name][0].remove()
                # self.circles[k.name][1].remove()
                # del self.circles[k.name]
                self.knights.remove(k)

            self.graphics.update(time=t, knights=knights)

            time.sleep(0.01)