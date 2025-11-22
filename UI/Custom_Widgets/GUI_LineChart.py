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
# Another Example - https://www.youtube.com/watch?v=lUEepHsNPpE&t=1819s
class Chart(QtChart.QChart):
    def __init__(self, month, data, min_x, max_x, min_y, max_y):
        super().__init__()
        self.objectName = "Chart_Monthly"
        self.series = QtChart.QLineSeries()
        self.series.setName(f"{month}")

        ##### - SERIES 1 - Get points for Zero Profit Line
        for x, y in data:
            self.series.append(qtc.QPointF(x, y))
        self.addSeries(self.series)
        self.series.setPointsVisible(True)
        self.series.setPointLabelsFormat("@yPoint")
        self.series.setPointLabelsVisible(True)
        self.series.setPointLabelsColor(QtGui.QColor(235, 64, 52))
        
       
        ##### - SERIES 2 - Get points for Zero Profit Line
        dummy_list = []
        for x in range(1,max_x+1):
            point = (x, 0)
            dummy_list.append(point)
        self.series_2 = QtChart.QLineSeries()
        self.series_2.setName("$0 Profit Line")

        for x, y in dummy_list:
            self.series_2.append(qtc.QPointF(x, y))

        self.addSeries(self.series_2)
        #Color Grid Lines
        pen = QtGui.QPen(QtGui.QColor(66, 62, 62))
        pen.setWidth(1) # Adjust the width as needed
        
       
        #Set X Axis
        self.axis_x = QtChart.QValueAxis()
        self.axis_x.setTickCount(max_x)
        self.axis_x.setMin(min_x)
        self.axis_x.setMax(max_x)
        
        self.axis_x.setLabelFormat("%i")
        self.axis_x.setTitleText("Day")
        self.axis_x.setLabelsColor(QtGui.QColor(66, 245, 75))
        

        #Set Y Axis
        self.axis_y = QtChart.QValueAxis()
        self.axis_y.setTickCount(len(data))
        self.axis_y.setLabelFormat("$ %i")
        self.axis_y.setTitleText("$ Spent")
        self.axis_x.setTitleBrush(QtGui.QColor(252, 3, 19))
        self.axis_y.setMin(min_y)
        self.axis_y.setMax(max_y+500)
        self.axis_y.setTickCount(5)
        self.axis_y.setLabelsColor(QtGui.QColor(66, 245, 75))
        self.axis_y.setTitleBrush(QtGui.QColor(252, 3, 19))

        self.axis_x.setGridLinePen(pen)
        self.axis_y.setGridLinePen(pen)

        self.setAxisX(self.axis_x, self.series)
        self.setAxisY(self.axis_y, self.series)
        self.setAxisX(self.axis_x, self.series_2)
        self.setAxisY(self.axis_y, self.series_2)

        self.legend().setVisible(True)
        self.legend().setFont(QtGui.QFont("Roboto", pointSize=12, italic=False, weight=10))
        self.legend().setColor(QtGui.QColor(200,200,200))
        self.setTitle(f"{month} Spending")
        self.setTitleBrush(QtGui.QColor(200,200,200))
        self.setAnimationOptions(QtChart.QChart.AllAnimations)
        self.chart_view = QtChart.QChartView(self)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.chart_view.chart().setBackgroundBrush(QtGui.QColor("Black"))
        #self.chart_view.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        #self.chart_view.adjustSize()
        
        


       



