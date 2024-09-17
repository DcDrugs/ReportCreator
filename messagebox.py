""" файл для настройки над обычным диалогом сообщений

"""

import sys
from PyQt5.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    """класс диалога для руссифицирования кнопок
    """
    def __init__(self, title: str, text: str, parent=None):
        """инициализация

        Args:
            title (str): заголовок диалога
            text (str): текст диалога
            parent (_type_, optional): родительский класс. Defaults to None.
        """
        super().__init__(parent)
        self.res = "нет"
        self.setIcon(QMessageBox.Warning)
        self.setText(text)
        self.setWindowTitle(title)
        self.no = self.addButton("нет", QMessageBox.NoRole)
        self.yes = self.addButton("да", QMessageBox.YesRole)
        self.buttonClicked.connect(self.onClicked)

    def execute(self):
        """Запуск диалога

        Returns:
            QMessageBox.Role: возвращает роль кнопки, на которую нажали 
        """
        self.exec_()
        if self.res == "да":
            return QMessageBox.YesRole
        else:
            return QMessageBox.NoRole
        
    def onClicked(self, btn):
        """Обработчик нажатия на кнопку
        """
        self.res = btn.text()