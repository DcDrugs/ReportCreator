"""файл, где описываеться вся работа с GUI
"""

from build.quick_referenceGUI_ui import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
        
class QuickReferenceGUI(QtWidgets.QWidget):
    """ Класс обработки окна
    """
    def __init__(self):
        """инициализация
        """
        super(QtWidgets.QWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        fileName = ":/files/docs/_build/html/index.html"
        self.ui.textBrowser.setSource(QtCore.QUrl.fromLocalFile(fileName))
        