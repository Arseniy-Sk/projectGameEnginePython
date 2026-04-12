import tkinter as tk


def create_label(root, content=" ", font=("Helvetica", 16)):
    return tk.Label(root, text=content, font=font)


def create_button(root, text="Button", command=None, font=("Helvetica", 12)):
    return tk.Button(root, text=text, command=command, font=font)