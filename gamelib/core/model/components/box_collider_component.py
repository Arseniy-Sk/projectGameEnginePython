from gamelib.core.model.components.image_for_base_gameObj import Component

class Box_collider(Component):
    def __init__(self, is_trigger: bool):
        super().__init__()
        self.is_trigger = is_trigger
        self.obj2 = None
        self.function = None
    
    def set_game_object(self, obj):
        """Устанавливает ссылку на игровой объект"""
        super().set_game_object(obj)
    
    def check_collision(self, obj2, function=None):
        '''Проверка на столкновение с указанным объектом'''
        self.obj2 = obj2
        self.function = function
        
        if not self.obj or not self.obj.canvas:
            print("ERROR: No object or canvas provided!")
            return
        
        # Запускаем проверку коллизий
        self._check_collision_loop()
    
    def _check_collision_loop(self):
        """Рекурсивно проверяет коллизии"""
        if not self.obj or not self.obj2 or not self.obj.canvas:
            return
        
        # Get object coordinate
        if hasattr(self.obj, 'get_coordinates'):
            coords1 = self.obj.get_coordinates()
        else:
            return
            
        if hasattr(self.obj2, 'get_coordinates'):
            coords2 = self.obj2.get_coordinates()
        else:
            return
            
        # Check collision with coordinate
        if (coords1[0] < coords2[2] and coords1[2] > coords2[0] and
            coords1[1] < coords2[3] and coords1[3] > coords2[1]):

            if not self.is_trigger:
                if hasattr(self.obj2, 'components'):
                    for component in self.obj2.components:
                        if hasattr(component, 'stop_gravity'):
                            component.stop_gravity()
                            break
            else:
                if self.function:
                    self.function()
        
        # Plan the next check
        if self.obj and self.obj.canvas:
            self.obj.canvas.after(100, self._check_collision_loop)