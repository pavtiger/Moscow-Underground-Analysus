import sys
import os
from time import time
from random import random, randrange
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QDesktopWidget)
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QPolygonF,
                                QPixmap, QPalette, QImage)
from PyQt5.QtCore import QCoreApplication, Qt, QPoint, QPointF, QRect, QTimer
from math import sqrt, sin, cos, pi, radians

SCREEN_WIDTH  = 100
SCREEN_HEIGHT = 500

SQUARE_LENGTH = 400
DEPTH         = 8

BASE_ANGLE    = 45

ANIMATE       = False

FILE_NAME     = 'ArrOfStations.txt'



class Example(QWidget):
    overlay: QImage #Overlay(Накладываем) Picture on Window
    timer: QTimer #Timet init
    painter: QPainter

    arr_points: list
    DeltaX: int
    DeltaY: int
    SelfHeight: int
    LastAngle: int
    LastMousePosition: QPoint
    

    def __init__(self):
        super().__init__()
        self.initUI()


    def mousePressEvent(self, event):
        if event.button() == 2:
            mousePoint = event.pos()

            self.LastMousePosition = mousePoint
            
            WindowW = self.frameGeometry().width()#   WindowSize
            WindowH = self.frameGeometry().height()#  WindowSize
            imgH = self.overlay.height()# Original Picture Size
            imgW = self.overlay.width()#  Original Picture Size
            
            img = self.overlay.scaledToHeight(self.SelfHeight, Qt.FastTransformation)

            #AdjX = (WindowW-img.width())/2
            ResultX = imgW * (mousePoint.x() - self.DeltaX) / img.width()

            ResultY = imgH / 100 * (mousePoint.y() / (self.SelfHeight / 100))

            radius = 10
            self.painter.drawEllipse(QPoint(ResultX, ResultY), radius, radius)
            self.arr_points.append((ResultX, ResultY))
            #print([(round(x[0]), round(x[1])) for x in self.arr_points])
            self.update()#Redraw


    def FileSaving(self, fileName: str):
        with open(fileName, 'w') as f:
            for item in self.arr_points:
                f.write(';'.join(str(x) for x in item) + '\n')
            f.close()


    def mouseReleaseEvent(self, event):
        self.point = None


    def closeEvent(self, event):
        self.FileSaving(FILE_NAME)
        sys.exit() #Programm Closing
      
            
    def initUI(self):
        self.showMaximized()
        #self.showNormal()
        self.arr_points = []
        self.LastAngle = 0
        self.timer = QTimer() #Timer init
        self.timer.timeout.connect(self.update)# Timer init
        self.setWindowTitle('Moscow Metro Map Poppularity')# Title
        self.point = None
        self.DeltaX = 0
        self.DeltaY = 0
        self.SelfHeight = self.frameGeometry().height()
        self.LastMousePosition = QPoint(0, 0)

        self.overlay = QImage()
        self.overlay.load('Moscow Metro Map Stations Popularity\\MainMap.bmp')

        pen = QPen(QColor(Qt.red))
        pen.setWidth(5)
        self.painter = QPainter(self.overlay)
        self.painter.setPen(pen)  
        self.painter.Antialiasing  = True

        self.timer.start(1000/30) #30 кадров в секунду


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        #windowsWidth = self.frameGeometry().width()
        windowsHeight = self.frameGeometry().height()
        
        img = self.overlay.scaledToHeight(self.SelfHeight, 0)
        painter.drawImage(self.DeltaX, self.DeltaY, img)
        painter.end()
        del painter


    def mouseMoveEvent(self, event):
        CurentPos = event.pos()
        self.DeltaX -= self.LastMousePosition.x()-CurentPos.x()
        self.DeltaY -= self.LastMousePosition.y()-CurentPos.y()
        self.LastMousePosition = event.pos()
       

    def wheelEvent(self, event):
        #print(str(event.angleDelta()))
        self.SelfHeight += (event.angleDelta().y()) / 10
        self.LastAngle = event.angleDelta().y()


    def resizeEvent(self, event):
        self.SelfHeight = self.frameGeometry().height()


if __name__ == '__main__':
   #Window Settings:
   app = QApplication(sys.argv)#Init application
   ex = Example()#Init programm
   sys.exit(app.exec_())#Make Programm End when Window is closed