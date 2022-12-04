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

        self.screen = turtle.Screen()
        self.screen.clearscreen()

        self.screen.setup(width=self.nx, height=self.ny + self.topbar)
        self.screen.setworldcoordinates(0, 0, self.nx, self.ny + self.topbar)

        cv = self.screen.getcanvas()
        cv.adjustScrolls()

        self.background = '#D3D3D3'
        self.screen.bgcolor(self.background)
        self.screen.tracer(0)

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
        self.previous_update = -10

    def add_grid(self):

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
        rectangle(self.pen, x=0, y=0, dx=self.nx, dy=self.ny, color='black')

    def add_obstacles(self, obstacles):
        x = obstacles['x']
        y = obstacles['y']
        dx = obstacles['dx']
        self.pen.color('#2F4F4F')
        for i in range(len(x)):
            rectangle(self.pen,
                      x=x[i] - 0.5 * dx,
                      y=y[i] - 0.5 * dx,
                      dx=dx,
                      dy=dx,
                      color='#2F4F4F',
                      fill=True)

    def add_castles(self, castles):
        dx = castles['dx']
        thickness = castles['thickness']
        star_size = int(castles['dx'] / 3)
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
            self.pen.setheading(0)
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
            self.pen.penup()
            self.pen.goto(params['x'], params['y'])
            self.pen.pendown()
            self.pen.setheading(0)
            self.pen.write("Fountain",
                           move=False,
                           align="center",
                           font=('Arial', 12, 'normal'))

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
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.dot(r)
        self.pen.penup()

    def initialize_scoreboard(self, knights, score):
        self.pen.setheading(0)
        self.pen.color('black')
        self.pen.pensize(1)
        self.pen.penup()
        self.pen.goto(self.nx // 2 + 5, self.ny + self.topbar - 25)
        self.pen.pendown()
        self.pen.write("Time left =",
                       move=False,
                       align="right",
                       font=('Arial', 18, 'normal'))

        self.pen.penup()
        self.pen.goto(self.nx // 2, self.ny + 40)
        self.pen.pendown()
        self.pen.write(f"Round number {score['count']}",
                       move=False,
                       align="center",
                       font=('Arial', 18, 'normal'))

        self.pen.penup()
        self.pen.goto(self.nx // 2, self.ny + 10)
        self.pen.pendown()
        self.pen.write(f"{score['red']} - {score['blue']}",
                       move=False,
                       align="center",
                       font=('Arial', 18, 'normal'))

        healthbar_dx = 300
        healthbar_dy = 15
        for knight in knights:
            self.pen.pensize(2)
            if knight.team == 'red':
                x = 0
            else:
                x = self.nx - healthbar_dx
            y = self.ny + 10 + (knight.number * (healthbar_dy + 15))
            rectangle(self.pen,
                      x=x,
                      y=y,
                      dx=healthbar_dx,
                      dy=healthbar_dy,
                      color='black',
                      fill=False)

            self.pen.penup()
            self.pen.goto(
                self.nx // 2 + 260 * (1 - 2 * int(knight.team == 'red')), y)
            self.pen.pendown()
            self.pen.color(knight.team)
            self.pen.write(knight.ai.creator,
                           move=False,
                           align="left",
                           font=('Arial', 10, 'normal'))
        self.pen.pensize(1)
        self.pen.penup()

    def update_scoreboard(self, t, knights, time_limit):
        self.score_pen.clear()
        self.score_pen.setheading(0)

        self.score_pen.color('black')
        self.score_pen.pensize(1)
        self.score_pen.penup()
        self.score_pen.goto(self.nx // 2 + 50, self.ny + self.topbar - 25)
        self.score_pen.pendown()
        self.score_pen.write(str(int(time_limit - t)),
                             move=False,
                             align="center",
                             font=('Arial', 18, 'normal'))

        healthbar_dx = 300
        healthbar_dy = 15
        for knight in knights:
            self.score_pen.pensize(1)
            perc = knight.health / knight.max_health
            if knight.team == 'red':
                x = 0
            else:
                x = self.nx - healthbar_dx
            y = self.ny + 10 + (knight.number * (healthbar_dy + 15))
            if perc > 0.5:
                fill = 'lime'
            elif perc < 0.2:
                fill = 'red'
            else:
                fill = 'gold'
            if knight.cooldown > 0:
                fill = 'cyan'
            rectangle(self.score_pen,
                      x=x + 1,
                      y=y + 2,
                      dx=healthbar_dx * perc - 3,
                      dy=healthbar_dy - 3,
                      color=fill,
                      fill=True)

            if knight.team == 'red':
                x = 0.77 * healthbar_dx
                text = (
                    f"{knight.health} / {knight.max_health}    "
                    f"attack={knight.attack}  speed={round(knight.speed, 1)}  "
                    f"{knight.name}")
                align = 'left'
            else:
                x = self.nx - 5
                text = (f"{knight.name}  speed={round(knight.speed, 1)}  "
                        f"attack={knight.attack}"
                        "                                  "
                        f" {knight.health} / {knight.max_health}")
                align = 'right'
            self.score_pen.pensize(1)
            self.score_pen.penup()
            self.score_pen.goto(x, y)
            self.score_pen.color('black')
            self.score_pen.pendown()
            self.score_pen.write(text,
                                 move=False,
                                 align=align,
                                 font=('Arial', 10, 'normal'))

    def update(self, t, dt_count, knights, time_limit):
        if dt_count % 10 == 0:
            self.update_scoreboard(t=t, knights=knights, time_limit=time_limit)
        self.screen.update()

    def announce_winner(self, winner):
        self.pen.penup()
        self.pen.goto(self.nx // 2, self.ny // 2)
        self.pen.pendown()
        if winner is None:
            self.pen.color('black')
            self.pen.write("It's a draw",
                           move=False,
                           align="center",
                           font=('Arial', 100, 'normal'))
        else:
            print(winner, 'team wins!')
            self.pen.color(winner)
            self.pen.write(f"{winner} team wins!",
                           move=False,
                           align="center",
                           font=('Arial', 100, 'normal'))
        self.screen.update()
