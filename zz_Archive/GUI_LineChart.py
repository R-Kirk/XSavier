from msilib.schema import tables
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QEvent
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui
from PyQt5 import QtChart
from PyQt5.QtWidgets import QMessageBox, QApplication, QComboBox, QColorDialog
from datetime import date as date, timedelta, datetime
import pandas as pd


#Chart Test https://www.youtube.com/watch?v=eAiKQgLhq_0&t=262s
class Chart(QtChart.QChart):
    def __init__(self, month, data,min_y, max_y, days_between):
        super().__init__()
        self.objectName = "Chart_Monthly"
        self.series = QtChart.QLineSeries()
        self.series.setName(f"{month}")
    
        my_new_list = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
        self.axis_x = QtChart.QDateTimeAxis()
        self.axis_x.setTickCount(15)
        
        print(f"X-tick: {days_between}")
        #axisX->setFormat("dd-MM-yyyy h:mm"); ---- EXAMPLE FOR FORMATS
        self.axis_x.setFormat("MM-dd")
        self.axis_x.setTitleText("Date")
        self.axis_x.setMin(datetime.strptime(str(data[0][0]), '%Y-%m-%d'))
        self.axis_x.setMax(datetime.strptime(str(data[len(data)-1][0]), '%Y-%m-%d'))
        
        self.axis_y = QtChart.QValueAxis()
        self.axis_y.setTickCount(len(data))
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setTitleText("$ Spent")
        self.axis_y.setMax(max_y)
        self.axis_y.setMin(min_y)
 
        for i in data:
            #print(qtc.QDateTime.fromString(str(i[0]), "yyyy-mm-dd").toMSecsSinceEpoch())
            #self.series.append(qtc.QDateTime.fromString(str(i[0]), "yyyy-mm-dd").toMSecsSinceEpoch(), float(i[1]))
            date_item = qtc.QDateTime()
            
            date_item.setDate(qtc.QDate(int(i[0].strftime("%Y")), int(i[0].strftime("%m")), int(i[0].strftime("%d"))))
            #date_item.setTime(qtc.QTime(0,0))
            self.series.append(date_item.toMSecsSinceEpoch(), float(i[1]))
            
        self.addSeries(self.series)  
        self.addAxis(self.axis_x, qtc.Qt.AlignmentFlag.AlignBottom)
        self.addAxis(self.axis_y, qtc.Qt.AlignmentFlag.AlignLeft)
        
        
        self.setAxisX(self.axis_x,self.series)
        self.setAxisY(self.axis_y, self.series)
        #self.series.attachAxis(self.axis_x)
        #self.series.attachAxis(self.axis_y)
       
        
        
       
        
        
        #for x, y in data:
        #   self.series.append(qtc.QPointF(str(x), y))

        
        self.legend().setVisible(True)
        #self.createDefaultAxes()
        #axisX = QtChart.QDateTimeAxis()
        #axisX.setTickCount(len(data))
        
        #self.addAxis(axisX, qtc.AlignBottom)
        


        #self.axisX().setTitleText("Days")
        #self.axisY().setTitleText("$ Spent")
        self.setTitle(f"{month} Spending")
        self.setAnimationOptions(QtChart.QChart.AllAnimations)

        self.chart_view = QtChart.QChartView(self)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)


       



