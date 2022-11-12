from game_map import Map
from knight import Knight

import matplotlib.patches as patches
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # mpl.use('TkAgg')

    nx = 1920
    ny = 1080
    m = Map(nx=nx, ny=ny)
    k = Knight(x=nx - 1, y=800)

    line, = m.ax.plot(k.x, k.y, 'o')

    # circle = patches.Circle(pos, 15)
    # m.ax.add_patch(circle)
    sec = input('Let us wait for user input.')

    # time = 0
    dt = 1.0
    sec = True
    for time in range(3000):
        # vec = k.direction / np.linalg.norm(k.direction)
        # new_pos = k.position + k.speed * vec
        # ix = int(new_pos[0])
        # iy = int(new_pos[1])
        m.ax.set_title(f'time = {time}')
        k.move(time=time)
        pos = k.next_position(dt=dt)
        print(pos)
        if not m.array[pos[1], pos[0]]:
            k.position = pos
        line.set_data([k.x], [k.y])
        plt.pause(0.001)

    sec = input('Let us wait for user input.')

    # while circle.center[0] > 0:
    #     print(circle.center[0] - dt)
    #     circle.set_center((circle.center[0] - dt, circle.center[1]))
    #     print(circle.center)
    #     m.fig.canvas.draw_idle()
    #     sec = input('Let us wait for user input.')
