from gamelib.core.model.render.render_input_system import *


class InputManager():
    key = ' '
    def __init__(self, root):
            self.root = root

            def key_pressed(event):
                self.key = event.keysym

            # Привязываем событие нажатия клавиши ко всему окну
            root.bind('<Key>', key_pressed)
    