"""файл для наблюдения за файлом/файлами
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import json
from settings import SETTINGS, globalConfig
from logger import logging


class MyHandler(FileSystemEventHandler):
    """Обработчик изменений с файлом/файлами
    """
    def __init__(self):
        """инициализация
        """
        self.last_content = None

    def on_modified(self, event):
        """обработчик изменения файла
            следим за файлом настройки
        """
        global globalConfig
        if event.is_directory or not event.src_path.endswith(SETTINGS + '.json'):
            return 
        with open(event.src_path, mode="r", encoding=sys.getdefaultencoding()) as f:
            content = f.read()
            if content == self.last_content:
                return
            self.last_content = content
        try:
            globalConfig.value = json.loads(self.last_content)
        except BaseException as ex:
            logging.error("BaseException",exc_info=True)

def start_observer():
    """функция запуска отслеживания
    """
    observer = Observer()
    observer.schedule(MyHandler(), path='./', recursive=False)
    observer.start()