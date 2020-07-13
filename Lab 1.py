#!/usr/bin/python
# coding: utf8
import math
from tkinter import Tk, Canvas, Frame, BOTH, Button, Entry, StringVar, Menu, simpledialog
import numpy as np
from functools import partial

pressed = False
class Example(Frame):

    line1 = []
    line2 = []
    line3 = []
    line4 = []
    line5 = []
    line6 = []
    line7 = []
    line8 = []

    circle1 = []
    circle2 = []
    circle3 = []
    circle4 = []
    circle5 = []
    circle6 = []
    circle7 = []
    circle8 = []

    combo = []

    combo_system = []

    radius = 30

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI(parent)

    def get_new_line(self, x1, y1, x2, y2):
        points = []
        issteep = abs(y2 - y1) > abs(x2 - x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2 - y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        return points

    def get_new_circle(self, center=(0, 0), r=50, start=0.0, end=math.pi * 2, n=1000):
        points = []
        current_angle = start

        for step in range(0, n):
            x = center[0] + (math.cos(current_angle) * r)
            y = center[1] + (math.sin(current_angle) * r)
            points.append((x, y))
            current_angle += (end - start) / n

        return points

    def draw_object(self, points, canvas):
        for i in range(0, len(points)):
            canvas.create_oval(points[i],points[i],width=0, fill='black')

    def draw_system(self, canvas):

        canvas.create_text(60, 575, text="40", font="Verdana 13")
        canvas.create_text(25, 535, text="40", font="Verdana 13")

        start_coef = 10

        # draw net lines
        for j in range(-150, 150):
            canvas.create_line(-12650 + start_coef, 5 + (j * 40), 12650 + start_coef, 5 + (j * 40),width=1)
        for j in range(-320, 320):
            canvas.create_line(5 + (j * 40) + start_coef, -5650, 5 + (j * 40) + start_coef, 5650,width=1)

    def draw_all(self, canvas):

        #self.draw_system(canvas)
        start_coef = 10

        # x and y arrows
        line100 = self.get_new_line(5 + start_coef, 5, 5 + start_coef, 565)
        line200 = self.get_new_line(5 + start_coef, 565, 1265 + start_coef, 565)
        line101 = self.get_new_line(5 + start_coef, 5, 5, 15)
        line102 = self.get_new_line(5 + start_coef, 5, 5 + start_coef + start_coef, 15)
        line201 = self.get_new_line(1265 + start_coef, 565, 1265, 565 - start_coef)
        line202 = self.get_new_line(1265 + start_coef, 565, 1265, 565 + start_coef)

        # x and y text
        canvas.create_text(8, 30, text="Y", font="Verdana 13")
        canvas.create_text(1244 + start_coef, 575, text="X", font="Verdana 13")

        # draw net lines
        for j in range(-150, 150):
            canvas.create_line(-12650 + start_coef, 5 + (j * 40), 12650 + start_coef, 5 + (j * 40),width=1)
        for j in range(-320, 320):
            canvas.create_line(5 + (j * 40) + start_coef, -5650, 5 + (j * 40) + start_coef, 5650,width=1)

        # x and y arrows
        self.draw_object(line100, canvas)
        self.draw_object(line200, canvas)
        self.draw_object(line101, canvas)
        self.draw_object(line102, canvas)
        self.draw_object(line201, canvas)
        self.draw_object(line202, canvas)

        # draw lines
        self.draw_object(self.line1, canvas)
        self.draw_object(self.line2, canvas)
        self.draw_object(self.line3, canvas)
        self.draw_object(self.line4, canvas)
        self.draw_object(self.line5, canvas)
        self.draw_object(self.line6, canvas)
        self.draw_object(self.line7, canvas)
        self.draw_object(self.line8, canvas)

        # draw circles
        self.draw_object(self.circle1, canvas)
        self.draw_object(self.circle2, canvas)
        self.draw_object(self.circle3, canvas)
        self.draw_object(self.circle4, canvas)
        self.draw_object(self.circle5, canvas)
        self.draw_object(self.circle6, canvas)
        self.draw_object(self.circle7, canvas)
        self.draw_object(self.circle8, canvas)

    def move(self, points, x_delta, y_delta, corner = 1):
        B = np.matrix(points)
        C = np.ones((len(points), 1), dtype=float)
        D = np.hstack((B, C))
        F = np.identity(3, dtype=float)
        F[2, 0] = x_delta
        F[2, 1] = y_delta
        F[2, 2] = corner
        return D.dot(F)

    def turn(self, points, alpha):
        B = np.matrix(points)
        C = np.ones((len(points), 1), dtype=float)
        D = np.hstack((B, C))
        F = np.identity(3, dtype=float)
        F[0, 0] = math.cos(math.radians(alpha))
        F[0, 1] = math.sin(math.radians(alpha))
        F[1, 0] = -math.sin(math.radians(alpha))
        F[1, 1] = math.cos(math.radians(alpha))
        return D.dot(F)

    def aphin(self, points, x0, y0, xx, yx, xy, yy):
        new_points = []
        for i in points:
            print(i[0],i[1])
            #x = i[0] - 15
            #y = 565 - i[1]
            new_x = ( x0 + (xx * i[0]) + (xy * i[1]) )
            new_y = ( y0 + (yx * i[0]) + (yy * i[1]) )
            #new_x = ( x0 + (xx * i[0]) + (xy * i[1]) ) + 15
            #new_y = ( y0 + (yx * i[0]) + (yy * i[1]) ) - 565
            #new_y = new_y * -1

            print(new_x,new_y)
            new_points.append((new_x, new_y))
            #new_points.append((new_y, new_x))
        return new_points

    def projective(self, points, x0, y0, xx, yx, xy, yy, w0, wx, wy):
        new_points = []
        for i in points:
            print(i[0],i[1])
            #x = i[0] - 15
            #y = 565 - i[1]
            new_x = ((w0 * x0) + (wx * xx * i[0]) + (wy * xy * i[1])) / (w0 + wx * i[0] + wy * i[1])
            new_y = ((w0 * y0) + (wx * yx * i[0]) + (wy * yy * i[1])) / (w0 + wx * i[0] + wy * i[1])
            #new_x = ((w0 * x0) + (wx * xx * x) + (wy * xy * y)) / (w0 + wx * x + wy * y) + 15
            #new_y = ((w0 * y0) + (wx * yx * x) + (wy * yy * y)) / (w0 + wx * x + wy * y) - 565
            #new_y = new_y * -1

            print(new_x,new_y)
            new_points.append((new_x, new_y))

        return new_points

    def get_list(self, array):
        new_list = []
        for i in range(0, len(array)-1):
            new_list.append((array[i,0], array[i,1]))
        return new_list

    def click_move_button(self, canvas, message, message2):

        x_delta = int(message.get())
        y_delta = int(message2.get()) * -1

        canvas.delete("all")

        self.combo = self.get_list(self.move(self.combo, x_delta, y_delta))
        self.draw_object(self.combo, canvas)
        self.draw_system(canvas)
        self.draw_object(self.combo_system, canvas)

        canvas.pack(fill=BOTH, expand=1)

    def click_turn_button(self, canvas, message3, message4, message5):

        x_delta = int(message3.get()) + 15
        y_delta = -1*(565 - int(message4.get()))

        canvas.delete("all")

        self.combo = self.get_list(self.move(self.combo, x_delta, y_delta))

        alpha = int(message5.get())
        self.combo = self.get_list(self.turn(self.combo, alpha))

        y_delta = 565 - int(message4.get())
        self.combo = self.get_list(self.move(self.combo, x_delta, y_delta,corner=-1))

        self.draw_object(self.combo, canvas)
        self.draw_system(canvas)
        self.draw_object(self.combo_system, canvas)

        canvas.pack(fill=BOTH, expand=1)

    def click_R_button(self, R, canvas):

        canvas.delete("all")
        self.radius = int(R.get())
        r_scale = self.radius - 30

        coef = 40 + r_scale

        # lines
        self.line1 = self.get_new_line(110 + coef - r_scale + r_scale, 240 + r_scale + r_scale,
                                       210 + coef + r_scale + r_scale, 240 + r_scale + r_scale)
        self.line2 = self.get_new_line(110 + coef - r_scale + r_scale, 180 - r_scale + r_scale,
                                       210 + coef + r_scale + r_scale, 180 - r_scale + r_scale)
        self.line3 = self.get_new_line(20 + coef - r_scale, 175, 20 + coef - r_scale, 245 + r_scale)
        self.line4 = self.get_new_line(300 + coef + r_scale + r_scale + r_scale, 173,
                                       300 + coef + r_scale + r_scale + r_scale, 247 + r_scale)
        self.line5 = self.get_new_line(60 + coef + r_scale, 125, 130 + coef - r_scale + r_scale, 90 - r_scale)
        self.line6 = self.get_new_line(260 + coef - r_scale + r_scale + r_scale, 127, 190 + coef + r_scale + r_scale,
                                       90 - r_scale)
        self.line7 = self.get_new_line(60 + coef + r_scale, 295 + r_scale, 130 + coef - r_scale + r_scale,
                                       330 + r_scale + r_scale)
        self.line8 = self.get_new_line(260 + coef - r_scale + r_scale + r_scale, 293 + r_scale,
                                       190 + coef + r_scale + r_scale, 330 + r_scale + r_scale)

        # circles
        self.circle1 = self.get_new_circle(center=(40 + coef, 150), r=30 + r_scale)
        self.circle2 = self.get_new_circle(center=(40 + coef, 270 + r_scale), r=30 + r_scale)
        self.circle3 = self.get_new_circle(center=(280 + coef + r_scale + r_scale, 150), r=30 + r_scale)
        self.circle4 = self.get_new_circle(center=(280 + coef + r_scale + r_scale, 270 + r_scale), r=30 + r_scale)
        self.circle5 = self.get_new_circle(center=(160 + coef + r_scale, 90 - r_scale), r=30 + r_scale)
        self.circle6 = self.get_new_circle(center=(160 + coef + r_scale, 330 + r_scale + r_scale), r=30 + r_scale)
        self.circle7 = self.get_new_circle(center=(110 + coef + r_scale, 210 + r_scale), r=30 + r_scale,
                                           start=math.pi * 1.5, end=math.pi * 0.5)
        self.circle8 = self.get_new_circle(center=(210 + coef + r_scale, 210 + r_scale), r=30 + r_scale,
                                           start=math.pi * 1.5, end=math.pi * 2 + math.pi * 0.5)

        self.combo = self.line1 + self.line2 + self.line3 + self.line4 + self.line5 + self.line6 + self.line7 + self.line8 + \
                     self.circle1 + self.circle2 + self.circle3 + self.circle4 + self.circle5 + self.circle6 + self.circle7 + self.circle8

        self.draw_all(canvas)

        start_coef = 10
        line100 = self.get_new_line(5 + start_coef, 5, 5 + start_coef, 565)
        line200 = self.get_new_line(5 + start_coef, 565, 1265 + start_coef, 565)
        line101 = self.get_new_line(5 + start_coef, 5, 5, 15)
        line102 = self.get_new_line(5 + start_coef, 5, 5 + start_coef + start_coef, 15)
        line201 = self.get_new_line(1265 + start_coef, 565, 1265, 565 - start_coef)
        line202 = self.get_new_line(1265 + start_coef, 565, 1265, 565 + start_coef)

        self.combo_system = line100 + line200 + line101 + line102 + line201 + line202

        canvas.pack(fill=BOTH, expand=1)

    def click_aphin_button(self, canvas, x0, y0, xx, yx, xy, yy):

        x0 = int(x0.get())
        y0 = int(y0.get())
        xx = int(xx.get())
        yx = int(yx.get())
        xy = int(xy.get())
        yy = int(yy.get())

        canvas.delete("all")

        self.combo = self.aphin(self.combo, x0, y0, xx, yx, xy, yy)
        self.draw_object(self.combo, canvas)

        self.draw_system(canvas)

        self.combo_system = self.aphin(self.combo_system, x0, y0, xx, yx, xy, yy)
        self.draw_object(self.combo_system, canvas)

        canvas.pack(fill=BOTH, expand=1)

    def click_projective_button(self, canvas, x0, y0, xx, yx, xy, yy, w0, wx, wy):

        x0 = int(x0.get())
        y0 = int(y0.get())
        w0 = int(w0.get())

        xx = int(xx.get())
        yx = int(yx.get())
        wx = int(wx.get())

        xy = int(xy.get())
        yy = int(yy.get())
        wy = int(wy.get())

        canvas.delete("all")

        self.combo = self.projective(self.combo, x0, y0, xx, yx, xy, yy, w0, wx, wy)
        self.draw_object(self.combo, canvas)

        self.draw_system(canvas)

        self.combo_system = self.projective(self.combo_system, x0, y0, xx, yx, xy, yy, w0, wx, wy)
        self.draw_object(self.combo_system, canvas)

        canvas.pack(fill=BOTH, expand=1)

    def initUI(self, parent):

        self.parent.title("LAB 0")
        self.pack(fill= BOTH, expand = 1)
        self.canvas = Canvas(self)

        #default r = 30
        r_scale = self.radius - 30

        coef = 40 + r_scale

        # lines
        self.line1 = self.get_new_line(110 + coef- r_scale+ r_scale, 240+ r_scale+ r_scale, 210 + coef+ r_scale+ r_scale, 240+ r_scale+ r_scale)
        self.line2 = self.get_new_line(110 + coef- r_scale+ r_scale, 180- r_scale+ r_scale, 210 + coef+ r_scale+ r_scale, 180- r_scale+ r_scale)
        self.line3 = self.get_new_line(20 + coef - r_scale, 175, 20 + coef- r_scale, 245+ r_scale)
        self.line4 = self.get_new_line(300 + coef + r_scale+ r_scale+ r_scale, 173, 300 + coef + r_scale+ r_scale+ r_scale, 247+ r_scale)
        self.line5 = self.get_new_line(60 + coef+ r_scale, 125, 130 + coef- r_scale+ r_scale, 90- r_scale)
        self.line6 = self.get_new_line(260 + coef- r_scale+ r_scale+ r_scale, 127, 190 + coef+ r_scale+ r_scale, 90- r_scale)
        self.line7 = self.get_new_line(60 + coef+ r_scale, 295+r_scale, 130 + coef- r_scale+ r_scale, 330+ r_scale+ r_scale)
        self.line8 = self.get_new_line(260 + coef- r_scale+ r_scale+ r_scale, 293+ r_scale, 190 + coef+ r_scale + r_scale, 330+ r_scale+ r_scale)

        # circles
        self.circle1 = self.get_new_circle(center=(40 + coef, 150), r=30 + r_scale)
        self.circle2 = self.get_new_circle(center=(40 + coef, 270 + r_scale), r=30 + r_scale)
        self.circle3 = self.get_new_circle(center=(280 + coef+ r_scale+ r_scale, 150), r=30 + r_scale)
        self.circle4 = self.get_new_circle(center=(280 + coef+ r_scale+ r_scale, 270 + r_scale), r=30 + r_scale)
        self.circle5 = self.get_new_circle(center=(160 + coef+ r_scale, 90- r_scale), r=30 + r_scale)
        self.circle6 = self.get_new_circle(center=(160 + coef+ r_scale, 330 + r_scale + r_scale), r=30 + r_scale)
        self.circle7 = self.get_new_circle(center=(110 + coef+ r_scale, 210+ r_scale), r=30 + r_scale, start=math.pi * 1.5, end=math.pi * 0.5)
        self.circle8 = self.get_new_circle(center=(210 + coef+ r_scale, 210+ r_scale), r=30 + r_scale, start=math.pi * 1.5, end=math.pi * 2 + math.pi * 0.5)

        self.canvas.create_oval(40 + coef, 150,40 + coef, 150, width=0, fill='black')
        self.canvas.create_oval(40 + coef, 270 + r_scale,40 + coef, 270 + r_scale, width=0, fill='black')
        self.canvas.create_oval(280 + coef+ r_scale+ r_scale, 150,280 + coef+ r_scale+ r_scale, 150, width=0, fill='black')
        self.canvas.create_oval(280 + coef+ r_scale+ r_scale, 270 + r_scale,280 + coef+ r_scale+ r_scale, 270 + r_scale, width=0, fill='black')
        self.canvas.create_oval(160 + coef+ r_scale, 90- r_scale,160 + coef+ r_scale, 90- r_scale, width=0, fill='black')
        self.canvas.create_oval(160 + coef+ r_scale, 330 + r_scale + r_scale,160 + coef+ r_scale, 330 + r_scale + r_scale, width=0, fill='black')
        self.canvas.create_oval(110 + coef+ r_scale, 210+ r_scale,110 + coef+ r_scale, 210+ r_scale, width=0, fill='black')
        self.canvas.create_oval(210 + coef+ r_scale, 210+ r_scale,210 + coef+ r_scale, 210+ r_scale, width=0, fill='black')

        self.draw_all(self.canvas)

        self.canvas.create_text(60, 575, text="40", font="Verdana 13")
        self.canvas.create_text(25, 535, text="40", font="Verdana 13")

        self.combo = self.line1+self.line2+self.line3+self.line4+self.line5+self.line6+self.line7+self.line8+\
                self.circle1+self.circle2+self.circle3+self.circle4+self.circle5+self.circle6+self.circle7+self.circle8

        start_coef = 10
        line100 = self.get_new_line(5 + start_coef, 5, 5 + start_coef, 565)
        line200 = self.get_new_line(5 + start_coef, 565, 1265 + start_coef, 565)
        line101 = self.get_new_line(5 + start_coef, 5, 5, 15)
        line102 = self.get_new_line(5 + start_coef, 5, 5 + start_coef + start_coef, 15)
        line201 = self.get_new_line(1265 + start_coef, 565, 1265, 565 - start_coef)
        line202 = self.get_new_line(1265 + start_coef, 565, 1265, 565 + start_coef)

        self.combo_system = line100 + line200 + line101 + line102 + line201 + line202

        self.canvas.pack(fill = BOTH, expand = 1)

# MOVE
        move_x = StringVar()
        move_y = StringVar()

        move_x_entry  = Entry(textvariable=move_x)
        move_x_entry.place(relx=0.055, rely = 0.98, width = 50, anchor="c")

        move_y_entry = Entry(textvariable=move_y)
        move_y_entry.place(relx=0.095, rely = 0.98, width = 50, anchor="c")

        command_move = partial(self.click_move_button,self.canvas,move_x, move_y)

        btn = Button(text="Move", command = command_move)
        btn.place(relx=0.5, rely=0.97, width=50, anchor="c")
        btn.pack(side='left')

# TURN
        turn_x = StringVar()
        turn_y = StringVar()
        turn_alpha = StringVar()

        turn_x_entry = Entry(textvariable=turn_x)
        turn_x_entry.place(relx=0.18, rely=0.98, width=50, anchor="c")

        turn_y_entry = Entry(textvariable=turn_y)
        turn_y_entry.place(relx=0.22, rely=0.98, width=50, anchor="c")

        turn_alpha_entry = Entry(textvariable=turn_alpha)
        turn_alpha_entry.place(relx=0.26, rely=0.98, width=50, anchor="c")

        command_turn = partial(self.click_turn_button, self.canvas,turn_x, turn_y, turn_alpha)

        btn2 = Button(text="Turn", command = command_turn)
        btn2.place(relx=0.14, rely=0.98, width=50, anchor="c")

# CHANGE R
        R = StringVar()
        R_entry = Entry(textvariable=R)
        R_entry.place(relx=0.34, rely=0.98, width=50, anchor="c")
        action_with_arg3 = partial(self.click_R_button, R, self.canvas)
        btn3 = Button(text="R", command=action_with_arg3)
        btn3.place(relx=0.3, rely=0.98, width=50, anchor="c")

# 3 POINTS
        x0 = StringVar()
        x0_entry = Entry(textvariable=x0)
        x0_entry.place(relx=0.5, rely=0.98, width=50, anchor="c")

        y0 = StringVar()
        y0_entry = Entry(textvariable=y0)
        y0_entry.place(relx=0.54, rely=0.98, width=50, anchor="c")

        w0 = StringVar()
        w0_entry = Entry(textvariable=w0)
        w0_entry.place(relx=0.58, rely=0.98, width=50, anchor="c")

        xx = StringVar()
        xx_entry = Entry(textvariable=xx)
        xx_entry.place(relx=0.66, rely=0.98, width=50, anchor="c")

        yx = StringVar()
        yx_entry = Entry(textvariable=yx)
        yx_entry.place(relx=0.7, rely=0.98, width=50, anchor="c")

        wx = StringVar()
        wx_entry = Entry(textvariable=wx)
        wx_entry.place(relx=0.74, rely=0.98, width=50, anchor="c")

        xy = StringVar()
        xy_entry = Entry(textvariable=xy)
        xy_entry.place(relx=0.82, rely=0.98, width=50, anchor="c")

        yy = StringVar()
        yy_entry = Entry(textvariable=yy)
        yy_entry.place(relx=0.86, rely=0.98, width=50, anchor="c")

        wy = StringVar()
        wy_entry = Entry(textvariable=wy)
        wy_entry.place(relx=0.9, rely=0.98, width=50, anchor="c")

# APHIN
        action_with_arg4 = partial(self.click_aphin_button, self.canvas, x0, y0, xx, yx, xy, yy)
        btn4 = Button(text="Aphin", command=action_with_arg4)
        btn4.place(relx=0.42, rely=0.98, width=50, anchor="c")

# PROJECTIVE
        action_with_arg5 = partial(self.click_projective_button, self.canvas, x0, y0, xx, yx, xy, yy, w0, wx, wy)
        btn5 = Button(text="Project", command=action_with_arg5)
        btn5.place(relx=0.46, rely=0.98, width=50, anchor="c")



        self.canvas.bind("<MouseWheel>",self.zoomer)
        # Hack to make zoom work on Windows
        parent.bind_all("<MouseWheel>",self.zoomer)

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)

        self.canvas.bind("<ButtonPress-2>", self.pressed2)
        self.canvas.bind("<Motion>", self.move_move2)

        #self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def zoomer(self, event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #move
    def pressed2(self, event):
        global pressed
        pressed = not pressed
        self.canvas.scan_mark(event.x, event.y)
    def move_move2(self, event):
        if pressed:
            self.canvas.scan_dragto(event.x, event.y, gain=1)

def main():
    root = Tk()
    ex = Example(root)
    root.geometry('1300x680')
    root.minsize(1300,680)
    root.maxsize(1300,680)
    root.mainloop()

if __name__ == '__main__':
    main()