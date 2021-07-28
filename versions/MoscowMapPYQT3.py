import sys
from time import time
from random import random
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QDesktopWidget)
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QPolygonF,
                                QPixmap, QPalette, QImage)
from PyQt5.QtCore import QCoreApplication, Qt, QPoint, QPointF, QRect, QTimer
from math import sqrt, sin, cos, pi, radians

SCREEN_WIDTH    = 100
SCREEN_HEIGHT   = 500

SQUARE_LENGTH   = 400
DEPTH           = 8

BASE_ANGLE      = 45

ANIMATE         = False



class Example(QWidget):
    overlay: QImage #Overlay(Накладываем) Picture on Window
    timer: QTimer #Timet init
    painter: QPainter

    def __init__(self):
        super().__init__()
        self.initUI()


    def mousePressEvent(self, event):
        WindowW = self.frameGeometry().width()#    WindowSize
        WindowH = self.frameGeometry().height()#  WindowSize
        imgH = self.overlay.height()# Picture Size
        imgW = self.overlay.width()#  Picture Size

        self.point = event.pos()
        _ResultY = self.point.y() / (WindowH / 100)
        ResultY = (imgH / 100) * _ResultY

        _ResultX = self.point.x() / (WindowW / 100)
        ResultX = (imgW / 100) * _ResultX

        self.painter.drawLine(QPoint(0,0), QPoint(ResultX, ResultY))#Drawing
        self.update()#Redraw


    def mouseReleaseEvent(self, event):
        self.point = None


    def closeEvent(self, event):
        sys.exit() #Programm Closing
      
            
    def initUI(self):
        self.timer = QTimer() #Timer init
        self.timer.timeout.connect(self.update) #Timer init
        self.setWindowTitle('Moscow Metro Map Poppularity')#Title
        self.point = None

        self.overlay = QImage()
        self.overlay.load('Moscow Metro Map Stations Popularity\\MainMap.bmp')

        pen = QPen(QColor(Qt.red))
        pen.setWidth(2)
        self.painter = QPainter(self.overlay)
        self.painter.setPen(pen)  
        self.showMaximized()
        self.timer.start(1000/15) #15 кадров в секунду


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        windowsWidth = self.frameGeometry().width()
        windowsHeight = self.frameGeometry().height()
        
        img = self.overlay.scaledToHeight(windowsHeight, Qt.FastTransformation)
        #painter.drawImage(round((windowsWidth-img.width())/2, 0), 0, img)
        painter.drawImage(round((windowsWidth-img.width())/2, 0), 0, img)
        painter.end()
        del painter
       



if __name__ == '__main__':
   #Window Settings:
   app = QApplication(sys.argv)#Init application
   ex = Example()#Init programm
   sys.exit(app.exec_())#Make Programm End when Window is closed