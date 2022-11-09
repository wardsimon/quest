import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Map:

    def __init__(self, nx=1920, ny=1080):
        self.nx = nx
        self.ny = ny
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, nx)
        self.ax.set_ylim(0, ny)
        self._make_obstacles()
        self.fig.show()

    def _make_obstacles(self, n=30):
        posx = np.random.random(n) * self.nx
        posy = np.random.random(n) * self.ny
        dx = 40

        for i in range(n):
            rect = patches.Rectangle((posx[i], posy[i]),
                                     dx,
                                     dx,
                                     linewidth=1.5,
                                     edgecolor='k',
                                     facecolor='none')
            self.ax.add_patch(rect)
