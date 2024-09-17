""" файл для работы с многопоточностью и qt
"""
from typing import Callable

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QGuiApplication


class InvokeMethod(QObject):
    """класс для обработки потоков в общем потоке

    Args:
        QObject (_type_): _description_
    """
    def __init__(self, method: Callable):
        super().__init__()

        main_thread = QGuiApplication.instance().thread()
        self.moveToThread(main_thread)
        self.setParent(QGuiApplication.instance())
        self.method = method
        self.called.connect(self.execute)
        self.called.emit()

    called = pyqtSignal()

    @pyqtSlot()
    def execute(self):
        self.method()
        self.setParent(None)