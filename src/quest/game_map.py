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
        # self._make_gems()
        # self._make_castle()
        # self.fig.show()

    def _make_obstacles(self, n=50):
        posx = np.random.random(n) * self.nx
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

    def _make_castle(self):
        dx = 80
        posx = np.random.random() * 0.5 * dx + 0.5 * dx
        posy = np.random.random() * self.ny

        rect = patches.Rectangle((posx, posy),
                                 dx,
                                 dx,
                                 linewidth=1.5,
                                 edgecolor='k',
                                 facecolor='r',
                                 alpha=0.8)
        self.ax.add_patch(rect)
