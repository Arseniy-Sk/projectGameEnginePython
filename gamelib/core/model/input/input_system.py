from gamelib.core.model.render.render_input_system import *

class InputManager():
    def __init__(self, root):
        self.root = root
        self.key = ' '
        self.keycode = None

        def key_pressed(event):
            self.key = event.keysym
            self.keycode = event.keycode

        root.bind('<Key>', key_pressed)

    def is_key_down(self, expected_key):
        letter_keycodes = {
            'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73,
            'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82,
            's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90
        }

        if isinstance(expected_key, int):
            return self.keycode == expected_key
        elif isinstance(expected_key, str):
            if expected_key.lower() in ['space', 'return', 'escape', 'up', 'down', 'left', 'right']:
                return self.key.lower() == expected_key.lower()
            
            elif len(expected_key) == 1 and expected_key.isalpha():
                expected_code = letter_keycodes.get(expected_key.lower())
                if expected_code is not None:
                    return self.keycode == expected_code
                else:
                    return self.key.lower() == expected_key.lower()
            else:
                return self.key == expected_key
        return False