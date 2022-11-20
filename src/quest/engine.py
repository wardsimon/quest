from game_map import Map
from graphics import Graphics
from fight import fight
from knight import Knight

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


def make_properties_dict(knight):
    return {
        'name': knight.name,
        'x': knight.x,
        'y': knight.y,
        'position': knight.position,
        'attack': knight.attack,
        'health': knight.health,
        'speed': knight.speed,
        'heading': knight.heading,
        'vector': knight.vector,
        'cooldown': knight.cooldown,
        'view_radius': knight.view_radius,
        'max_health': knight.max_health,
        'message': knight.ai.message
    }


class Engine:

    def __init__(self, score, red_team, blue_team, speedup=1.0):

        self.ng = 32
        self.nx = self.ng * 56
        self.ny = self.ng * 30
        self.graphics = Graphics(nx=self.nx, ny=self.ny, ng=self.ng)
        self.map = Map(nx=self.nx, ny=self.ny, ng=self.ng)
        # self.score = score
        self.speedup = speedup

        self.graphics.add_obstacles(self.map._obstacles)
        self.graphics.add_castles(self.map._castles)
        self.graphics.add_fountains(self.map._fountains)
        self.graphics.add_gems(self.map._gems)

        # self.gems = generate_gems(n=100, game_map=self.map)

        # inds = np.where(self.gems == 1)[0].ravel()
        # if np.sum(inds) > 0:
        #     self._gems_1 = self.map.ax.plot([g.x for g in self.gems],
        #                                     [g.y for g in self.gems], '^')
        # knights = [
        #     Knight(x=nx - 1, y=800, direction=[-1, -0.5], name='Arthur'),
        #     Knight(x=1, y=100, direction=[1, 0.5], name='Lancelot')
        # ]
        # team_names = {
        #     'red': ['Arthur', 'Galahad', 'Lancelot'],
        #     'blue': ['Caspar', 'Balthazar', 'Melchior']
        # }

        team_knights = {'red': red_team, 'blue': blue_team}

        # team_names = {
        #     'red': ['Arthur', 'Galahad', 'Lancelot'],
        #     'blue': ['Caspar', 'Balthazar', 'Melchior']
        # }

        self.team_counts = {
            'red': len(team_knights['red']),
            'blue': len(team_knights['blue'])
        }

        self.knights = []
        for team, names in team_knights.items():
            for n, (name, ai) in enumerate(names.items()):
                self.knights.append(
                    Knight(
                        x=self.map._castles[team]['x'] +
                        self.map._castles['dx'] * 0.7 *
                        (1 - 2.0 * (int(team == 'blue'))),
                        y=int(self.map._castles[team]['y'] -
                              0.5 * self.map._castles['dx'] +
                              (n * 0.5 * self.map._castles['dx'])),
                        heading=180 - (180 * int(team == 'red')),
                        # heading=90,
                        name=name,
                        team=team,
                        castle=self.map._castles[team],
                        fountain=self.map._fountains[team],
                        number=n,
                        AI=ai))

        self.graphics.initialize_scoreboard(knights=self.knights, score=score)

        # sec = input('Let us wait for user input.')

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
    def get_local_map(self, x, y, radius):
        xmin = max(x - radius, 0)
        xmax = min(x + radius + 1, self.nx - 1)
        ymin = max(y - radius, 0)
        ymax = min(y + radius + 1, self.ny - 1)
        local_map = self.map.array[xmin:xmax, ymin:ymax].copy()
        xm, ym = np.meshgrid(np.arange(xmin, xmax),
                             np.arange(ymin, ymax),
                             indexing='ij')
        dist_map = np.sqrt((xm - x)**2 + (ym - y)**2)
        invalid = dist_map > radius
        local_map[invalid] = -1
        return local_map

    def get_info(self, knight, friends_as_dict=False):
        r = knight.view_radius
        # local_map = self.map.array[knight.x - dx:knight.x + dx,
        #                            knight.y - dx:knight.y + dx].copy()
        local_map = self.get_local_map(x=knight.x, y=knight.y, radius=r)
        friends = {}
        enemies = {}
        for k in self.knights:
            props = make_properties_dict(k)
            if (k.team != knight.team):
                dist = knight.get_distance(k.position)
                if dist < knight.view_radius:
                    enemies[k.name] = props
                    # {
                    #     'x': k.x,
                    #     'y': k.y,
                    #     'attack': k.attack,
                    #     'health': k.health,
                    #     'speed': k.speed,
                    #     'heading': k.heading,
                    #     'vector': k.vector,
                    #     'cooldown': k.cooldown,
                    #     'view_radius': k.view_radius
                    # }
            elif k.name != knight.name:
                if friends_as_dict:
                    friends[k.name] = props
                else:
                    friends[k.name] = k
            else:
                my_props = props

        flags = {}
        for team in ('red', 'blue'):
            pos = self.map._flags[team]
            dist = knight.get_distance(pos)
            if team == knight.team or dist < knight.view_radius:
                flags[team] = pos

        #     k.name: k
        #     for k in self.knights
        #     if (k.team == knight.team) and (k.name != knight.name)
        # }
        # enemies = {}
        # for k in self.knights:
        #     if k.team != knight.team:
        #         dist = knight.get_distance(k.position)
        #         if dist < knight.view_radius:
        #             enemies[k.name] = {
        #                 'x': k.x,
        #                 'y': k.y,
        #                 'attack': k.attack,
        #                 'health': k.health,
        #                 'speed': k.speed,
        #                 'heading': k.heading,
        #                 'vector': k.vector,
        #                 'cooldown': k.cooldown,
        #                 'view_radius': k.view_radius
        #             }

        gems = {}
        gem_inds = np.where(local_map == 2)
        # print(knight.name, 'gem_inds', gem_inds)
        if len(gem_inds[0]) > 0:
            gems = {
                'x': gem_inds[0] + max(knight.x - r, 0),
                'y': gem_inds[1] + max(knight.y - r, 0)
            }
        # for i in range(len(gem_inds[0])):
        #     pos = (gem_inds[0][i] + max(knight.x - dx, 0),
        #            gem_inds[1][i] + max(knight.y - dx, 0))
        #     if knight.get_distance(pos) < knight.view_radius:
        #         gems.append(pos)

        return {
            'local_map': local_map,
            'friends': friends,
            'enemies': enemies,
            'gems': gems,
            'flags': flags,
            'me': my_props
        }

    def pickup_gem(self, x, y, team):
        kind_mapping = {0: ('attack', 3), 1: ('health', 5), 2: ('speed', 0.3)}
        kind = np.random.choice([0, 1, 2])
        # kind = 1
        bonus = np.random.random() * kind_mapping[kind][1]
        for k in self.knights:
            if k.team == team:
                if kind == 0:
                    k.attack += int(bonus)
                elif kind == 1:
                    k.max_health += int(bonus)
                elif kind == 2:
                    k.speed = min(k.speed + bonus, k.max_speed)
        # print("picked up gem:", x, y, team)

    def move(self, knight, t, dt, info):

        pos = knight.next_position(dt=dt)
        # print(knight.name, 'Before position', knight.x, knight.y, knight.)
        # print(knight.name, 'Next position', pos)
        if (pos[0] >= 0) and (pos[0] < self.map.nx) and (pos[1] >= 0) and (
                pos[1] < self.map.ny):
            pos2 = knight.next_position(dt=1.01 * np.sqrt(2.0) / knight.speed)
            if (self.map.array[pos[0], pos[1]] !=
                    1) and (self.map.array[pos2[0], pos2[1]] != 1):
                # if (self.map.array[pos[0], pos[1]] != 1):

                if info['gems']:
                    for x, y in zip(info['gems']['x'], info['gems']['y']):
                        # x = info['gems']['x'][igem]
                        # y = info['gems']['y'][igem]
                        # print(
                        #     knight.name, 'gem distance',
                        #     knight.get_distance((x, y)), (knight.speed * dt),
                        #     knight.get_distance((x, y)) <= (knight.speed * dt))
                        if (knight.get_distance((x, y)) <=
                            (knight.speed * dt)) and (abs(
                                abs(
                                    knight.avatar.towards(x, y) -
                                    knight.avatar.heading() - 180) - 180) <
                                                      10):
                            # x = gem[0]
                            # y = gem[1]
                            # print(knight.name, "found gem at", x, y)
                            self.pickup_gem(x=x, y=y, team=knight.team)
                            self.map.array[x, y] = 0
                            self.graphics.erase_gem(x=x, y=y)
                            break

                if not knight.ai.stop:
                    knight.move(dt)

        # self.circles[knight.name][0].center = (knight.x, knight.y)
        # self.circles[knight.name][1].center = (knight.x, knight.y)
        # print(knight.name, 'After position', knight.x, knight.y)
        # x = knight.x
        # y = knight.y
        # for gem in info['gems']:
        #     x = gem[0]
        #     y = gem[1]
        #     if (knight.get_distance(gem) <= (knight.speed * dt)) and (abs(
        #             abs(
        #                 knight.avatar.towards(x, y) - knight.avatar.heading() -
        #                 180) - 180) < 10):
        #         # x = gem[0]
        #         # y = gem[1]
        #         # print(knight.name, "found gem at", x, y)
        #         self.pickup_gem(x=x, y=y, team=knight.team)
        #         self.map.array[x, y] = 0
        #         self.graphics.erase_gem(x=x, y=y)

        opposing_team = 'red' if knight.team == 'blue' else 'blue'
        if knight.get_distance(self.map._flags[opposing_team]) < 5.0:
            self.graphics.announce_winner(knight.team)
            # print(knight.team, 'team wins!')
            return knight.team

    def run(self):

        # time = 0
        # speedup = 1.0
        # sec = True
        t = 0
        # start_time = time.time()
        time_limit = 4000
        dt = 1.0 * self.speedup
        # for t in range(time_limit):
        dt_count = 0
        while t < time_limit:
            # dt_start = time.time()
            # vec = k.direction / np.linalg.norm(k.direction)
            # new_pos = k.position + k.speed * vec
            # ix = int(new_pos[0])
            # iy = int(new_pos[1])
            # self.map.ax.set_title(f'time = {time}')
            for k in self.knights:
                k.advance_dt(t=t, dt=dt, info=self.get_info(knight=k))
                # need to update into after advance step
                info = self.get_info(knight=k, friends_as_dict=True)
                k.execute_ai(t=t, dt=dt, info=info)
                winner = self.move(knight=k, t=t, dt=dt, info=info)
                if winner is not None:
                    return winner
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
                self.team_counts[k.team] -= 1
                if self.team_counts[k.team] == 0:
                    winner = 'red' if k.team == 'blue' else 'blue'
                    self.graphics.announce_winner(winner)
                    return winner

            self.graphics.update(t=t, dt_count=dt_count, knights=self.knights)
            # input('step')

            time.sleep(0.015)
            # dt_end = time.time()
            # dt = dt_end - dt_start
            t += dt
            dt_count += 1
        self.graphics.announce_winner(None)
