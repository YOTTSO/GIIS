from tkinter import *

list = []
choice = 0


def delay(x, y):
    c.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill='black')


def zero():
    c.create_rectangle(0, 0, 1920, 1080, fill='white')


def get_point():
    with open('points.txt', "r") as file:
        points = []
        for line in file:
            point = line.split()
            result = [int(item) for item in point]
            points.append(result)
        return points


def sorty_G():
    points0 = get_point()
    points1 = []
    points0 = sorted(points0, key=lambda point: point[1])
    first = points0[0]
    points0.remove(first)
    points0 = sorted(points0, key=lambda point: (first[1] - point[1]) / (first[0] - point[0]))
    points1.append(first)
    points1.insert(0, points0[0])
    points0.remove(points0[0])
    for point in points0:
        while (points1[0][0] - points1[1][0]) * (point[1] - points1[0][1]) - (points1[0][1] - points1[1][1]) * (
                point[0] - points1[0][0]) < 0:
            points1.pop(0)
        points1.insert(0, point)
    return points1


def sorty_jarvis():
    points0 = get_point()
    points1 = []
    points0 = sorted(points0, key=lambda point: point[1])
    first = points0[0]
    points0.remove(first)
    points0 = sorted(points0, key=lambda point: (first[1] - point[1]) / (first[0] - point[0]))
    points0.insert(0, first)
    points1.append(first)
    points1.append(points0[1])
    a = points1
    l = points0
    l.pop(1)
    i = 1
    while a[i] != a[0]:
        l = sorted(l, key=lambda s: (abs((a[i][0] - a[i - 1][0]) * (s[0] - a[i][0])) + abs(
            (a[i][1] - a[i - 1][1]) * (s[1] - a[i][1]))) / (
                                                ((a[i][0] - a[i - 1][0]) ** 2 + (a[i][1] - a[i - 1][1]) ** 2) ** 0.5 * (
                                                    (s[0] - a[i][0]) ** 2 + (s[1] - a[i][1]) ** 2) ** 0.5))
        a.append(l[0])
        l.pop(0)
        i += 1
    return a


def create_grem():
    points = sorty_G()
    p = get_point()
    for point in p:
        delay(point[0], point[1])
    for point in points:
        c.create_rectangle(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, outline='red', fill='red')

    segments = []
    for i in range(len(points)):
        segment = []
        if i == 0:
            segment.append(points[len(points) - 1])
            segment.append(points[i])
        else:
            segment.append(points[i - 1])
            segment.append(points[i])
        segments.append(segment)

    for segment in segments:
        root.after(100, c.create_line(segment[0][0], segment[0][1], segment[1][0], segment[1][1]))
        root.update()


def create_jarvis():
    points = sorty_jarvis()
    points.remove(points[len(points) - 1])
    p = get_point()
    for point in p:
        delay(point[0], point[1])
    for point in points:
        c.create_rectangle(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, outline='red', fill='red')

    segments = []
    for i in range(len(points)):
        segment = []
        if i == 0:
            segment.append(points[len(points) - 1])
            segment.append(points[i])
        else:
            segment.append(points[i - 1])
            segment.append(points[i])
        segments.append(segment)

    for segment in segments:
        root.after(100, c.create_line(segment[0][0], segment[0][1], segment[1][0], segment[1][1]))
        root.update()


root = Tk()

mainmenu = Menu(root)
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Грэхам", command=create_grem)
segmentMenu.add_command(label="Джарвис", command=create_jarvis)

mainmenu.add_cascade(label="Алгоритм", menu=segmentMenu)

c = Canvas(width=1000, height=1000, bg='white')

c.grid(row=6, column=3)

root.mainloop()
