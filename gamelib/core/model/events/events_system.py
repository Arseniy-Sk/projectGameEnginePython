#imports

class Event:
    def __init__(self, source, event_type, data=None):
        self.source = source
        self.type = event_type
        self.data = data


class EventBus:
    """Шина событий"""
    def __init__(self):
        # Ключ: (source, event_type) — может быть None для любого источника/типа
        self._subscribers = {}

    def subscribe(self, source, event_type, callback):
        """
        Подписаться на события.
        :param source: объект-источник (или None для всех источников)
        :param event_type: строка (или None для всех типов)
        :param callback: функция, принимающая один аргумент Event
        """
        key = (source, event_type)
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)

    def unsubscribe(self, source, event_type, callback):
        """Отписаться от события."""
        key = (source, event_type)
        if key in self._subscribers:
            try:
                self._subscribers[key].remove(callback)
            except ValueError:
                pass

    def emit(self, source, event_type, data=None):
        """
        Испустить событие от указанного источника с заданным типом.
        """
        event = Event(source, event_type, data)

        # Точное совпадение (source, event_type)
        key = (source, event_type)
        if key in self._subscribers:
            for cb in self._subscribers[key]:
                cb(event)

        # Все события от этого источника (source, None)
        key = (source, None)
        if key in self._subscribers:
            for cb in self._subscribers[key]:
                cb(event)

        # Все события этого типа от любых источников (None, event_type)
        key = (None, event_type)
        if key in self._subscribers:
            for cb in self._subscribers[key]:
                cb(event)

        # Все события вообще (None, None)
        key = (None, None)
        if key in self._subscribers:
            for cb in self._subscribers[key]:
                cb(event)


# Global event system
global_bus = EventBus()