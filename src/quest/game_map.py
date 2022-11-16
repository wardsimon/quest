import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Map:

    def __init__(self, nx, ny, ng):
        self.nx = nx
        self.ny = ny
        self.ng = ng
        self.array = np.zeros((nx, ny), dtype=int)
        # self.fig, self.ax = plt.subplots()
        # self.ax.set_aspect('equal')
        # self.ax.set_xlim(0, nx)
        # self.ax.set_ylim(0, ny)
        self._make_obstacles()
        self._make_castles()
        self._make_fountains()
        self._make_gems()
        # self._make_castle()
        # self.fig.show()

    def _make_obstacles(self, n=50):
        free_zone = 180
        posx = np.random.random(n) * (self.nx - (2 * free_zone)) + free_zone
        posy = np.random.random(n) * self.ny
        dx = 40

        for k in range(n):
            ic = int(posx[k])
            jc = int(posy[k])
            for i in range(max(int(ic - 0.5 * dx), 0),
                           min(int(ic + 0.5 * dx), self.nx)):
                for j in range(max(int(jc - 0.5 * dx), 0),
                               min(int(jc + 0.5 * dx), self.ny)):
                    self.array[i, j] = 1

            # rect = patches.Rectangle((posx[i], posy[i]),
            #                          dx,
            #                          dx,
            #                          linewidth=1.5,
            #                          edgecolor='k',
            #                          facecolor='C0',
            #                          alpha=0.5)
            # self.ax.add_patch(rect)
        # self.ax.pcolormesh(np.arange(self.nx + 1),
        #                    np.arange(self.ny + 1),
        #                    self.map,
        #                    shading='auto')
        # self.im = self.ax.imshow(self.array.T, origin='lower')
        self._obstacles = {'x': posx, 'y': posy, 'dx': dx}

    def _make_gems(self, n=100):
        posx = np.zeros(n, dtype=int)
        posy = np.zeros(n, dtype=int)
        for i in range(n):
            not_good = True
            while not_good:
                x = int(np.random.random() * self.nx)
                y = int(np.random.random() * self.ny)
                if self.array[x, y] == 0:
                    self.array[x, y] = 2
                    posx[i] = x
                    posy[i] = y
                    not_good = False
        self._gems = {'x': posx, 'y': posy}
        # self.ax.plot(posx, posy, '^')

    def _make_castles(self):
        dx = 80
        thickness = 10
        dir_choice = np.random.choice([0, 1, 2, 3])
        directions = [[0, 2], [1, 1], [2, 0], [3, 3]]
        d = directions[dir_choice]

        x = []
        y = []

        for i in range(2):
            posx = np.random.random() * 0.5 * dx + dx
            if i == 1:
                posx = self.nx - posx
            posy = np.random.random() * (self.ny - (2 * dx)) + dx

            self.array[int(posx - 0.5 * dx):int(posx + 0.5 * dx),
                       int(posy - 0.5 * dx):int(posy + 0.5 * dx)] = 1
            self.array[int(posx - 0.5 * dx) +
                       (thickness * int(d[i] != 2)):int(posx + 0.5 * dx) -
                       (thickness * int(d[i] != 0)),
                       int(posy - 0.5 * dx) +
                       (thickness * int(d[i] != 3)):int(posy + 0.5 * dx) -
                       (thickness * int(d[i] != 1))] = 0
            x.append(posx)
            y.append(posy)
        # fig, ax = plt.subplots()
        # ax.imshow(self.array.T, origin='lower')
        # fig.show()

        self._castles = {
            'dx': dx,
            'thickness': thickness,
            'red': {
                'x': x[0],
                'y': y[0],
                'direction': d[0],
            },
            'blue': {
                'x': x[1],
                'y': y[1],
                'direction': d[1]
            }
        }

        self._flags = {'red': [x[0], y[0]], 'blue': [x[1], y[1]]}

    def _make_fountains(self):
        dist = self.ny // 3
        size = 100
        self._fountains = {}
        for team in ('red', 'blue'):
            posx = self._castles[team]['x']
            posy = self._castles[team]['y'] - dist if self._castles[team][
                'y'] > (self.ny // 2) else self._castles[team]['y'] + dist
            self._fountains[team] = {'x': posx, 'y': posy, 'size': size}
