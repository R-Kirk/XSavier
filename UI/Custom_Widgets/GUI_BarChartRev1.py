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
        # Data and categories
        data = [[10, 20, 15, 25]]  # One bar set with multiple bars
        categories = ["Jan"]

        # Create the bar series
        bar_series = QtChart.QBarSeries()

        # Simulate multiple colors in the first bar set
        colors = [QtGui.QColor("green"), QtGui.QColor("orange"), QtGui.QColor("blue"), QtGui.QColor("red")]

        # Create individual QBarSets for each bar (trick)
        for i, value in enumerate(data[0]):
            bar_set = QtChart.QBarSet(f"Bar {i+1}")
            bar_set.append(value)
            bar_set.setColor(colors[i])
            bar_series.append(bar_set)
        # Enable labels
        bar_series.setLabelsVisible(True)
        bar_series.setLabelsPosition(QtChart.QBarSeries.LabelsOutsideEnd)

        # Add the series to the chart
        self.addSeries(bar_series)

        # Customize the chart
        self.addSeries(bar_series)
        self.setTitle("Custom Bar Labels at Bottom")
        self.createDefaultAxes()

        # Customize the axes
        x_axis = QtChart.QBarCategoryAxis()
        custom_labels = ["Bar 1"]
        x_axis.append(custom_labels)
        self.setAxisX(x_axis, bar_series)

        y_axis = QtChart.QValueAxis()
        self.setAxisY(y_axis, bar_series)

        # Display the chart
        self.chart_view = QtChart.QChartView(self)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

        # Corrected custom label positioning
        x_spacing = 0
        y_spacing = -200
        for i, label_text in enumerate(custom_labels):
            # Use the correct Y-position for the labels
            bar_pos = self.mapToPosition(qtc.QPointF(i + x_spacing, y_axis.min()), bar_series)
            y_pos = ((self.chart_view.size().height()))*(.90)
            width = ((self.chart_view.size().width())/4)
            x_spacing += width

            bar_pos = self.chart_view.mapTo(self.chart_view, qtc.QPoint(i,int(y_axis.min())))
            # Add label at the corrected position
            label = self.scene().addText(label_text)
            label.setDefaultTextColor(QtGui.QColor("black"))
            label.setFont(QtGui.QFont("Arial", 10))
            
            # Adjust the label's position to be centered below each bar
            print(f"({bar_pos.x()}, {bar_pos.y()})")
            label.setPos(
                x_spacing - label.boundingRect().width() / 2, 
                y_pos + label.boundingRect().height() + 5
    )

           
        

