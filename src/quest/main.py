from game_map import Map
from knight import Knight
from fight import fight
from engine import Engine

import matplotlib.patches as patches
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # mpl.use('TkAgg')

    best_of = 5
    first_to = 3

    match_score = {'red': 0, 'blue': 0}
    for n in range(best_of):
        engine = Engine(score=match_score)
        winner = engine.run()
        if winner is not None:
            match_score[winner] += 1
        for team in match_score:
            if match_score[team] == first_to:
                break
        input('start next match')

    # ng = 32
    # nx = ng * 56  # 1920
    # ny = ng * 32  # 1080
    # m = Map(nx=nx, ny=ny, ng=ng)
    # # knights = [
    # #     Knight(x=nx - 1, y=800, direction=[-1, -0.5], name='Arthur'),
    # #     Knight(x=1, y=100, direction=[1, 0.5], name='Lancelot')
    # # ]
    # knights = [
    #     Knight(x=nx - 1, y=800, direction=[-1, 0], name='Arthur', team='red'),
    #     Knight(x=nx - 100,
    #            y=800,
    #            direction=[1, 0],
    #            name='Lancelot',
    #            team='blue')
    # ]

    # lines = {}
    # for k in knights:
    #     line, = m.ax.plot(k.x, k.y, 'o')
    #     lines[k.name] = line

    # # circle = patches.Circle(pos, 15)
    # # m.ax.add_patch(circle)
    # sec = input('Let us wait for user input.')

    # # time = 0
    # dt = 1.0
    # sec = True
    # for time in range(3000):
    #     # vec = k.direction / np.linalg.norm(k.direction)
    #     # new_pos = k.position + k.speed * vec
    #     # ix = int(new_pos[0])
    #     # iy = int(new_pos[1])
    #     m.ax.set_title(f'time = {time}')
    #     for k in knights:
    #         k.advance_dt(time=time, dt=dt)
    #         k.execute(time=time, local_env=get_local_environment(knight=k, ))
    #         pos = k.next_position(dt=dt)
    #         print(pos)
    #         if not m.array[pos[1], pos[0]]:
    #             k.position = pos
    #         lines[k.name].set_data([k.x], [k.y])

    #     dead_bodies = fight(knights=knights, game_map=m)
    #     for k in dead_bodies:
    #         lines[k.name].remove()
    #         del lines[k.name]
    #         knights.remove(k)

    #     plt.pause(0.001)

    # sec = input('Let us wait for user input.')

    # while circle.center[0] > 0:
    #     print(circle.center[0] - dt)
    #     circle.set_center((circle.center[0] - dt, circle.center[1]))
    #     print(circle.center)
    #     m.fig.canvas.draw_idle()
    #     sec = input('Let us wait for user input.')
