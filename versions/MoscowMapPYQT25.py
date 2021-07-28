import sys
import os
from time import time
from pathlib import Path
from random import random, randrange
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QDesktopWidget)
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QPolygonF,
                                QPixmap, QPalette, QImage)
from PyQt5.QtCore import QCoreApplication, Qt, QPoint, QPointF, QRect, QTimer
from math import sqrt, sin, cos, pi, radians

SCREEN_WIDTH  = 100
SCREEN_HEIGHT = 500

RADIUS        = 30
ADDITIONAL    = 5

FILE_NAME     = '!StationsLine'
FILE_STATIONS_NAME = '!Stations.txt'
FILE_DATA_NAME = '!StationSize.txt'



class Example(QWidget):
    overlay: QImage #Overlay(Накладываем) Picture on Window
    timer: QTimer #Timet init
    painter: QPainter

    Colors: list
    arr_points: list
    DeltaX: int
    DeltaY: int
    SelfHeight: int
    LastAngle: int
    stationSize: list
    LastMousePosition: QPoint
    AllData: list
    

    def __init__(self):
        super().__init__()
        self.initUI()


    def keyPressEvent(self, event):
        if event.key() == 16777216:#Esc
            #self.FileSaving(self.arr_points, FILE_NAME)
            sys.exit() #Programm Closing
        elif event.key() == 16777249: #Ctrl + R
            stationsName = self.FileReading(FILE_STATIONS_NAME)
            self.FileSaving(self.GetGoogleData(stationsName), FILE_DATA_NAME)



    def GetStationPopularity(self, station_name, trends_object):
        kw_list = station_name
        trends_object.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

        interest = trends_object.interest_over_time()
        return interest.mean()[0]
        #plt.plot(interest[station_name])
        #plt.show()
    


    def mousePressEvent(self, event):
        mousePoint = event.pos()
        self.LastMousePosition = mousePoint
        if event.button() == 2:
            WindowW = self.frameGeometry().width()#   WindowSize
            WindowH = self.frameGeometry().height()#  WindowSize
            imgH = self.overlay.height()# Original Picture Size
            imgW = self.overlay.width()#  Original Picture Size
            
            img = self.overlay.scaledToHeight(self.SelfHeight, Qt.FastTransformation)
            #AdjX = (WindowW-img.width())/2
            ResultX = imgW * (mousePoint.x() - self.DeltaX) / img.width()
            ResultY = imgH / 100 * ((mousePoint.y() - self.DeltaY) / (self.SelfHeight / 100))
            #eraser = 7
            self.painter.drawEllipse(QPoint(ResultX, ResultY), RADIUS, RADIUS)
            #self.painter.eraseRect(QRect(QPoint(ResultX-RADIUS/2-eraser, ResultY-RADIUS/2-eraser), QPoint(ResultX+radius/2+eraser, ResultY+radius/2+eraser)))
            self.arr_points.append((ResultX, ResultY))
            #print([(round(x[0]), round(x[1])) for x in self.arr_points])
            self.update()#Redraw


    def FileSaving(self, arr: list, fileName: str):
        with open(fileName, 'w') as f:
            for item in arr:
                f.write(';'.join(str(x) for x in item) + '\n')
            f.close()



    def FileReading(self, fileName: str):
        with open(fileName, 'r') as f:
            names = f.read().split('\n')
        f.close()
        
        #print(names)
        return [x.split(';') for x in names]


    def GetGoogleData(self, namesSt: list):
        stationSizes = []
        for station in namesSt:
            sz = self.GetStationPopularity([station], self.pytrends)
            if sz>0:
                stationSizes.append([station, sz])
                print(station+': '+str(round(sz, 1)))
            else:
                print(station+' error')

        return stationSizes
        



    def FileDrawing(self, fileName: str): 
        penLine = QPen(QColor(Qt.red))
        penLine.setWidth(10)

   

        #my_file = Path('!StationsLine12.txt')
        #print(my_file.isfile())


        for n in range(14*2):
            penEllipse = QPen(self.Colors[int(n/2)])
            penEllipse.setWidth(5)

            data = []
            path = fileName + str(n/2 + 1) + '.txt'
            my_file = Path(path)
            #print(os.listdir())
           
            if my_file.is_file():
                with open(fileName + str(n/2 + 1) + '.txt', 'r') as f:
                    data = f.read().split('\n')
                    f.close()

                lastX =    None
                lastY =    None
                Point1 =   None
                Point2 =   None
                Startlen = None
                x = 0
                y = 0
                i = 0
                #print(self.NameReading('!Stations.txt'))
                for line in data:
                    x, y = line.split(';')

                    #if lastX is not None or lastY is not None:
                    self.painter.setPen(penLine)
                    #Point1 = QPoint(lastX, lastY)
                    #Point2 = QPoint(float(x), float(y))
                    #self.painter.drawLine(Point1, Point2)

                    self.painter.setPen(penEllipse)
                    penLine = QPen(QColor(Qt.red))
                    self.painter.setBrush(QColor(Qt.white))

                    CircleSize = (RADIUS/100)*float(self.AllData[i][1]) + ADDITIONAL
                    #print(CircleSize)
                    self.painter.drawEllipse(float(x)-CircleSize, float(y)-CircleSize, CircleSize*2, CircleSize*2)
                    i+=1



    def mouseReleaseEvent(self, event):
        self.point = None



    def closeEvent(self, event):
        #self.FileSaving(self.arr_points, FILE_NAME)
        sys.exit() #Programm Closing
      
            

    def initUI(self):
        self.Colors = [
            QColor(228, 37, 24),#1
            QColor(75, 175, 79),#2
            QColor(5, 114, 185),#3
            QColor(36, 188, 239),#4
            QColor(146, 82, 51),#5
            QColor(239, 128, 39),#6
            QColor(148, 63, 144),#7
            QColor(255, 209, 30),#8
            QColor(173, 172, 172),#9
            QColor(185, 206, 31),#10
            QColor(134, 204, 206),#11
            QColor(186, 200, 232),#12
            QColor(68, 143, 201),#13
            QColor(232, 68, 57),#14
        ]

        self.pytrends = TrendReq(hl='en-US', tz=360)

        self.showMaximized()
        #self.showNormal()
        self.setStyleSheet("background-color: white;")



        self.arr_points = []
        self.stationSize = []
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

        self.timer.start(1000/50) #50 кадров в секунду

        self.AllData = self.FileReading(FILE_DATA_NAME)
        self.FileDrawing(FILE_NAME)



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
        #self.LastMousePosition = mousePoint
        self.LastMousePosition = event.pos()
       

    def wheelEvent(self, event):
        #print(str(event.angleDelta()))
        
        self.SelfHeight += (event.angleDelta().y()) / 10
        self.LastAngle = event.angleDelta().y()


    def resizeEvent(self, event):
        self.SelfHeight = self.frameGeometry().height() - 10
        
        if hasattr(self, 'overlay'):
            img = self.overlay.scaledToHeight(self.SelfHeight, 0)
            self.DeltaX = (self.frameGeometry().width() - img.width())/2
            self.DeltaY = 0


if __name__ == '__main__':
   #Window Settings:
   app = QApplication(sys.argv)#Init application
   ex = Example()#Init programm
   sys.exit(app.exec_())#Make Programm End when Window is closed