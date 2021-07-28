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
        self.point = None


    def closeEvent(self, event):
        sys.exit() #Programm Closing
      
            
    def initUI(self):
        self.timer = QTimer() #Timer init
        self.timer.timeout.connect(self.update) #Timer init
        
        self.setWindowTitle('Moscow Metro Map Poppularity')#Title
        self.overlay = QImage()
        self.overlay.load('Moscow Metro Map Stations Popularity\\MainMap.bmp')

        pen = QPen(QColor(Qt.red))
        pen.setWidth(2)
        self.painter = QPainter(self.overlay)
        self.painter.setPen(pen)  
        self.showMaximized()
        self.timer.start(1000/30) #15 кадров в секунду
        
    def mousePressEvent(self, event):
        self.point = event.pos()

        # Вызов перерисовки виджета
        self.update()   


    def mouseReleaseEvent(self, event):
        self.point = None


    def paintEvent(self, event):
        super().paintEvent(event)

        # Если нет
        if not self.point:
            return

        # Рисовать будем на самом себе
        painter = QPainter(self)

        # Для рисования точки хватит setPen, но для других фигур (типо rect) понадобится setBrush
        painter.setPen(QPen(Qt.black, 20.0))

        # Рисование точки
        painter.drawPoint(self.point)


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        windowsWidth = self.frameGeometry().width()
        
        img = self.overlay.scaledToWidth(windowsWidth, Qt.FastTransformation)
        painter.drawImage(round((windowsWidth-img.width())/2, 0), 0, img)
        painter.end()
        QApplication.processEvents()



if __name__ == '__main__':
   #Window Settings:
   app = QApplication(sys.argv)#Init application
   ex = Example()#Init programm
   sys.exit(app.exec_())#Make Programm End when Window is closed