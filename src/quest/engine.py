from game_map import Map
from knight import Knight
from fight import fight

import matplotlib.patches as patches
import matplotlib.pyplot as plt


def generate_gems(n, game_map):
    posx = np.random.random(n) * game_map.nx
    posy = np.random.random(n) * game_map.ny
    kind = np.random.choice([0, 1, 2], size=n)


class Engine:

    def __init__(self):

        self.ng = 32
        self.nx = self.ng * 56  # 1920
        self.ny = self.ng * 32  # 1080
        self.map = Map(nx=self.nx, ny=self.ny, ng=self.ng)

        self.gems = generate_gems(n=100, game_map=self.map)
        # knights = [
        #     Knight(x=nx - 1, y=800, direction=[-1, -0.5], name='Arthur'),
        #     Knight(x=1, y=100, direction=[1, 0.5], name='Lancelot')
        # ]
        self.knights = [
            Knight(x=self.nx - 1,
                   y=800,
                   direction=[-1, 0],
                   name='Arthur',
                   team='red'),
            Knight(x=self.nx - 100,
                   y=800,
                   direction=[1, 0],
                   name='Lancelot',
                   team='blue')
        ]

        self.lines = {}
        for k in self.knights:
            line, = self.map.ax.plot(k.x, k.y, 'o')
            self.lines[k.name] = line

        # circle = patches.Circle(pos, 15)
        # m.ax.add_patch(circle)
        sec = input('Let us wait for user input.')

    def get_intel(self, knight):
        dx = knight.view_radius // 2
        local_map = self.map.array[knight.y - dx:knight.y + dx,
                                   knight.x - dx:knight.x + dx]
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
                        'direction': k.direction,
                        'cooldown': k.cooldown,
                        'view_radius': k.view_radius
                    }

        gems

        return {'local_map': local_map, 'friends': friends, 'enemies': enemies}

    def run(self):

        # time = 0
        dt = 1.0
        sec = True
        for time in range(3000):
            # vec = k.direction / np.linalg.norm(k.direction)
            # new_pos = k.position + k.speed * vec
            # ix = int(new_pos[0])
            # iy = int(new_pos[1])
            m.ax.set_title(f'time = {time}')
            for k in knights:
                k.advance_dt(time=time, dt=dt)
                k.execute(time=time,
                          local_env=get_local_environment(knight=k, ))
                pos = k.next_position(dt=dt)
                print(pos)
                if not m.array[pos[1], pos[0]]:
                    k.position = pos
                lines[k.name].set_data([k.x], [k.y])

            dead_bodies = fight(knights=knights, game_map=m)
            for k in dead_bodies:
                lines[k.name].remove()
                del lines[k.name]
                knights.remove(k)

            plt.pause(0.001)