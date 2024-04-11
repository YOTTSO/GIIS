from operator import itemgetter
from tkinter import *

pointsMax = []
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


def create_grem():
    points = get_point()
    c.create_rectangle(0, 0, 1920, 1080, outline='white', fill='white')
    global pointsMax
    for point in points:
        c.create_rectangle(point[0], point[1], point[0] + 50, point[1] + 50, fill='black')
    pointsMax.extend(points)


def razv(event):
    test = pointsMax
    for point in test:
        i = 0
        for point1 in test:
            if point[1] == point1[1]:
                i += 1
        if i > 2:
            for point2 in test:
                if point2[1] == point[1]:
                    test.remove(point2)
    test = sorted(test, key=itemgetter(1, 0))
    list1 = []
    for i in range(0, len(test), 2):
        list2 = []
        if i != len(test) - 1:
            list2 = [test[i], test[i + 1]]
            list1.append(list2)
    list1.pop(0)
    for interval in list1:
        for i in range(interval[0][0] + 50, interval[1][0], 50):
            c.create_rectangle(i, interval[0][1], i + 50, interval[0][1] + 50, fill='cyan', outline='black')
            c.after(100, root.update())


def simple_Z(event):
    x = event.x - (event.x % 50)
    y = event.y - (event.y % 50)
    stack = [[x, y]]
    visited = []
    while len(stack) > 0:
        c.create_rectangle(stack[0][0], stack[0][1], stack[0][0] + 50, stack[0][1] + 50, fill='cyan', outline='black')
        visited.append(stack[0])
        test_point = stack[0]
        stack.pop(0)
        points = []
        points.append([test_point[0], test_point[1] + 50])
        points.append([test_point[0] + 50, test_point[1]])
        points.append([test_point[0], test_point[1] - 50])
        points.append([test_point[0] - 50, test_point[1]])
        for point in points:
            if point not in visited and point not in pointsMax:
                stack.insert(0, point)
        c.after(100, root.update())


def str_Z(event):
    x = event.x - (event.x % 50)
    y = event.y - (event.y % 50)
    stack = [[x, y]]
    visited = []
    while len(stack) > 0:
        c.create_rectangle(stack[0][0], stack[0][1], stack[0][0] + 50, stack[0][1] + 50, fill='cyan', outline='black')
        visited.append(stack[0])
        test_point = stack[0]
        stack.pop(0)
        point = [test_point[0] - 50, test_point[1]]
        x_right = 0
        while point not in visited and point not in pointsMax:
            c.create_rectangle(point[0], point[1], point[0] + 50, point[1] + 50, fill='cyan', outline='black')
            visited.append(point)
            point = [point[0] - 50, point[1]]
            c.after(100, root.update())
        point = [test_point[0] + 50, test_point[1]]
        x_right = test_point[0]
        while point not in visited and point not in pointsMax:
            c.create_rectangle(point[0], point[1], point[0] + 50, point[1] + 50, fill='cyan', outline='black')
            visited.append(point)
            x_right = point[0]
            point = [point[0] + 50, point[1]]
            c.after(100, root.update())
        pointUp = [x_right, test_point[1] + 50]
        pointDown = [x_right, test_point[1] - 50]
        if pointDown not in visited and pointDown not in pointsMax:
            stack.insert(0, pointDown)
        if pointUp not in visited and pointUp not in pointsMax:
            stack.insert(0, pointUp)


root = Tk()

mainmenu = Menu(root)
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Грэхам", command=create_grem)

mainmenu.add_cascade(label="Алгоритм", menu=segmentMenu)

c = Canvas(width=1000, height=1000, bg='white')

c.bind("<Button-2>", str_Z)
c.bind("<Button-1>", simple_Z)
c.bind("<Button-3>", razv)

c.grid(row=6, column=3)

root.mainloop()
