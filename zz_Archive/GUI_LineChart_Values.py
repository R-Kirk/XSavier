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
    def __init__(self, month, data, min_x, max_x, min_y, max_y):
        super().__init__()
        self.objectName = "Chart_Monthly"
        self.series = QtChart.QLineSeries()
        self.series.setName(f"{month}")
    
        
        for x, y in data:
            self.series.append(qtc.QPointF(x, y))

        self.addSeries(self.series)
        self.legend().setVisible(True)
        self.createDefaultAxes()
        self.axisX().setTitleText("Days")
        self.axisX().setMin(min_x)
        self.axisX().setMax(max_x)
        
        self.axisY().setTitleText(" Monthly Net Profit")
        print(f"Min Y: {min_y}")
        self.axisY().setMin(min_y)
        self.axisY().setMax(max_y)
        self.setTitle(f"{month} Spending")
        self.setAnimationOptions(QtChart.QChart.AllAnimations)
        self.chart_view = QtChart.QChartView(self)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        


       



