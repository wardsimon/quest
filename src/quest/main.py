from game_map import Map

import matplotlib.patches as patches
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # mpl.use('TkAgg')

    nx = 1920
    ny = 1080
    m = Map(nx=nx, ny=ny)
    pos = [nx - 1, 800]

    line, = m.ax.plot(pos[0], pos[1], 'o')

    # circle = patches.Circle(pos, 15)
    # m.ax.add_patch(circle)
    sec = input('Let us wait for user input.')

    dt = 2.0
    sec = True
    while line.get_xdata()[0] > 0:
        line.set_xdata([line.get_xdata()[0] - dt])
        # m.fig.canvas.draw_idle()
        # print(line.get_xdata()[0])
        plt.pause(0.001)

    sec = input('Let us wait for user input.')

    # while circle.center[0] > 0:
    #     print(circle.center[0] - dt)
    #     circle.set_center((circle.center[0] - dt, circle.center[1]))
    #     print(circle.center)
    #     m.fig.canvas.draw_idle()
    #     sec = input('Let us wait for user input.')
