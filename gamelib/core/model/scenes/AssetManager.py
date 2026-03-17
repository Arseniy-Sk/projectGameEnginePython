class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.loading_queue = []
    
    def load_image_async(self, name, path):
        """Асинхронная загрузка изображений"""
        thread = threading.Thread(target=self._load_image, args=(name, path))
        thread.start()
    
    def _load_image(self, name, path):
        img = Image.open(path)
        self.images[name] = img
        global_bus.emit(self, 'asset_loaded', {'name': name, 'type': 'image'})
    
    def get_image(self, name):
        return self.images.get(name)
    
    def preload_scene_assets(self, scene_name, asset_list):
        """Предзагрузка всех ресурсов для сцены"""
        pass