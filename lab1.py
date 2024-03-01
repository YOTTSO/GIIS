import tkinter as tk
from pynput.mouse import Listener
import time
import numpy as np


global debug_mode
debug_mode = False

window = tk.Tk()
window.title("Графический редактор")

# создаем холст для рисования
canvas = tk.Canvas(window, width=600, height=600)
canvas.pack()

# функция для рисования пикселя по координатам
def draw_pixel(x, y, color="black"):
    canvas.create_rectangle(x, y, x+1, y+1, fill=color)

# функция для рисования пикселя с заданной интенсивностью
def draw_pixel_with_intensity(x, y, intensity, color="black"):
    # преобразуем интенсивность в диапазон от 0 до 255
    intensity = int(intensity * 255)

    # получаем цветовые компоненты пикселя
    r, g, b = canvas.winfo_rgb(color)

    # умножаем цветовые компоненты на интенсивность
    r = (r * intensity) // 65535
    g = (g * intensity) // 65535
    b = (b * intensity) // 65535

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    # создаем новый цвет из полученных компонентов
    new_color = f"#{r:02x}{g:02x}{b:02x}"

    # рисуем пиксель с новым цветом
    canvas.create_rectangle(x, y, x + 1, y + 1, fill=new_color)


def draw_grid():
    # Размер сетки
    grid_size = 10

    # Цикл по линиям сетки
    for i in range(0, canvas.winfo_width(), grid_size):
        canvas.create_line(i, 0, i, canvas.winfo_height(), dash=(2, 2))
    for i in range(0, canvas.winfo_height(), grid_size):
        canvas.create_line(0, i, canvas.winfo_width(), i, dash=(2, 2))


def draw_line_dda(x1, y1, x2, y2, color="red"):
    # вычисляем разницу координат
    dx = x2 - x1
    dy = y2 - y1

    # определяем количество шагов для рисования
    steps = max(abs(dx), abs(dy))

    # вычисляем приращение координат на каждом шаге
    x_inc = dx / steps
    y_inc = dy / steps

    # инициализируем начальную точку
    x = x1
    y = y1

    global debug_mode
    # цикл по шагам
    for i in range(steps + 1):
        # рисуем пиксель по округленным координатам
        draw_pixel(round(x), round(y), color)

        # обновляем координаты
        x += x_inc
        y += y_inc
        if debug_mode:
            canvas.after(30)

# функция для рисования линии по алгоритму Брезенхема
def draw_line_bresenham(x1, y1, x2, y2, color="green"):
    # вычисляем разницу координат
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # определяем направление шага по осям
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    # инициализируем ошибку
    err = dx - dy

    # цикл по линии
    while True:
        # рисуем пиксель по текущим координатам
        draw_pixel(x1, y1, color)

        # если достигли конечной точки, выходим из цикла
        if x1 == x2 and y1 == y2:
            break

        # вычисляем двойную ошибку
        e2 = 2 * err

        # корректируем ошибку и координаты по оси x
        if e2 > -dy:
            err -= dy
            x1 += sx

        # корректируем ошибку и координаты по оси y
        if e2 < dx:
            err += dx
            y1 += sy

        # если включен режим отладки, то задерживаем рисование на 100 мс
        if debug_mode:
            canvas.after(100)

# функция для рисования сглаженной линии по алгоритму Ву
def draw_line_wu(x1, y1, x2, y2, color="blue"):
    # вычисляем разницу координат
    dx = x2 - x1
    dy = y2 - y1

    # определяем направление шага по осям
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    # меняем местами оси, если линия наклонена больше, чем под 45 градусов
    steep = abs(dy) > abs(dx)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx

    # вычисляем градиент линии
    # вычисляем градиент линии
    if dx != 0:  # проверяем, что dx не равен нулю
        gradient = dy / dx
    else:  # иначе, если dx равен нулю
        gradient = 0  # устанавливаем градиент равным нулю

    # инициализируем начальную точку
    x = round(x1)
    y = y1 + gradient * (x - x1)

    # цикл по линии
    while x != round(x2):
        # рисуем два пикселя с разной интенсивностью
        if steep:
            draw_pixel_with_intensity(y, x, 1 - (y - int(y)), color)
            draw_pixel_with_intensity(y + sy, x, y - int(y), color)
        else:
            draw_pixel_with_intensity(x, y, 1 - (y - int(y)), color)
            draw_pixel_with_intensity(x, y + sy, y - int(y), color)

        # обновляем координаты
        x += sx
        y += gradient

        # если включен режим отладки, то задерживаем рисование на 100 мс
        if debug_mode:
            canvas.after(100)

# функция для обработки событий мыши
def on_click(x, y, button, pressed):
    global first_point
    if button.name == "left" and pressed:
        # получаем координаты холста
        canvas_x = window.winfo_pointerx() - window.winfo_rootx()
        canvas_y = window.winfo_pointery() - window.winfo_rooty()

        # если нет первой точки, запоминаем ее координаты
        if first_point is None:
            first_point = (canvas_x, canvas_y)
        # если есть первая точка, рисуем отрезок между ней и второй точкой с помощью выбранного алгоритма
        else:
            if current_algorithm == "ЦДА":
                draw_line_dda(first_point[0], first_point[1], canvas_x, canvas_y, "red")
            elif current_algorithm == "Брезенхем":
                draw_line_bresenham(first_point[0], first_point[1], canvas_x, canvas_y, "blue")
            elif current_algorithm == "Ву":
                draw_line_wu(first_point[0], first_point[1], canvas_x, canvas_y, "green")
            # сбрасываем значение первой точки
            first_point = None

# функция для обработки нажатий на кнопки
def handler(algorithm):
    global current_algorithm
    # устанавливаем текущий выбранный алгоритм
    current_algorithm = algorithm


def set_debug_mode(new_mode):
    global debug_mode
    debug_mode = new_mode
    # Перерисовка холста
    canvas.delete("all")
    draw_grid()
    # ...

# Кнопка режима отладки
button_debug = tk.Button(window, text="Режим отладки", command=lambda: set_debug_mode(not debug_mode))
button_debug.pack()

# создаем кнопки для выбора алгоритма
button_dda = tk.Button(window, text="ЦДА", command=lambda: handler("ЦДА"))
button_dda.pack()

button_bresenham = tk.Button(window, text="Брезенхем", command=lambda: handler("Брезенхем"))
button_bresenham.pack()

button_wu = tk.Button(window, text="Ву", command=lambda: handler("Ву"))
button_wu.pack()

# инициализируем переменные
current_algorithm = "ЦДА"
first_point = None

# запускаем обработчик событий мыши
listener = Listener(on_click=on_click)
listener.start()

# запускаем приложение
window.mainloop()