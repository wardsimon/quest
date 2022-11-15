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
        # self._make_gems()
        # self._make_castle()
        # self.fig.show()

    def _make_obstacles(self, n=50):
        free_zone = 150
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

    def _make_gems(self, n=200):
        posx = (np.random.random(n) * self.nx).astype(int)
        posy = (np.random.random(n) * self.ny).astype(int)
        for i in range(n):
            self.array[posx[i], posy[i]] = 2
        self.ax.plot(posx, posy, '^')

    def _make_castles(self):
        dx = 80
        thickness = 10
        direction = np.random.choice([0, 1, 2, 3])

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
                       (thickness * int(direction != 2)):int(posx + 0.5 * dx) -
                       (thickness * int(direction != 0)),
                       int(posy - 0.5 * dx) +
                       (thickness * int(direction != 3)):int(posy + 0.5 * dx) -
                       (thickness * int(direction != 1))] = 0
            x.append(posx)
            y.append(posy)
        # fig, ax = plt.subplots()
        # ax.imshow(self.array.T, origin='lower')
        # fig.show()

        self._castles = {
            'dx': dx,
            'thickness': thickness,
            'direction': direction,
            'red': {
                'x': x[0],
                'y': y[0],
            },
            'blue': {
                'x': x[1],
                'y': y[1],
            }
        }
