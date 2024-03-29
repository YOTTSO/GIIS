from tkinter import *

list = []
choice = 0


def delay(x, y):
    c.create_rectangle(x, y, x, y, fill='black')


def zero():
    c.create_rectangle(0, 0, 1920, 1080, fill='white')


def set_bezie():
    global choice
    choice = 1


def set_ermit():
    global choice
    choice = 2


def set_B_spline():
    global choice
    choice = 3


def b_spline():
    x1, y1, x2, y2, x3, y3, x4, y4 = get_point()
    global list
    list = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    create_B_spline(list)


def b_spline_event(event):
    global list
    if event.num == 1:
        list.pop(0)
        list_extra = [event.x, event.y]
        list.append(list_extra)
    create_B_spline(list)


def make_choice():
    global choice
    if choice == 1:
        create_bezie()
    if choice == 2:
        create_ermit()
    if choice == 3:
        b_spline()


def get_point():
    x1 = float(e1.get())
    y1 = float(e2.get())
    x2 = float(e3.get())
    y2 = float(e4.get())
    x3 = float(e5.get())
    y3 = float(e6.get())
    x4 = float(e7.get())
    y4 = float(e8.get())
    return x1, y1, x2, y2, x3, y3, x4, y4


def create_bezie():
    c.create_rectangle(0, 0, 1920, 1080, fill='white')
    x1, y1, x2, y2, x3, y3, x4, y4 = get_point()
    t = 0
    c.create_rectangle(x1 - 5, y1 - 5, x1 + 5, y1 + 5, outline='red', fill='red')
    c.create_rectangle(x4 - 5, y4 - 5, x4 + 5, y4 + 5, outline='red', fill='red')
    c.create_rectangle(x2 - 5, y2 - 5, x2 + 5, y2 + 5, outline='red', fill='red')
    c.create_rectangle(x3 - 5, y3 - 5, x3 + 5, y3 + 5, outline='red', fill='red')
    while t <= 1:
        x = (1 - t) ** 3 * x1 + 3 * t * (1 - t) ** 2 * x2 + 3 * t ** 2 * (1 - t) * x3 + t ** 3 * x4
        y = (1 - t) ** 3 * y1 + 3 * t * (1 - t) ** 2 * y2 + 3 * t ** 2 * (1 - t) * y3 + t ** 3 * y4
        root.after(10, delay(x, y))
        root.update()
        t += 0.001


def create_ermit():
    c.create_rectangle(0, 0, 1920, 1080, fill='white')
    x1, y1, x2, y2, x3, y3, x4, y4 = get_point()
    t = 0
    c.create_rectangle(x1 - 5, y1 - 5, x1 + 5, y1 + 5, outline='red', fill='red')
    c.create_rectangle(x2 - 5, y2 - 5, x2 + 5, y2 + 5, outline='red', fill='red')
    c.create_line(x1, y1, x1 + x3, y1 + y3, fill='green',
                  width=3, arrow=LAST,
                  activefill='lightgreen',
                  arrowshape=(10, 20, 10))
    c.create_line(x2, y2, x2 + x4, y2 + y4, fill='green',
                  width=3, arrow=LAST,
                  activefill='lightgreen',
                  arrowshape=(10, 20, 10))

    while t <= 1:
        x = x1 + x3 * t + (-3 * x1 + 3 * x2 - 2 * x3 - x4) * t ** 2 + (2 * x1 - 2 * x2 + x3 + x4) * t ** 3
        y = y1 + y3 * t + (-3 * y1 + 3 * y2 - 2 * y3 - y4) * t ** 2 + (2 * y1 - 2 * y2 + y3 + y4) * t ** 3
        root.after(10, delay(x, y))
        root.update()
        t += 0.001


def create_B_spline(list):
    x1, y1, x2, y2, x3, y3, x4, y4 = list[0][0], list[0][1], list[1][0], list[1][1], list[2][0], list[2][1], list[3][0], \
    list[3][1]
    t = 0
    c.create_rectangle(x1 - 5, y1 - 5, x1 + 5, y1 + 5, outline='red', fill='red')
    c.create_rectangle(x4 - 5, y4 - 5, x4 + 5, y4 + 5, outline='red', fill='red')
    c.create_rectangle(x2 - 5, y2 - 5, x2 + 5, y2 + 5, outline='red', fill='red')
    c.create_rectangle(x3 - 5, y3 - 5, x3 + 5, y3 + 5, outline='red', fill='red')
    x1_prev, y1_prev = x1 + 2 * (x2 - x1) / 3, y1 + 2 * (y2 - y1) / 3
    x2_prev, y2_prev = x2 + (x3 - x2) / 3, y2 + (y3 - y2) / 3
    x3_prev, y3_prev = x2 + 2 * (x3 - x2) / 3, y2 + 2 * (y3 - y2) / 3
    x4_prev, y4_prev = x3 + (x4 - x3) / 3, y3 + (y4 - y3) / 3
    x1_new, y1_new = x1_prev + (x2_prev - x1_prev) / 2, y1_prev + (y2_prev - y1_prev) / 2
    x2_new, y2_new = x2_prev, y2_prev
    x3_new, y3_new = x3_prev, y3_prev
    x4_new, y4_new = x3_prev + (x4_prev - x3_prev) / 2, y3_prev + (y4_prev - y3_prev) / 2
    while t <= 1:
        x = (1 - t) ** 3 * x1_new + 3 * t * (1 - t) ** 2 * x2_new + 3 * t ** 2 * (1 - t) * x3_new + t ** 3 * x4_new
        y = (1 - t) ** 3 * y1_new + 3 * t * (1 - t) ** 2 * y2_new + 3 * t ** 2 * (1 - t) * y3_new + t ** 3 * y4_new
        root.after(1, delay(x, y))
        root.update()
        t += 0.001


root = Tk()

mainmenu = Menu(root)
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Кривая Безье", command=set_bezie)
segmentMenu.add_command(label="Форма Эрмита", command=set_ermit)
segmentMenu.add_command(label="Алгоритм Ву", command=set_B_spline)

mainmenu.add_cascade(label="Отрезок", menu=segmentMenu)

e1 = Entry(width=10)
e2 = Entry(width=10)
e3 = Entry(width=10)
e4 = Entry(width=10)
e5 = Entry(width=10)
e6 = Entry(width=10)
e7 = Entry(width=10)
e8 = Entry(width=10)

c = Canvas(width=1000, height=1000, bg='white')

b1 = Button(text="Ввод", command=make_choice)
b3 = Button(text="0", width=4, command=zero)

c.bind("<Button-1>", b_spline_event)

e1.grid(row=0, column=0)
e2.grid(row=0, column=1)
e3.grid(row=1, column=0)
e4.grid(row=1, column=1)
e5.grid(row=2, column=0)
e6.grid(row=2, column=1)
e7.grid(row=3, column=0)
e8.grid(row=3, column=1)

b1.grid(row=4, column=1)
b3.grid(row=5, column=1)

c.grid(row=6, column=3)

root.mainloop()
