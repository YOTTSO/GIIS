# Импортируем библиотеки
import tkinter as tk
import math

# Создаем окно приложения
window = tk.Tk()
window.title("Графический редактор")
window.geometry("800x600")

# Создаем холст для рисования
canvas = tk.Canvas(window, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT)

# Создаем панель инструментов
toolbar = tk.Frame(window, width=200, height=600, bg="lightgray")
toolbar.pack(side=tk.RIGHT, fill=tk.Y)

# Создаем переменные для хранения координат и типа кривой
x1 = y1 = x2 = y2 = None
curve_type = None

# Создаем функцию для рисования окружности
def draw_circle(x1, y1, x2, y2):
    # Вычисляем радиус окружности
    r = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # Рисуем окружность
    canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, outline="black")

# Создаем функцию для рисования эллипса
def draw_ellipse(x1, y1, x2, y2):
    # Вычисляем полуоси эллипса
    a = abs(x2 - x1) / 2
    b = abs(y2 - y1) / 2
    # Рисуем эллипс
    canvas.create_oval(x1 - a, y1 - b, x1 + a, y1 + b, outline="black")

# Создаем функцию для рисования гиперболы
def draw_hyperbola(x1, y1, x2, y2):
    # Вычисляем параметр гиперболы
    a = abs(x2 - x1) / 2
    # Рисуем ветви гиперболы
    for x in range(-300, 301):
        # Проверяем, что выражение под корнем не отрицательно
        if x ** 2 / a ** 2 - 1 >= 0:
            y = math.sqrt(a ** 2 * (x ** 2 / a ** 2 - 1))
            canvas.create_line(x1 + x, y1 + y, x1 + x + 1, y1 + y + 1, fill="black")
            canvas.create_line(x1 + x, y1 - y, x1 + x + 1, y1 - y - 1, fill="black")

# Создаем функцию для рисования параболы
def draw_parabola(x1, y1, x2, y2):
    # Вычисляем параметр параболы
    p = y2 - y1 / 2
    # Рисуем параболу
    for x in range(-300, 301):
        y = x ** 2 / (2 * p)
        canvas.create_line(x1 + x, y1 + y, x1 + x + 1, y1 + y + 1, fill="black")

# Создаем функцию для рисования сетки
def draw_grid():
    # Рисуем вертикальные линии
    for x in range(0, 601, 10):
        canvas.create_line(x, 0, x, 600, fill="gray")
    # Рисуем горизонтальные линии
    for y in range(0, 601, 10):
        canvas.create_line(0, y, 600, y, fill="gray")

# Создаем функцию для рисования кривой
def draw_curve(event):
    global x1, y1, x2, y2, curve_type
    # Если это первый клик мыши, то запоминаем координаты
    if x1 == None and y1 == None:
        x1 = event.x
        y1 = event.y
    # Если это второй клик мыши, то запоминаем координаты и рисуем кривую
    elif x2 == None and y2 == None:
        x2 = event.x
        y2 = event.y
        if curve_type == "Окружность":
            draw_circle(x1, y1, x2, y2)
        elif curve_type == "Эллипс":
            draw_ellipse(x1, y1, x2, y2)
        elif curve_type == "Гипербола":
            draw_hyperbola(x1, y1, x2, y2)
        elif curve_type == "Парабола":
            draw_parabola(x1, y1, x2, y2)
        # Сбрасываем координаты
        x1 = y1 = x2 = y2 = None

# Создаем функцию для выбора типа кривой
def choose_curve(type):
    global curve_type
    curve_type = type

# Создаем функцию для включения отладочного режима
def debug_mode():
    global points, index, speed
    # Рисуем сетку
    draw_grid()
    # Очищаем список точек
    points = []
    # Сбрасываем индекс
    index = 0
    # Сбрасываем скорость
    speed = 1
    # Вычисляем точки кривой в зависимости от типа
    if curve_type == "Окружность":
        # Вычисляем радиус окружности
        r = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Вычисляем угол в радианах
        angle = 0
        # Добавляем точки окружности в список
        while angle < 2 * math.pi:
            x = x1 + r * math.cos(angle)
            y = y1 + r * math.sin(angle)
            points.append((x, y))
            angle += 0.01
    elif curve_type == "Эллипс":
        # Вычисляем полуоси эллипса
        a = abs(x2 - x1) / 2
        b = abs(y2 - y1) / 2
        # Вычисляем угол в радианах
        angle = 0
        # Добавляем точки эллипса в список
        while angle < 2 * math.pi:
            x = x1 + a * math.cos(angle)
            y = y1 + b * math.sin(angle)
            points.append((x, y))
            angle += 0.01
    elif curve_type == "Гипербола":
        # Вычисляем параметр гиперболы
        a = abs(x2 - x1) / 2
        # Добавляем точки гиперболы в список
        for x in range(-300, 301):
            # Проверяем, что выражение под корнем не отрицательно
            if x ** 2 / a ** 2 - 1 >= 0:
                y = math.sqrt(a ** 2 * (x ** 2 / a ** 2 - 1))
                points.append((x1 + x, y1 + y))
                points.append((x1 + x, y1 - y))
    elif curve_type == "Парабола":
        # Вычисляем параметр параболы
        p = abs(y2 - y1) / 2
        # Добавляем точки параболы в список
        for x in range(-300, 301):
            y = x ** 2 / (2 * p)
            points.append((x1 + x, y1 + y))
    # Запускаем функцию для анимации кривой
    animate_curve()

def animate_curve():
    global points, index, speed
    # Если список точек не пустой
    if points:
        # Очищаем холст
        canvas.delete("all")
        # Рисуем сетку
        draw_grid()
        # Рисуем точки кривой до текущего индекса
        for i in range(index):
            x, y = points[i]
            canvas.create_line(x, y, x + 1, y + 1, fill="black")
        # Увеличиваем или уменьшаем индекс в зависимости от скорости
        index += speed
        # Проверяем, что индекс не выходит за границы списка
        if index < 0:
            index = 0
        elif index > len(points):
            index = len(points)
        # Повторяем функцию через 10 миллисекунд
        window.after(10, animate_curve)

# Создаем меню
menu = tk.Menu(window)
window.config(menu=menu)

# Создаем подменю "Линии второго порядка"
submenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Линии второго порядка", menu=submenu)
submenu.add_command(label="Окружность", command=lambda: choose_curve("Окружность"))
submenu.add_command(label="Эллипс", command=lambda: choose_curve("Эллипс"))
submenu.add_command(label="Гипербола", command=lambda: choose_curve("Гипербола"))
submenu.add_command(label="Парабола", command=lambda: choose_curve("Парабола"))

# Создаем подменю "Отладочный режим"
submenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Отладочный режим", menu=submenu)
submenu.add_command(label="Включить", command=debug_mode)

# Создаем кнопки на панели инструментов
button1 = tk.Button(toolbar, text="Окружность", command=lambda: choose_curve("Окружность"))
button1.pack(padx=10, pady=10)
button2 = tk.Button(toolbar, text="Эллипс", command=lambda: choose_curve("Эллипс"))
button2.pack(padx=10, pady=10)
button3 = tk.Button(toolbar, text="Гипербола", command=lambda: choose_curve("Гипербола"))
button3.pack(padx=10, pady=10)
button4 = tk.Button(toolbar, text="Парабола", command=lambda: choose_curve("Парабола"))
button4.pack(padx=10, pady=10)

# Привязываем событие клика мыши к холсту
canvas.bind("<Button-1>", draw_curve)

# Запускаем главный цикл приложения
window.mainloop()
