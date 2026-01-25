from gamelib.core.model.components.image_for_base_gameObj import Component

class Box_collider(Component):
    def __init__(self, obj1, root, is_trigger: bool):
        super().__init__(obj1)
        self.root = root
        self.is_trigger = is_trigger
    
    def check_collision(self, obj2, canvas, root, function):
        '''Проверка на столкновение с указанным объектом'''
        self.obj2 = obj2
        self.canvas = canvas
        self.root = root

        if not canvas:
            print("ERROR: No canvas provided!")
            return

        # Get object coordinate
        if hasattr(self.obj, 'get_coordinates'):
            coords1 = self.obj.get_coordinates()
        else:
            return
            
        if hasattr(obj2, 'get_coordinates'):
            coords2 = obj2.get_coordinates()
        else:
            return
            
        # Check collosion with coordinate
        if (coords1[0] < coords2[2] and coords1[2] > coords2[0] and
            coords1[1] < coords2[3] and coords1[3] > coords2[1]):

            if not self.is_trigger:
                if hasattr(obj2, 'components'):
                    for component in obj2.components:
                        if hasattr(component, 'stop_gravity'):
                            component.stop_gravity()
                            break
            else:
                if self.function:
                    self.function()
        
        # Plan the next check
        self.root.after(100, lambda: self.check_collision(obj2, canvas, root, function))

        


