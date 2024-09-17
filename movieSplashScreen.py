from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class MovieSplashScreen(QtWidgets.QSplashScreen):

    def __init__(self, pathToGIF, flags, *args, **kwargs):
        self.movie = QtGui.QMovie(pathToGIF)
        self.movie.jumpToFrame(0)
        pixmap = QtGui.QPixmap(self.movie.frameRect().size()).scaled(300,300,Qt.KeepAspectRatio)
        QtWidgets.QSplashScreen.__init__(self, pixmap, flags, *args, **kwargs)
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, event):
        self.movie.start()

    def hideEvent(self, event):
        self.movie.stop()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap().scaled(300,300,Qt.KeepAspectRatio)
        
        pixmap.fill(QtCore.Qt.transparent)
        w = pixmap.size().width()
        h = pixmap.size().height()
        
        clipPath = QtGui.QPainterPath()
        clipPath.addRoundedRect(QtCore.QRectF(0, 0, w, h), w//15, h//15)
            
        painter.setClipPath(clipPath)
        # self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, self.movie.currentPixmap().scaled(300,300,Qt.KeepAspectRatio))
        painter.end()