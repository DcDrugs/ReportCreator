"""Это загрузчик для приложения, тут описаны все утилиты, которые запускаются рядом 
с приложением и обеспечивают работоспособность и функциональность приложения
"""
import onefilebug
import sys


import multiprocessing
import time

class MyProcess(multiprocessing.Process):
    _Popen = onefilebug._Popen

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        self.show()

    def shutdown(self):
        self.exit.set()
 
    def show(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication
        from build.resource_rc import qInitResources
        from runner import callMe
        app = QApplication(sys.argv)
        
        from movieSplashScreen import MovieSplashScreen
        pathToGIF = ":/images/icons/QSplashScreen.gif"
        splash = MovieSplashScreen(pathToGIF, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        splash.show()
        app.thread().sleep(1)
        while not self.exit.is_set():
            app.processEvents()
    
from PyQt5.QtGui import QPixmap 
from PyQt5.QtWidgets import QSplashScreen 

if __name__ == '__main__':
    multiprocessing.freeze_support()
    process = MyProcess()
    process.start()
    
    if not getattr(sys, 'frozen', False):
        import os 
        import os.path
        os.system("python ./qrc/dynamic_add.py")
        os.system("pyrcc5 qrc\\resourcebuild.qrc -o build\\resource_rc.py")
        os.system("pyuic5 -x ui\main.ui -o build\main_ui.py")
        os.system("pyuic5 -x ui\homeGUI.ui -o build\homeGUI_ui.py")
        os.system("pyuic5 -x ui\quick_referenceGUI.ui -o build\quick_referenceGUI_ui.py")

    
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication
    from build.resource_rc import *
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    
    # отрисовываем экран загрузки, пока наше приложение не загрузилось
    # pix = QPixmap( ":/images/icons/QSplashScreen.png" ).scaled(300,300,Qt.KeepAspectRatio)
    # splashScreen = QSplashScreen ( pix, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    # import time
    # splashScreen.setWindowOpacity(0)
    # splashScreen.show()
    # app.thread().sleep(1)
    # app.processEvents()
    # @callMe
    # def f():
    #     opaqueness = 0.0
    #     step = 0.1
    #     while opaqueness < 1:
    #         splashScreen.setWindowOpacity(opaqueness)
    #         time.sleep(step) # Gradually appears
    #         opaqueness+=step
    #     time.sleep(1)
    
    # f()
    
    from PyQt5 import QtCore
    # стиль приложения
    f = QtCore.QFile(":/files/styles/style.qss")
    f.open(QtCore.QIODevice.ReadOnly)
    if f.isOpen():
        style_str = str(f.readAll().data(), encoding='utf-8')
        f.close()
        app.setStyleSheet(style_str)
    from watcher import start_observer
    from GUI import App
    
    # запускаем слежку за фаилом настроек
    start_observer()
    from settings import set_settings
    set_settings()
    
    ex = App()
    process.shutdown()
    # splashScreen.finish(ex)
    
    ex.show()
    sys.exit(app.exec())