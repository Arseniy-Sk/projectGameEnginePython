import tkinter as tk


def prevenous_sym_code_keys(root, key_sym):
    return root.tk.call("keysym", key_sym)


def bind_def_key(key_sym, function, root):
    root.bind(prevenous_sym_code_keys(root, key_sym), function)