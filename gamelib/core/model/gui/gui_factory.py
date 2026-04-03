# gamelib/core/model/gui/gui_factory.py
import tkinter as tk


class Label:
    """Простая текстовая метка"""
    
    def __init__(self, parent, text="", font=("Arial", 12), color="white", bg=None):
        self.widget = tk.Label(parent, text=text, font=font, fg=color, bg=bg)
    
    def set_text(self, text):
        self.widget.config(text=text)
    
    def set_color(self, color):
        self.widget.config(fg=color)
    
    def set_font(self, font):
        self.widget.config(font=font)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
        return self
    
    def place(self, x, y):
        self.widget.place(x=x, y=y)
        return self


class Button:
    """Простая кнопка"""
    
    def __init__(self, parent, text="", command=None, font=("Arial", 12), 
                 color="white", bg="#333333"):
        self.widget = tk.Button(
            parent, text=text, command=command, font=font,
            fg=color, bg=bg, relief="flat", padx=10, pady=5
        )
    
    def set_text(self, text):
        self.widget.config(text=text)
    
    def set_color(self, color):
        self.widget.config(fg=color)
    
    def set_bg(self, bg):
        self.widget.config(bg=bg)
    
    def set_command(self, command):
        self.widget.config(command=command)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
        return self
    
    def place(self, x, y):
        self.widget.place(x=x, y=y)
        return self


class CheckBox:
    """Простой чекбокс"""
    
    def __init__(self, parent, text="", default=False, on_change=None,
                 color="white", bg=None):
        self.var = tk.BooleanVar(value=default)
        self.on_change = on_change
        self.widget = tk.Checkbutton(
            parent, text=text, variable=self.var,
            command=self._on_click, fg=color, bg=bg,
            selectcolor=bg if bg else parent.cget('bg'),
            relief="flat"
        )
    
    def _on_click(self):
        if self.on_change:
            self.on_change(self.is_checked())
    
    def is_checked(self):
        return self.var.get()
    
    def set_checked(self, checked):
        self.var.set(checked)
        if self.on_change:
            self.on_change(checked)
    
    def set_text(self, text):
        self.widget.config(text=text)
    
    def set_color(self, color):
        self.widget.config(fg=color)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
        return self


class Slider:
    """Простой ползунок"""
    
    def __init__(self, parent, from_=0, to=100, default=50, on_change=None,
                 length=200, bg=None):
        self.on_change = on_change
        self.widget = tk.Scale(
            parent, from_=from_, to=to, orient='horizontal',
            command=self._on_change, length=length, bg=bg,
            relief="flat", highlightthickness=0
        )
        self.widget.set(default)
    
    def _on_change(self, value):
        if self.on_change:
            self.on_change(int(float(value)))
    
    def get_value(self):
        return self.widget.get()
    
    def set_value(self, value):
        self.widget.set(value)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
        return self


class DropDown:
    """Простой выпадающий список"""
    
    def __init__(self, parent, items=[], default=None, on_select=None,
                 color="white", bg="#333333"):
        self.on_select = on_select
        self.var = tk.StringVar(value=default if default else (items[0] if items else ""))
        self.widget = tk.OptionMenu(parent, self.var, *items, command=self._on_select)
        self.widget.config(fg=color, bg=bg, relief="flat", highlightthickness=0)
    
    def _on_select(self, value):
        if self.on_select:
            self.on_select(value)
    
    def get_selected(self):
        return self.var.get()
    
    def set_items(self, items):
        menu = self.widget["menu"]
        menu.delete(0, "end")
        for item in items:
            menu.add_command(label=item, command=lambda v=item: self.var.set(v))
    
    def set_color(self, color):
        self.widget.config(fg=color)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
        return self


class TextInput:
    """Простое поле ввода"""
    
    def __init__(self, parent, placeholder="", width=20, on_change=None,
                 color="white", bg="#333333", placeholder_color="gray"):
        self.on_change = on_change
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.text_color = color
        
        self.widget = tk.Entry(parent, width=width, fg=placeholder_color, bg=bg,
                               relief="flat", highlightthickness=0)
        
        if placeholder:
            self.widget.insert(0, placeholder)
            self.widget.bind('<FocusIn>', self._clear_placeholder)
            self.widget.bind('<FocusOut>', self._set_placeholder)
        
        self.widget.bind('<KeyRelease>', self._on_change)
    
    def _clear_placeholder(self, event):
        if self.widget.get() == self.placeholder:
            self.widget.delete(0, tk.END)
            self.widget.config(fg=self.text_color)
    
    def _set_placeholder(self, event):
        if not self.widget.get():
            self.widget.insert(0, self.placeholder)
            self.widget.config(fg=self.placeholder_color)
    
    def _on_change(self, event):
        if self.on_change:
            self.on_change(self.get_text())
    
    def get_text(self):
        text = self.widget.get()
        if text == self.placeholder:
            return ""
        return text
    
    def set_text(self, text):
        self.widget.delete(0, tk.END)
        self.widget.insert(0, text)
        self.widget.config(fg=self.text_color)
    
    def set_color(self, color):
        self.text_color = color
        if self.widget.get() != self.placeholder:
            self.widget.config(fg=color)
    
    def set_bg(self, bg):
        self.widget.config(bg=bg)
    
    def clear(self):
        self.set_text("")
        if self.placeholder:
            self.widget.insert(0, self.placeholder)
            self.widget.config(fg=self.placeholder_color)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
        return self


class Panel:
    """Простой контейнер"""
    
    def __init__(self, parent, bg=None):
        self.widget = tk.Frame(parent, bg=bg)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
        return self
    
    def place(self, x, y):
        self.widget.place(x=x, y=y)
        return self


__all__ = ['Label', 'Button', 'CheckBox', 'Slider', 'DropDown', 'TextInput', 'Panel']