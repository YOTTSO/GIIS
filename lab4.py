import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


points = np.array([[-1, -1, -1],
                   [1, -1, -1],
                   [1, 1, -1],
                   [-1, 1, -1],
                   [-1, -1, 1],
                   [1, -1, 1],
                   [1, 1, 1],
                   [-1, 1, 1]])


edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]


def transform(points, matrix):
    return np.dot(points, matrix)


def translation_matrix(dx, dy, dz):
    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                     [0, 0, 0, 1]])


def rotation_matrix(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def scaling_matrix(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])

def plot_cube(points, edges):
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(111, projection='3d')
    for edge in edges:
        p1, p2 = points[edge[0]], points[edge[1]]
        ax.plot3D(*zip(p1, p2), color="b")
    return fig


def update_plot(angle, dx, dy, dz, sx, sy, sz):
    global points
    points = np.hstack((points, np.ones((points.shape[0], 1))))
    points = transform(points, translation_matrix(dx, dy, dz))
    points = transform(points, rotation_matrix(angle))
    points = transform(points, scaling_matrix(sx, sy, sz))
    points = points[:, :3]
    fig = plot_cube(points, edges)
    canvas.figure = fig
    canvas.draw()


root = tk.Tk()
root.wm_title("3D Object Transformations")


fig = plot_cube(points, edges)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)

slider_width = 5
angle_slider = tk.Scale(root, from_=0, to=360, orient='horizontal', label='Rotate', width=slider_width)
angle_slider.pack(fill=tk.X)

dx_slider = tk.Scale(root, from_=-10, to=10, orient='horizontal', label='Translate X',width=slider_width)
dx_slider.pack(fill=tk.X)

dy_slider = tk.Scale(root, from_=-10, to=10, orient='horizontal', label='Translate Y', width=slider_width)
dy_slider.pack(fill=tk.X)

dz_slider = tk.Scale(root, from_=-10, to=10, orient='horizontal', label='Translate Z', width=slider_width)
dz_slider.pack(fill=tk.X)


sx_slider = tk.Scale(root, from_=0.1, to=5, resolution=0.1, orient='horizontal', label='Scale X')
sx_slider.pack(fill=tk.X)

sy_slider = tk.Scale(root, from_=0.1, to=5, resolution=0.1, orient='horizontal', label='Scale Y')
sy_slider.pack(fill=tk.X)

sz_slider = tk.Scale(root, from_=0.1, to=5, resolution=0.1, orient='horizontal', label='Scale Z')
sz_slider.pack(fill=tk.X)


apply_button = tk.Button(root, text="Apply Transformations", command=lambda: update_plot(
    angle_slider.get(),
    dx_slider.get(),
    dy_slider.get(),
    dz_slider.get(),
    sx_slider.get(),
    sy_slider.get(),
    sz_slider.get()
))

apply_button.pack()

tk.mainloop()
