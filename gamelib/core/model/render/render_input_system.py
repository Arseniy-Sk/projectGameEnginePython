import tkinter as tk


def prevenous_sym_code_keys(root, key_sym):
    key_code = root.tk.call("keysym", key_sym)

    return key_code

def bind_def_key(key_sym, function, root):
    key_code = prevenous_sym_code_keys(root, key_sym)
    root.bind(key_code, function)

