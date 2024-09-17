"""Файл для враппера
"""

from logger import logging

class Wrapper(object):
    """Врапаем значение с дополнительным функционалом в ввиде сигнала при изменении
    """
    def __init__(self, v):
        """инициализация"""
        self._value = v
        self._observers = []

    @property
    def value(self):
        """получение значения"""
        return self._value

    @value.setter
    def value(self, value):
        """установка значения

        Args:
            value (optional): новое значение
        """
        self._value = value
        for callback in self._observers:
            logging.debug('announcing change')
            callback(self._value)

    def bind_to(self, callback):
        """функция для установкий обработчиков сигнала при изменении значения

        Args:
            callback (function): вызываеться при изменении значения
        """
        logging.debug("bind")
        self._observers.append(callback)