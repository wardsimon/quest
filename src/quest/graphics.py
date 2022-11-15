import turtle


class Graphics:

    def __init__(self, nx, ny, ng):
        self.nx = nx
        self.ny = ny
        self.ng = ng

        # create a screen object
        self.screen = turtle.Screen()
        print(self.nx, self.ny)

        # set screen size
        # self.screen.setup(width=int(self.nx * 1.2), height=int(self.ny * 1.2))
        self.screen.setup(width=self.nx, height=self.ny)
        # self.screen.setup(width=self.nx + 500, height=self.ny + 500)
        # self.screen.screensize(self.nx, self.ny)
        self.screen.setworldcoordinates(0, 0, self.nx, self.ny)

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

        self.time_pen = turtle.Turtle()
        self.time_pen.hideturtle()
        self.time_pen.speed(0)
        self.time_pen.penup()
        self.time_pen.goto(self.nx // 2, self.ny)
        self.time_pen.pendown()

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
        for i in range(self.nx // self.ng):
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
        self.pen.color('#000000')
        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.setheading(0)
        self.pen.pendown()
        self.pen.forward(self.nx)
        self.pen.left(90)
        self.pen.forward(self.ny)
        self.pen.left(90)
        self.pen.forward(self.nx)
        self.pen.left(90)
        self.pen.forward(self.ny)
        self.pen.penup()

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
            self.pen.penup()
            self.pen.goto(x[i] - 0.5 * dx, y[i] - 0.5 * dx)
            self.pen.setheading(0)
            self.pen.pendown()
            self.pen.begin_fill()
            self.pen.forward(dx)
            self.pen.left(90)
            self.pen.forward(dx)
            self.pen.left(90)
            self.pen.forward(dx)
            self.pen.left(90)
            self.pen.forward(dx)
            self.pen.end_fill()

    def add_castles(self, castles):

        # create a turtle object object
        # pen = turtle.Turtle()

        # set a turtle object color
        # x = obstacles['x']
        # y = obstacles['y']
        # dx = obstacles['dx']
        dx = castles['dx']
        thickness = castles['thickness']
        direction = castles['direction']

        # x = [dx // 2]
        # y = [dx // 2]
        for team in ('red', 'blue'):
            params = castles[team]
            self.pen.color(team)
            self.pen.penup()
            if direction == 0:
                self.pen.goto(params['x'] + 0.5 * dx, params['y'] + 0.5 * dx)
                self.pen.setheading(180)
            elif direction == 1:
                self.pen.goto(params['x'] - 0.5 * dx, params['y'] + 0.5 * dx)
                self.pen.setheading(270)
            elif direction == 2:
                self.pen.goto(params['x'] - 0.5 * dx, params['y'] - 0.5 * dx)
                self.pen.setheading(0)
            elif direction == 3:
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

            # self.pen.color(self.background)
            # self.pen.penup()
            # self.pen.goto(
            #     params['x'] - 0.5 * dx + (thickness * int(direction != 2)),
            #     params['y'] - 0.5 * dx + (thickness * int(direction != 3)))
            # self.pen.setheading(0)
            # self.pen.pendown()
            # self.pen.begin_fill()
            # self.pen.forward(dx - thickness -
            #                  (thickness * int(direction in [0, 2])))
            # self.pen.left(90)
            # self.pen.forward(dx - thickness -
            #                  (thickness * int(direction in [1, 3])))
            # self.pen.left(90)
            # self.pen.forward(dx - thickness -
            #                  (thickness * int(direction in [0, 2])))
            # self.pen.left(90)
            # self.pen.forward(dx - thickness -
            #                  (thickness * int(direction in [1, 3])))
            # self.pen.end_fill()

# self.array[int(posx - 0.5 * dx):int(posx + 0.5 * dx),
#                        int(posy - 0.5 * dx):int(posy + 0.5 * dx)] = 1
#             self.array[int(posx - 0.5 * dx) +
#                        (thickness * int(direction != 2)):int(posx + 0.5 * dx) -
#                        (thickness * int(direction != 0)),
#                        int(posy - 0.5 * dx) +
#                        (thickness * int(direction != 3)):int(posy + 0.5 * dx) -
#                        (thickness * int(direction != 1))] = 0

#         self.pen.color('#2F4F4F')
#         for i in range(len(x)):
#             self.pen.penup()
#             self.pen.goto(x[i] - 0.5 * dx, y[i] - 0.5 * dx)
#             self.pen.setheading(0)
#             self.pen.pendown()
#             self.pen.begin_fill()
#             self.pen.forward(dx)
#             self.pen.left(90)
#             self.pen.forward(dx)
#             self.pen.left(90)
#             self.pen.forward(dx)
#             self.pen.left(90)
#             self.pen.forward(dx)
#             self.pen.end_fill()

# def add_knights(self, knights):
#     for k in knights:
#         self.knights[k.name] = turtle.Turtle()
#         self.knights[k.name].speed(0)
#         self.knights[k.name].penup()

#     # for n in range(len(obstacles['x'])):
#     #     pen.penup()
#     #     pen.goto(obstacles['x'][-], 0)
#     #     pen.pendown()

# set turtle object speed

    def move_knight(self, knight):
        # self.knights[knight.name].clear()
        self.knights[knight.name].goto(knight.position)
        self.knights[knight.name].setheading(knight.heading)
        # self.knights[knight.name].pendown()
        # self.knights[knight.name].dot(10)

    def update(self, time):
        # self.pen.penup()
        # self.pen.goto(self.nx // 2, self.ny)
        # self.pen.pendown()
        self.time_pen.clear()
        self.time_pen.write(f"Time = {time}",
                            move=False,
                            align="center",
                            font=('Arial', 18, 'normal'))
        # self.pen.penup()
        self.screen.update()


# ng = 32
# nx = ng * 56  # 1920
# ny = ng * 32  # 1080

# turtle.screensize(nx, ny)

# turtle.speed(0)

# turtle.home()
# turtle.position()

# turtle.heading()

# turtle.circle(50)
# turtle.position()

# turtle.heading()

# turtle.circle(120, 180)  # draw a semicircle
# turtle.position()

# turtle.heading()

# input('wait')

# # color('red', 'yellow')
# # begin_fill()
# # while True:
# #     forward(200)
# #     left(170)
# #     if abs(pos()) < 1:
# #         break
# # end_fill()
# # done()

# import turtle package
# import turtle


# function for movement of an object
def moving_object(move):

    # to fill the color in ball
    # move.fillcolor('orange')

    # start color filling
    # move.begin_fill()

    # draw circle
    move.dot(10)

    # end color filling
    # move.end_fill()


# Driver Code
if __name__ == "__main__":

    # create a screen object
    screen = turtle.Screen()

    # set screen size
    # screen.setup(width=600, height=600, startx=0, starty=-0)
    screen.screensize(1000, 600)

    # screen background color
    screen.bgcolor('green')

    # screen updaion
    screen.tracer(0)

    # create a turtle object object
    move = turtle.Turtle()

    # set a turtle object color
    move.color('orange')

    # set turtle object speed
    move.speed(1)

    # set turtle object width
    # move.width(2)

    # hide turtle object
    move.hideturtle()

    # turtle object in air
    move.penup()

    # set initial position
    move.goto(-250, 0)

    # move turtle object to surface
    move.pendown()

    # create a turtle object object
    move2 = turtle.Turtle()

    # set a turtle object color
    move2.color('cyan')

    # set turtle object speed
    move2.speed(1)

    # set turtle object width
    # move.width(2)

    # hide turtle object
    move2.hideturtle()

    # turtle object in air
    move2.penup()

    # set initial position
    move2.goto(-300, 100)

    # move turtle object to surface
    move2.pendown()
    move2.setheading(60)

    # infinite loop
    while True:

        # clear turtle work
        move.clear()
        move2.clear()

        # call function to draw ball
        moving_object(move)
        moving_object(move2)

        # update screen
        screen.update()

        # forward motion by turtle object
        move.forward(0.5)
        move2.forward(0.5)