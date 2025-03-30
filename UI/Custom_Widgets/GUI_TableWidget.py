from PyQt5 import QtWidgets as qtw

class Table_Widget(qtw.QTableWidget):
    def __init__(self, columns, totals):
        super().__init__()
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Tag", "Amount"])
        
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.set_items(columns, totals)
        

    def set_items(self, columns, totals):
        self.setRowCount(len(columns))
        row = 0
        x = 0
        for i in columns:
            self.setItem(row, 0,qtw.QTableWidgetItem(str(i)))
            self.setItem(row, 1, qtw.QTableWidgetItem(str(round(totals[x],2))))
            x +=1
            row +=1
