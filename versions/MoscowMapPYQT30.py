import sys
import os
import pandas as pd
import numpy as np
from time import time, sleep
from pathlib import Path
from random import random, randrange
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QDesktopWidget, 
                                QLabel, QFrame)
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QPolygonF,
                                QPixmap, QPalette, QImage)
from PyQt5.QtCore import QCoreApplication, Qt, QPoint, QPointF, QRect, QTimer
from math import sqrt, sin, cos, pi, radians, log

RADIUS        = 25
ADDITIONAL    = 10

FILE_NAME     = '!StationsLine'
FILE_STATIONS_NAME = '!Stations.txt'
FILE_DATA_NAME = '!StationsNew.csv'
FILE_BACKGROUND = 'Moscow Metro Map Stations Popularity\\MainMap.bmp'
IS_FULL_LOAD    = True
IS_ANIMATE      = True
UPDATE_SPEED    = 1000/30 #30 кадров  сек


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
    AllData: pd.DataFrame
    toolTipWidget: QLabel
    pytrends: TrendReq
    

    def __init__(self):
        super().__init__()
        self.initUI()


    def keyPressEvent(self, event):
        if event.key() == 16777216:#Esc
            #self.FileSaving(self.arr_points, FILE_NAME)
            sys.exit() #Programm Closing
        elif event.key() == 16777249: #Ctrl
            self.UpdateGoogleData()
            #self.FileSaving(self.GetGoogleData(stationsName), FILE_DATA_NAME)


    def UpdateGoogleData(self):
        self.pytrends = TrendReq(hl='ru-RU', tz=360)
        for i, row in self.AllData.iterrows():
            if not row['Popul']>0 or IS_FULL_LOAD:
                stationPopul = self.GetStationPopularity(row['Name'], self.pytrends)
                print(row['Name'] + ' ' + str(round(stationPopul,2)))
                self.AllData.at[i,'Popul'] = stationPopul
            else:
                print(row['Name'] + ' ' + str(round(row['Popul'],2))+' old')
            
            # self.FileDrawing(False)
            QApplication.processEvents()
            # if i>10:
            #      break
            if i % 10 == 0:
                self.AllData.to_csv(FILE_DATA_NAME, index = False, sep=',', encoding='utf-8-sig')
        print('All Loaded!')



    def GetStationPopularity(self, station_name, trends_object):
        # station_name = 'Тульская'
        # timeframe='today 5-y'
        suggestions_dict = self.pytrends.suggestions(keyword=station_name+' Станция метрополитена')
        # kw_list = station_name 'type:Moscow Metro']
        suggestions = [x for x in suggestions_dict if x['title']==station_name]
        if len(suggestions)>0:
            kw_list =[suggestions[0]['mid']]
            print('          ' + suggestions[0]['type'])
        else:
            return 0
            # kw_list = [station_name]

        trends_object.build_payload(kw_list, cat=0, geo='RU', timeframe='2017-01-01 2018-11-01', gprop='')

        interest = trends_object.interest_over_time()
        mean = interest.mean()
        if len(list(mean))>0:
            return mean[0]
        else:
            return 0
        #plt.plot(interest[station_name])
        #plt.show()
    



    def mousePressEvent(self, event):
        mousePoint = event.pos()
        self.LastMousePosition = mousePoint

        if event.button() == 1:
            # self.painter.setFont(QFont('Arial', 111)) 
            # self.painter.drawText(QPoint(200,200), 'HELLO')
            WindowW = self.frameGeometry().width()#   WindowSize
            WindowH = self.frameGeometry().height()#  WindowSize
            imgH = self.overlay.height()# Original Picture Size
            imgW = self.overlay.width()#  Original Picture Size
            
            img = self.overlay.scaledToHeight(self.SelfHeight, Qt.FastTransformation)
            #AdjX = (WindowW-img.width())/2
            ResultX = imgW * (mousePoint.x() - self.DeltaX) / img.width()
            ResultY = imgH / 100 * ((mousePoint.y() - self.DeltaY) / (self.SelfHeight / 100))
            #eraser = 7
            #self.painter.drawEllipse(QPoint(ResultX, ResultY), RADIUS, RADIUS)

            for i, row in self.AllData.iterrows():            
                if  ResultX >= row['X'] - (row['Popul'] + ADDITIONAL) /2 and \
                    ResultX <= row['X'] + (row['Popul'] + ADDITIONAL) /2 and \
                    ResultY >= row['Y'] - (row['Popul'] + ADDITIONAL) /2 and \
                    ResultY <= row['Y'] + (row['Popul'] + ADDITIONAL) /2:
                    text = row['Name']+', '+str(round(row['Popul'],1)) + '%'

                    self.toolTipWidget.setText(text)
                    self.toolTipWidget.move(event.pos())
                    self.toolTipWidget.adjustSize()
                    self.toolTipWidget.show()

            #self.painter.eraseRect(QRect(QPoint(ResultX-RADIUS/2-eraser, ResultY-RADIUS/2-eraser), QPoint(ResultX+radius/2+eraser, ResultY+radius/2+eraser)))
            self.arr_points.append((ResultX, ResultY))
            #print([(round(x[0]), round(x[1])) for x in self.arr_points])
            self.update()#Redraw


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

    def mouseReleaseEvent(self, event):
        self.point = None
        self.toolTipWidget.hide()

    '''
    def FileSaving(self, arr: list, fileName: str):
        with open(fileName, 'w') as f:
            for item in arr:
                f.write(','.join(str(x) for x in item) + '\n')
            f.close()



    def FileReading(self, fileName: str):
        with open(fileName, 'r') as f:
            names = f.read().split('\n')
        f.close()
        
        #print(names)
        return [x.split(',') for x in names]
    

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
    '''    



    def FileDrawing(self, animate): 
        if not animate:
            self.timer.stop()      
        penLine = QPen(QColor(Qt.red))
        penLine.setWidth(10)

        for i, row in self.AllData.iterrows():
            penEllipse = QPen(self.Colors[int(row['Line'].replace('A',''))-1])
            penEllipse.setWidth(5)


            x = row['X']
            y = row['Y']
            # self.AllData[allDataI].append(x)
            #self.AllData[allDataI].append(y)
            #if lastX is not None or lastY is not None:
            self.painter.setPen(penLine)
            #Point1 = QPoint(lastX, lastY)
            #Point2 = QPoint(float(x), float(y))
            #self.painter.drawLine(Point1, Point2)

            self.painter.setPen(penEllipse)
            penLine = QPen(QColor(Qt.red))
            self.painter.setBrush(QColor(Qt.white))

            if row['Popul']>0:
                CircleSize = (RADIUS/100) * row['Popul'] + ADDITIONAL
            else:
                CircleSize = 1
            #print(CircleSize)
            #if n == 8 and i>=11 and i<=12: 
            self.painter.drawEllipse(float(x)-CircleSize, float(y)-CircleSize, CircleSize*2, CircleSize*2)
            QApplication.processEvents()
            #sleep(1)
        self.timer.start(UPDATE_SPEED)
        self.overlay.save('hehe.jpg',format = 'jpeg')




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

        
        self.showMaximized()
        #self.showNormal()
        self.setStyleSheet("background-color: white;")
        
        self.toolTipWidget = QLabel()
        self.toolTipWidget.setStyleSheet("QLabel {"
                                                "border-style: solid;"
                                                "border-width: 1px;"
                                                "border-color: grey; "
                                                "border-radius: 3px;"
                                                "padding: 5px 5px 5px 5px;"
                                                "background-color: rgb(255,255,225);"
                                                "}")

        self.toolTipWidget.setWindowFlags(Qt.ToolTip)
        self.toolTipWidget.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.toolTipWidget.hide()
        

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
        #self.overlay.load('Moscow Metro Map Stations Popularity\\MainMap.bmp')
        self.overlay.load(FILE_BACKGROUND)
  
 
        
        pen = QPen(QColor(Qt.red))
        pen.setWidth(5)
        self.painter = QPainter(self.overlay)
        self.painter.setPen(pen) 
        self.painter.Antialiasing  = False

        self.timer.start(UPDATE_SPEED) 

        #self.AllData = self.FileReading(FILE_DATA_NAME)
        self.AllData = pd.read_csv(FILE_DATA_NAME,',', encoding='utf-8-sig')
        # self.AllData = [x for x in self.AllData.iterrows() if x['Line']='8A']
        #self.arr_points = self.FileReading()
        # self.FileDrawing()



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
   ex.FileDrawing(IS_ANIMATE)
   sys.exit(app.exec_())#Make Programm End when Window is 