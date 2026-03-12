from gamelib.core.model.render.gui_render import *
import tkinter as tk

class GUI:
    def __init__(self, root):
        self.root = root


class Label(GUI):
    def __init__(self, root, content, font=("Helvetica", 16)):
        super().__init__(root)
        self.label = create_label(self.root, content, font)
        self.content = content
        self.font = font
    
    def set_text(self, text):
        """Изменяет текст метки"""
        self.label.config(text=text)
        self.content = text
    
    def pack(self, **kwargs):
        """Упаковывает метку"""
        self.label.pack(**kwargs)


class Button(GUI):
    def __init__(self, root, text, command=None, font=("Helvetica", 12)):
        super().__init__(root)
        self.button = tk.Button(
            self.root,
            text=text,
            command=command,
            font=font
        )
        self.button.pack()
        self.text = text
        self.command = command
    
    def set_text(self, text):
        """Изменяет текст кнопки"""
        self.button.config(text=text)
        self.text = text
    
    def pack(self, **kwargs):
        """Упаковывает кнопку"""
        self.button.pack(**kwargs)