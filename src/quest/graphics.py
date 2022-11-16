import turtle


def rectangle(pen, x, y, dx, dy, color, fill=False):
    pen.penup()
    pen.setheading(0)
    pen.goto(x, y)
    pen.color(color)
    if fill:
        pen.begin_fill()
    pen.pendown()
    pen.forward(dx)
    pen.left(90)
    pen.forward(dy)
    pen.left(90)
    pen.forward(dx)
    pen.left(90)
    pen.forward(dy)
    if fill:
        pen.end_fill()
    pen.penup()


class Graphics:

    def __init__(self, nx, ny, ng, topbar=100):
        self.nx = nx
        self.ny = ny
        self.ng = ng
        self.topbar = topbar

        # create a screen object
        self.screen = turtle.Screen()
        # print(self.nx, self.ny)

        # set screen size
        # self.screen.setup(width=int(self.nx * 1.2), height=int(self.ny * 1.2))
        self.screen.setup(width=self.nx, height=self.ny + self.topbar)
        # self.screen.setup(width=self.nx + 500, height=self.ny + 500)
        # self.screen.screensize(self.nx, self.ny)
        self.screen.setworldcoordinates(0, 0, self.nx, self.ny + self.topbar)

        cv = self.screen.getcanvas()
        cv.adjustScrolls()

        # print(self.screen.window_height())
        # print(self.screen.window_height())
        # print(self.ny, int(self.ny * 1.1))
        # self.canvas = self.screen.getcanvas()

        # screen background color
        self.background = '#D3D3D3'
        self.screen.bgcolor(self.background)

        # screen updaion
        self.screen.tracer(0)

        # self.pen = turtle.RawTurtle(self.canvas)
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.hideturtle()

        self.score_pen = turtle.Turtle()
        self.score_pen.hideturtle()
        self.score_pen.speed(0)
        self.score_pen.penup()
        self.score_pen.goto(self.nx // 2, self.ny)
        self.score_pen.pendown()

        self.add_grid()
        self.add_border()

        self.knights = {}

    def add_grid(self):

        # set a turtle object color
        self.pen.color('#BDBDBD')
        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.setheading(90)
        self.pen.pendown()
        for i in range(self.nx // self.ng):
            self.pen.forward(self.ny)
            if i % 2 == 0:
                self.pen.right(90)
            else:
                self.pen.left(90)
            self.pen.forward(self.ng)
            if i % 2 == 0:
                self.pen.right(90)
            else:
                self.pen.left(90)

        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.setheading(0)
        self.pen.pendown()
        for i in range(self.ny // self.ng):
            self.pen.forward(self.nx)
            if i % 2 == 0:
                self.pen.left(90)
            else:
                self.pen.right(90)
            self.pen.forward(self.ng)
            if i % 2 == 0:
                self.pen.left(90)
            else:
                self.pen.right(90)

        self.pen.penup()

    def add_border(self):

        # create a turtle object object

        # set a turtle object color
        rectangle(self.pen, x=0, y=0, dx=self.nx, dy=self.ny, color='black')
        # self.pen.color('#000000')

        # self.pen.penup()
        # self.pen.goto(0, 0)
        # self.pen.setheading(0)
        # self.pen.pendown()
        # self.pen.forward(self.nx)
        # self.pen.left(90)
        # self.pen.forward(self.ny)
        # self.pen.left(90)
        # self.pen.forward(self.nx)
        # self.pen.left(90)
        # self.pen.forward(self.ny)
        # self.pen.penup()

    def add_obstacles(self, obstacles):

        # create a turtle object object
        # pen = turtle.Turtle()

        # set a turtle object color
        x = obstacles['x']
        y = obstacles['y']
        dx = obstacles['dx']

        # x = [dx // 2]
        # y = [dx // 2]

        self.pen.color('#2F4F4F')
        for i in range(len(x)):

            rectangle(self.pen,
                      x=x[i] - 0.5 * dx,
                      y=y[i] - 0.5 * dx,
                      dx=dx,
                      dy=dx,
                      color='#2F4F4F',
                      fill=True)

            # self.pen.penup()
            # self.pen.goto(x[i] - 0.5 * dx, y[i] - 0.5 * dx)
            # self.pen.setheading(0)
            # self.pen.pendown()
            # self.pen.begin_fill()
            # self.pen.forward(dx)
            # self.pen.left(90)
            # self.pen.forward(dx)
            # self.pen.left(90)
            # self.pen.forward(dx)
            # self.pen.left(90)
            # self.pen.forward(dx)
            # self.pen.end_fill()

    def add_castles(self, castles):

        # create a turtle object object
        # pen = turtle.Turtle()

        # set a turtle object color
        # x = obstacles['x']
        # y = obstacles['y']
        # dx = obstacles['dx']
        dx = castles['dx']
        thickness = castles['thickness']
        star_size = int(castles['dx'] / 3)

        # x = [dx // 2]
        # y = [dx // 2]
        for team in ('red', 'blue'):
            params = castles[team]
            self.pen.color(team)
            self.pen.penup()
            d = params['direction']
            if d == 0:
                self.pen.goto(params['x'] + 0.5 * dx, params['y'] + 0.5 * dx)
                self.pen.setheading(180)
            elif d == 1:
                self.pen.goto(params['x'] - 0.5 * dx, params['y'] + 0.5 * dx)
                self.pen.setheading(270)
            elif d == 2:
                self.pen.goto(params['x'] - 0.5 * dx, params['y'] - 0.5 * dx)
                self.pen.setheading(0)
            elif d == 3:
                self.pen.goto(params['x'] + 0.5 * dx, params['y'] - 0.5 * dx)
                self.pen.setheading(90)
            self.pen.pendown()
            self.pen.begin_fill()
            self.pen.forward(dx)
            self.pen.left(90)
            self.pen.forward(dx)
            self.pen.left(90)
            self.pen.forward(dx)
            self.pen.left(90)
            self.pen.forward(thickness)
            self.pen.left(90)
            self.pen.forward(dx - thickness)
            self.pen.right(90)
            self.pen.forward(dx - (2 * thickness))
            self.pen.right(90)
            self.pen.forward(dx - thickness)
            self.pen.left(90)
            self.pen.forward(thickness)
            self.pen.end_fill()

            self.pen.penup()
            self.pen.goto(params['x'] - 0.5 * star_size,
                          params['y'] - 0.25 * star_size)
            self.pen.pendown()
            self.pen.begin_fill()
            for i in range(5):
                self.pen.forward(star_size)
                self.pen.left(360 / 2.5)
            self.pen.end_fill()

    def add_fountains(self, fountains):

        for team in ('red', 'blue'):
            params = fountains[team]
            self.pen.color('green')
            self.pen.penup()
            self.pen.goto(params['x'] - params['size'], params['y'])
            self.pen.pendown()
            self.pen.setheading(270)
            self.pen.circle(params['size'])

    def add_gems(self, gems):
        x = gems['x']
        y = gems['y']
        r = 10

        self.pen.color('orange')
        for i in range(len(x)):
            self.pen.penup()
            self.pen.goto(x[i], y[i])
            self.pen.pendown()
            self.pen.dot(r)

    def erase_gem(self, x, y):
        r = 10

        self.pen.color(self.background)
        # for i in range(len(x)):
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.dot(r)
        self.pen.penup()

    # def move_knight(self, knight):
    #     # self.knights[knight.name].clear()
    #     self.knights[knight.name].goto(knight.position)
    #     self.knights[knight.name].setheading(knight.heading)
    #     # self.knights[knight.name].pendown()
    #     # self.knights[knight.name].dot(10)

    def draw_scoreboard(self, time, knights):
        self.score_pen.clear()
        self.score_pen.setheading(0)

        self.score_pen.color('black')
        self.score_pen.pensize(1)
        self.score_pen.penup()
        self.score_pen.goto(self.nx // 2, self.ny + self.topbar - 25)
        self.score_pen.pendown()
        self.score_pen.write(f"Time = {time}",
                             move=False,
                             align="center",
                             font=('Arial', 18, 'normal'))

        centerbar_dx = 400
        centerbar_dy = 20
        # self.score_pen.penup()
        self.score_pen.pensize(2)
        rectangle(self.score_pen,
                  x=self.nx // 2 - centerbar_dx // 2,
                  y=self.ny + 10,
                  dx=centerbar_dx,
                  dy=centerbar_dy,
                  color='black')

        rectangle(self.score_pen,
                  x=self.nx // 2 - centerbar_dx // 2,
                  y=self.ny + 40,
                  dx=centerbar_dx,
                  dy=centerbar_dy,
                  color='black')

        healthbar_dx = 300
        healthbar_dy = 15
        counts = {'red': 0, 'blue': 0}
        for knight in knights:
            self.score_pen.pensize(1)
            perc = knight.health / knight.max_health
            if knight.team == 'red':
                x = 0
            else:
                x = self.nx - healthbar_dx
            y = self.ny + 10 + (counts[knight.team] * (healthbar_dy + 15))
            if perc > 0.5:
                fill = 'lime'
            elif perc < 0.2:
                fill = 'red'
            else:
                fill = 'gold'
            rectangle(self.score_pen,
                      x=x,
                      y=y,
                      dx=healthbar_dx * perc,
                      dy=healthbar_dy,
                      color=fill,
                      fill=True)
            self.score_pen.pensize(2)
            rectangle(self.score_pen,
                      x=x,
                      y=y,
                      dx=healthbar_dx,
                      dy=healthbar_dy,
                      color='black',
                      fill=False)

            self.score_pen.pensize(1)
            self.score_pen.goto(x + 0.99 * healthbar_dx, y)
            self.score_pen.color('black')
            self.score_pen.pendown()
            self.score_pen.write(f"{knight.health} / {knight.max_health}",
                                 move=False,
                                 align="right",
                                 font=('Arial', 10, 'normal'))
            self.score_pen.penup()
            self.score_pen.goto(
                x + healthbar_dx + 10 if knight.team == 'red' else x - 10, y)
            self.score_pen.pendown()
            self.score_pen.write(
                knight.name,
                move=False,
                align="left" if knight.team == 'red' else "right",
                font=('Arial', 10, 'normal'))

            counts[knight.team] += 1

        # self.pen.penup()
        # self.screen.update()

    def update(self, time, knights):
        # self.pen.penup()
        # self.pen.goto(self.nx // 2, self.ny)
        # self.pen.pendown()
        # self.time_pen.clear()
        # self.time_pen.write(f"Time = {time}",
        #                     move=False,
        #                     align="center",
        #                     font=('Arial', 18, 'normal'))
        # self.pen.penup()
        if time % 5 == 0:
            self.draw_scoreboard(time=time, knights=knights)
        self.screen.update()
