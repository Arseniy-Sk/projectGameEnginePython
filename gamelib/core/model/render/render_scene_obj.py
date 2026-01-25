import tkinter as tk 

def create_canvas(root, width, height, background):
    canvas = tk.Canvas(root, width=width, height=height, bg=background)
    canvas.pack()
    return canvas


def render_rectangle(canvas, o1, o2, o3, o4, color):
    canvas.create_rectangle(o1, o2, o3, o4, fill=color, outline=color)


def render_set_position(canvas, obj, dx, dy):
    canvas.move(obj, dx, dy)



def show_scene(scene):
    scene.canvas.pack()


def close_scene(scene):
    scene.canvas.pack_forget()