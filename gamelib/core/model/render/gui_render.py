import tkinter as tk

def create_label(root, content=" ", font=("Helvetica", 16)):
    """
    Создает текстовую метку на указанном root-виджете
    """
    label = tk.Label(root, text=content, font=font)
    return label


def create_button(root, text="Button", command=None, font=("Helvetica", 12)):
    """
    Создает кнопку на указанном root-виджете
    """
    button = tk.Button(root, text=text, command=command, font=font)
    return button