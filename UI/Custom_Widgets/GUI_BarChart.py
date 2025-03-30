from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui
from PyQt5 import QtChart
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.Qt import Qt


#https://www.youtube.com/watch?v=761X9aVJuOE
class Bar_Chart(QtChart.QChart):
    def __init__(self, columns, totals):
        super().__init__()

        self.set0 = QtChart.QBarSet("Tag 1s")
        
        self.set0.append(totals)
        

        self.bar_series = QtChart.QBarSeries()
        self.bar_series.append(self.set0)


        self.addSeries(self.bar_series)
        self.setTitle('Spending Breakdown')

        self.categories = columns
        self.x_axis = QtChart.QBarCategoryAxis()
        
        self.x_axis.append(self.categories)
        self.x_axis.setLabelsColor(QtGui.QColor(66, 245, 75))
        self.setAxisX(self.x_axis, self.bar_series)
       
        self.y_axis = QtChart.QValueAxis()
        self.y_axis.setLabelsColor(QtGui.QColor(66, 245, 75))
        self.setAxisY(self.y_axis, self.bar_series)
        self.y_axis.setRange(min(totals) - 100,max(totals) + 100)
        
        
        self.legend().setVisible(True)
        self.legend().setAlignment(qtc.Qt.AlignBottom)
        self.legend().setFont(QtGui.QFont("Roboto", pointSize=12, italic=False, weight=10))
        self.axisX().setTitleText("Categories")
        self.axisX().setTitleBrush(QtGui.QColor(252, 3, 19))
        self.axisX().setTitleFont(QtGui.QFont("Arial", pointSize=12, italic=False, weight=10))
        self.setTitleBrush(QtGui.QColor(200,200,200))
        self.axisY().setTitleText("$$$")
        self.axisY().setTitleBrush(QtGui.QColor(252, 3, 19))
        self.axisY().setTitleFont(QtGui.QFont("Arial", pointSize=12, italic=False, weight=10))
        self.setAnimationOptions(QtChart.QChart.SeriesAnimations)
       

        #https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QAbstractBarSeries.html#PySide6.QtCharts.PySide6.QtCharts.QAbstractBarSeries.LabelsPosition
        #https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QAbstractBarSeries.html
        #Webiste above is good documentation on how to set positions and other stuff
        #https://stackoverflow.com/questions/50156082/changing-text-color-for-each-label-in-qcategoryaxis
        #Website above could be useful
        self.bar_series.setLabelsVisible(True)
        self.bar_series.setLabelsPosition(QtChart.QBarSeries.LabelsOutsideEnd)
        self.bar_series.setLabelsAngle(0)
      
       
        
        self.chart_view = QtChart.QChartView(self)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

        self.chart_view.chart().setBackgroundBrush(QtGui.QColor("Black"))
        
        self.chart_view.chart().setFont(QtGui.QFont("Roboto",12,5,False))
        self.chart_view.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
    
        yes = False
        if yes == True:
            y = 100
            x = 100
            for set_index,barset in enumerate(self.bar_series.barSets()):
                for value_index, value in enumerate(barset):
            
                    bar_pos = qtc.QPointF(x, y)
                    label = self.chart_view.chart().scene().addText(str(value))
                    label.setPos(self.chart_view.chart().mapToPosition(bar_pos, self.bar_series) + self.chart_view.pos())#

                    label.setFlag(label.ItemIsMovable)
                    label.setFlag(label.ItemIsSelectable)
                    y+=200
                    x+=100

        yes = False
        if yes == True:
            distance = 10  # Adjust this value based on your needs
            bar_width = self.plotArea().width() / len(self.bar_series.barSets())
            x = 0
            y_adjust = 0
            for barset in self.bar_series.barSets():
                for i in range(len(barset)):
                    # Calculate the position for each label
                    x = bar_width * (i + 0.5) - barset.brush().color().lightnessF() * 20 + x
                    y = self.plotArea().height() - (barset.at(i) / self.axisY().max() * self.plotArea().height()) + y_adjust
                    # Create a label (QGraphicsTextItem)
                    label = QGraphicsTextItem(str(barset.at(i)), parent=self)
                    label.setPos(x, -y - distance)  # Adjust label position
                    label.setDefaultTextColor(barset.brush().color().darker(150))  # Darken the text color
                    self.scene().addItem(label)  # Add label to the chart's scene
                    x+=100
                    y_adjust +=0

           
        

