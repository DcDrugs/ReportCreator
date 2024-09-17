"""файл, где описываеться вся работа с GUI
"""

from build.homeGUI_ui import Ui_Form

from pyqtgraph.parametertree import ParameterTree
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from invoke import InvokeMethod

from doctemp import print_docx, get_list
from settings import  PNAME, SETTINGS, JSON_KEY, EXCEL, COMBOBOX, TEMPLATE, RESULT, JSON_TYPE, JSON_VALUE, globalConfig, read_config
from logger import logging
from messagebox import MessageBox

from PyQt5.QtWidgets import QMessageBox
        
from utils import create_params

class HomeGUI(QtWidgets.QWidget):
    """ Класс обработки окна
    """
    def __init__(self):
        """инициализация
        """
        super(QtWidgets.QWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # completers only work for editable combo boxes. QComboBox.NoInsert prevents insertion of the search text
        self.ui.comboBox.setEditable(True)
        self.ui.comboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)

        # change completion mode of the default completer from InlineCompletion to PopupCompletion
        self.ui.comboBox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.ui.comboBox.completer().setFilterMode(Qt.MatchContains)

        
        def onClick(checked):
            """Обработка нажатия кнопки "напечатать"
            """
            import os.path
            if os.path.isfile(globalConfig.find(RESULT)[JSON_VALUE]) and MessageBox(PNAME, os.path.basename(globalConfig.find(RESULT)[JSON_VALUE]) + " уже существует, заменить?").execute() == QMessageBox.NoRole:
                return
            try:
                print_docx(self.ui.comboBox.currentText(),
                        globalConfig.find(EXCEL)[JSON_VALUE],
                        globalConfig.find(COMBOBOX)[JSON_VALUE], 
                        globalConfig.find(TEMPLATE)[JSON_VALUE], 
                        globalConfig.find(RESULT)[JSON_VALUE],
                        { v.value[JSON_KEY]: v.value[JSON_VALUE] for v in globalConfig.items() if v.value[JSON_TYPE] != "group" })
                QtWidgets.QMessageBox.information(None, 'Успех', f'Операция выполнена успешно')
            except BaseException as error:
                # import traceback 
                # traceback.print_exc() 
                logging.error("BaseException",exc_info=True)
                QtWidgets.QMessageBox.warning(None, 'Неудача', str(error))
    
        self.ui.pushButton.clicked.connect(onClick)
        
        def set_combobox():
            """функция для заполнения combobox
            """
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(
                get_list(
                    globalConfig.find(EXCEL)[JSON_VALUE],
                    globalConfig.find(COMBOBOX)[JSON_VALUE]    
                )
            )   

        tree = ParameterTree(self)
        global last_combobox, last_excel
        last_combobox = ""
        last_excel = ""
        def f(args = None):
            def l ():
                global last_combobox, last_excel
                tree.setParameters(create_params())
                combobox = globalConfig.find(COMBOBOX)[JSON_VALUE]
                excel = globalConfig.find(EXCEL)[JSON_VALUE]
                if combobox != last_combobox or excel != last_excel:
                    set_combobox()
                    last_combobox = combobox
                    last_excel = excel
                
            InvokeMethod(lambda : l())
            
        tree.header().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.ui.verticalLayout_3.addWidget(tree)
        
        globalConfig.bind_to(f)
        f()  