##########################################################################################

##### --- LIBRARY IMPORTS AND SETUP CODE BELOW --- #####.........................................

##########################################################################################

##### --- External Libraries --- #####...........................................................
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMessageBox,  QComboBox, QColorDialog, QDialog
from datetime import date as date
from datetime import datetime
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
)

##### --- #####

##### --- Import GUI Files to use --- #####.......................................................
from UI.GUI_Files.GUI_MainWindow import Ui_MainWindow
from UI.GUI_Files.GUI_Dashboard2 import Ui_Form as Ui_Dashboard
from UI.GUI_Files.GUI_Accounts import Ui_Form as Ui_Accounts
from UI.GUI_Files.GUI_NewAccount import Ui_Form as Ui_NewAccount
from UI.GUI_Files.GUI_Accounts_Config import Ui_Form as Ui_AccountsConfig
from UI.GUI_Files.GUI_Import_Manager import Ui_Form as Ui_ImportManager
from UI.GUI_Files.GUI_TagManager3 import Ui_Form as Ui_TagManager
from UI.GUI_Files.GUI_Settings import Ui_Form as Ui_Settings
from UI.GUI_Files.GUI_Tags import Ui_Form as UI_Tags
from UI.GUI_Files.GUI_AddTag1 import Ui_Form as UI_AddTag1
from UI.GUI_Files.GUI_AddTag2 import Ui_Form as UI_AddTag2
from UI.GUI_Files.GUI_EditTag1 import Ui_Form as UI_EditTag1
from UI.GUI_Files.GUI_MoveFiles import Ui_Form as UI_MoveFiles
from UI.GUI_Files.GUI_Developer_Details import Ui_Form as UI_DeveloperDetails
from UI.GUI_Files.GUI_Application_Settings import Ui_Form as UI_ApplicationSettings
from UI.GUI_Files.GUI_KeywordTagging import Ui_Form as UI_KeywordTagging
from UI.GUI_Files.GUI_AddKeywordRule import Ui_Form as UI_AddKeywordRule
from UI.GUI_Files.GUI_EditKeywordRule import Ui_Form as UI_EditKeywordRule
from UI.GUI_Files.GUI_Tags_Convert import Ui_Form as UI_TagsConvert
from UI.GUI_Files.GUI_Analytics import Ui_Form as UI_Analytics
from UI.GUI_Files.GUI_DeleteTag1 import Ui_Form as UI_DeleteTag1
from UI.GUI_Files.GUI_Bills import Ui_Form as UI_Bills
from UI.GUI_Files.GUI_BillsAdd import Ui_Form as UI_BillsAdd
##### --- #####

##### --- CUSTOM WIDGETS --- #####...............................................................
from UI.Custom_Widgets.GUI_LineChart import Chart as LineChart
from UI.Custom_Widgets.GUI_BarChartRev1 import Bar_Chart
from UI.Custom_Widgets.GUI_YearlyLineChart import Chart as YearlyLineChart
##### --- ######

##### --- Import Personal Libraries --- #####....................................................
from customs.db_ import database 
from customs.File_Manager import File_Manager
from customs import CSV_Manager
from customs import jarvis
from customs.StartUp import StartUp
##### --- #####
##### --- Getting Todays Date --- #####..........................................................
today = date.today()
d = today.strftime("%d")
m = today.strftime("%m")
y = today.strftime("%Y")
month = today.strftime("%B")
##### --- #####

##########################################################################################

###   MAIN CODE BELOW   ###...............................................................

##########################################################################################
class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        self.main_window.statusbar.setStyleSheet("background-color: #b4b4b4; font-size: 18pt; font-family: Courier; color: black")
        self.main_window.statusbar.showMessage(f" Version {setting_2}")
        self.setWindowTitle("XSavier")
        self.setWindowIcon(QtGui.QIcon(':/Other_Icons/logo.ico'))

        #Tool Bar Actions
        self.main_window.actionBackup_Database.triggered.connect(self.backup_database)
        self.main_window.actionImport_Files.triggered.connect(show_MoveFiles)
        self.main_window.actionPush_Database_Update.triggered.connect(self.update_db_tables)

        #Define Shortcuts
        #......Home
        shortcut = QtGui.QKeySequence(qtc.Qt.CTRL + qtc.Qt.Key_H)
        self.shortcut = qtw.QShortcut(shortcut, self)
        self.shortcut.activated.connect(self.shortcut_show_dashboard)

        #......Settings
        shortcut = QtGui.QKeySequence(qtc.Qt.CTRL + qtc.Qt.Key_S)
        self.shortcut = qtw.QShortcut(shortcut, self)
        self.shortcut.activated.connect(show_Settings)

        #Disable Tool Menu due to not programmed yet
        self.main_window.actionRestore_Database.setEnabled(False)
        

        #self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.setWindowFlag(qtc.Qt.WindowSystemMenuHint)
       
    def backup_database(self):
        backup_status = fm.backup_database()
        if backup_status:
            status = AlertMessage(self,'Backup Database Status', 'Backup completed successfully...', '', '')
            status.exec_()
        else:
            status = AlertMessage(self,'Backup Database Status', 'Backup failed...', '', '')
            status.exec_()
    
    def update_db_tables(self):
        db.create_tables()
        settings = db.get_application_settings()

        #Update Application Version if needed
        setting_2 = settings[2]
        self.main_window.statusbar.showMessage(f" Version {setting_2}")
        
        status = AlertMessage(self,'DB Update Status', 'Pushed Table Update Only...', '', '')
        status.exec_()
        
    def shortcut_show_dashboard(self):
        if self.centralWidget().objectName != "Dashboard_Widget":
            widget = Dashboard_Widget(int(m))
            self.setCentralWidget(widget)
    
class Dashboard_Widget(qtw.QWidget):
    def __init__(self, month_selection, year_selection=y, Toggled=True):
        super().__init__()
        self.dashboard = Ui_Dashboard()
        self.dashboard.setupUi(self)
        self.month_selection = month_selection
        self.year_selection = year_selection

        self.dashboard.comboBox_Month.setStyleSheet("font: 16pt ""Arial Rounded MT Bold"";")
        self.dashboard.comboBox_Year.setStyleSheet("font: 16pt ""Arial Rounded MT Bold"";")
        self.objectName = "Dashboard_Widget"

        ##### --- Buttons --- #####
        self.dashboard.pushButton_Accounts.clicked.connect(show_accounts)
        self.dashboard.pushButton_ImportAccountData.clicked.connect(show_ImportManager)
        self.dashboard.pushButton_TagManager.clicked.connect(show_TagManager)
        self.dashboard.pushButton_Settings.clicked.connect(show_Settings)
        self.dashboard.commandLinkButton_Yearly.toggled.connect(self.update_daashboard_yearly)
        self.dashboard.commandLinkButton_HamBurger.setChecked(Toggled)
        self.dashboard.commandLinkButton_TagsbyYear.toggled.connect(self.update_dashboard_yearly_tags)
        self.dashboard.pushButton_Analytics.clicked.connect(lambda: show_Analytics(int(y)))
        self.dashboard.pushButton_Bills.clicked.connect(show_Bills)
        ##### --- #####

        ##### --- disable buttons if Accounts aren't created yet --- #####
        if db.accounts == [["NA", "NA", "NA","NA", "NA", "NA","NA", "NA", "NA"]]:
            self.dashboard.pushButton_ImportAccountData.setEnabled(False)
            self.dashboard.pushButton_TagManager.setEnabled(False)
            window.main_window.actionImport_Files.setEnabled(False)
            
            self.dashboard.pushButton_ImportAccountData.setStyleSheet('QPushButton {background-color: #878273; color: white;}')
            self.dashboard.pushButton_TagManager.setStyleSheet('QPushButton {background-color: #878273; color: white;}')
        ##### --- #####

        ##### --- Set Month Combo Box --- #####
        months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", 'October', "November", "December"]
        self.dashboard.comboBox_Month.addItems(months_list)
        self.dashboard.comboBox_Month.setCurrentIndex(self.month_selection-1)
        self.dashboard.comboBox_Month.currentIndexChanged.connect(lambda: show_dashboard(self.dashboard.comboBox_Month.currentIndex() + 1, self.dashboard.comboBox_Year.currentText(), self.dashboard.commandLinkButton_HamBurger.isChecked()))
        
        self.update_dashboard()
        ##### --- #####

        ##### --- Set Year Combo Box --- #####
        years = db.get_expense_years()
        for year in years:
            self.dashboard.comboBox_Year.addItem(year)
        self.dashboard.comboBox_Year.setCurrentText(str(year_selection))
        self.dashboard.comboBox_Year.currentIndexChanged.connect(lambda: show_dashboard(self.dashboard.comboBox_Month.currentIndex() + 1, self.dashboard.comboBox_Year.currentText(), self.dashboard.commandLinkButton_HamBurger.isChecked()))
        ##### --- #####
        
    def update_dashboard(self):
        ##### --- Define Dashboard Charts --- #####
        self.month_selection = self.dashboard.comboBox_Month.currentIndex() + 1
        self.month_text = self.dashboard.comboBox_Month.currentText()

        expenses = db.get_expenses("Month-Year",str(int(self.month_selection)), str(self.year_selection), 0, 0)
        amount = 0
        count = 1
        if expenses != False:
            for expense in expenses: 
                amount += float(expense[20])
                if expense[1] == "Test Account 2":
                    print(f"{count}   {expense[19]}")
                    count += 1

        tag_data = db.get_tag1s()
       
       ##### --- Bar Chart - Line Series - Monthly Cash Flow Calculation --- #####
        if expenses != False:
            ##### --- Get Line Series Data --- #####
            series_data, min_x, max_x, min_y, max_y = jarvis.get_line_series(expenses, tag_data, str(int(self.month_selection)), str(int(y)))
            ##### --- #####

            ##### --- Get profit for PROFIT LABEL --- #####
            current_profit = float(series_data[len(series_data)-1][1])
            self.dashboard.label_CurrentProfit.setText(f"Monthly Profit: $ {round(current_profit,2):,}")
            ##### --- #####

            ##### --- Color Label Red for negative and green for positive --- #####
            if current_profit < 0:
                self.dashboard.label_CurrentProfit.setStyleSheet(f"color: #de5b5b")
            else:
                self.dashboard.label_CurrentProfit.setStyleSheet(f"color: #5c9165")
            ##### --- #####
            
            ##### --- Add Line Chart to Dashboard --- #####
            self.chart = LineChart(self.dashboard.comboBox_Month.currentText(), series_data, min_x, max_x, min_y, max_y)
            self.dashboard.gridLayout.addWidget(self.chart.chart_view, 0,0,1,1)
            ##### --- ######
        
            ##### --- BAR CHART --- #####
            setting_bar_chart_zeros = db.get_application_settings()[3]
            show_zeros = True
            if setting_bar_chart_zeros == "True":
                show_zeros = True
            else:
                show_zeros = False
                    
            ##### --- Remove Overridden Epenses --- #####
            expenses_cleaned = jarvis.remove_overridden_expenses(expenses, self.month_selection, self.year_selection)
            
            columns, colors, values = jarvis.get_bar_series(expenses_cleaned, tag_data, show_zeros)
            #--Old Bar Chart Data -- #
            #self.BarChart = Bar_Chart(columns, values)
            #self.dashboard.gridLayout.addWidget(self.BarChart.chart_view, 1,0,1,1)
            #self.dashboard.label_CurrentProfit.show()
            #-- END OF OLD BAR CHART CODE -- #

            self.Bar_Chart = Matplotlib_Widget(self, columns, colors, values, f"{self.month_text} Tag Summary")
            self.dashboard.gridLayout.addWidget(self.Bar_Chart, 1,0,1,1)

            ##### --- #####
            
        else:
            ##### --- Not sure why this code is here or if it ever runs, other than when there are no expenses --- ######
            try:
                self.dashboard.gridLayout.removeWidget(self.chart)
                self.chart.deleteLater()
                del self.chart
                self.dashboard.gridLayout.removeWidget(self.BarChart)
                self.BarChart.deleteLater()
                del self.BarChart
            except:
                pass
            self.dashboard.label_CurrentProfit.hide()
            ##### --- #####

    def update_daashboard_yearly(self):
        if self.dashboard.commandLinkButton_Yearly.isChecked():
            self.dashboard.commandLinkButton_TagsbyYear.setChecked(False)
            tag_data = db.get_tag1s()

            ##### --- Year-To-Date Cash Flow --- #####
            expenses_year_to_date = db.get_expenses_year_to_date(self.year_selection)
            if expenses_year_to_date != False:
                yearly_cashflow, min_x, max_x, min_y, max_y = jarvis.get_year_cashflow(expenses_year_to_date, int(y), tag_data)
                self.YearlyLineChart = YearlyLineChart(yearly_cashflow, min_x, max_x, min_y, max_y)
                self.dashboard.gridLayout.addWidget(self.YearlyLineChart.chart_view, 0,0,2,2)
                
                ##### --- Set Label to show yearly cashflow --- #####
                current_profit = yearly_cashflow[len(yearly_cashflow)-1]
                self.dashboard.label_CurrentProfit.setText(f"Yearly Profit: $ {round(current_profit[1],2):,}")
                if current_profit[1] < 0:
                    self.dashboard.label_CurrentProfit.setStyleSheet(f"color: #de5b5b")
                else:
                    self.dashboard.label_CurrentProfit.setStyleSheet(f"color: #5c9165")
                self.dashboard.label_CurrentProfit.show()
                ##### --- #####
        else:
            if self.dashboard.commandLinkButton_TagsbyYear.isChecked() != True:
                show_dashboard(self.dashboard.comboBox_Month.currentIndex()+1, self.dashboard.comboBox_Year.currentText(), self.dashboard.commandLinkButton_HamBurger.isChecked())

    def update_dashboard_yearly_tags(self):
        if self.dashboard.commandLinkButton_TagsbyYear.isChecked():
            self.dashboard.commandLinkButton_Yearly.setChecked(False)
            tag_data = db.get_tag1s()

            ##### --- Year-To-Date Tags Summary --- #####
            expenses_year_to_date = db.get_expenses_year_to_date(self.year_selection)
            if expenses_year_to_date != False:
                setting_bar_chart_zeros = db.get_application_settings()[3]
                show_zeros = True
                if setting_bar_chart_zeros == "True":
                    show_zeros = True
                else:
                    show_zeros = False
                columns, colors, values = jarvis.get_bar_series(expenses_year_to_date, tag_data, show_zeros)
                #positive_columns, positive_totals, negative_columns, negative_totals = jarvis.get_bar_series_1(expenses_year_to_date, tag_data)
                #self.YearlyTagBarChart = Bar_Chart(columns, totals)
                #self.YearlyTagBarChart = Bar_Chart(positive_columns, positive_totals, negative_columns, negative_totals)
                #self.dashboard.gridLayout.addWidget(self.YearlyTagBarChart.chart_view, 0,0,2,2)

                self.bar_widget = Matplotlib_Widget(self, columns, colors, values, "Yearly Tag 1 Summary")
                self.dashboard.gridLayout.addWidget(self.bar_widget,0,0,2,2)
                
            ##### --- #####
        else:
            if self.dashboard.commandLinkButton_Yearly.isChecked() != True:
                show_dashboard(self.dashboard.comboBox_Month.currentIndex()+1, self.dashboard.commandLinkButton_HamBurger.isChecked())
            
class Accounts_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = Ui_Accounts()
        self.accounts.setupUi(self)

        ##### --- Buttons --- #####
        self.accounts.pushButton_Home.clicked.connect(lambda: show_dashboard("Auto"))
        self.accounts.pushButton_NewAccount.clicked.connect(show_NewAccount)
        self.accounts.pushButton_ConfigAccount.clicked.connect(show_AccountsConfig)
        ##### --- #####
        
        ##### --- Edit QTableWidget --- ##### 
        self.accounts.tableWidget_Accounts.setColumnCount(10)
        self.accounts.tableWidget_Accounts.setHorizontalHeaderLabels(["ID", "Account Name", "Account Type", "Transaction Date Column" ,"Posted Date Col", "Desc. Col", "Amt1 Col", "Sign1 Col", "Amt2 Col", "Sign2 Col"])
        ##### --- #####
        

        ##### --- Set items in table and color the rows red if the account isnt configured --- #####
        row_count = len(db.accounts)
        self.accounts.tableWidget_Accounts.setRowCount(row_count)
        row = 0
        col = 0
        for x in db.accounts:
            for y in x:
                self.accounts.tableWidget_Accounts.setItem(row, col, qtw.QTableWidgetItem(str(y)))
                col += 1
            ##### --- Color Cells Red if the acocunt hasnt been configured yet --- #####
            if x[0] != "NA" and x[7] == "Config":  #Will be NA if the user has no accounts          
                for z in range(10):
                    self.accounts.tableWidget_Accounts.item(row,z).setBackground(QtGui.QColor(242, 100, 90))                        
            col = 0
            row += 1
        ##### --- #####

class Bills_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bills = UI_Bills()
        self.bills.setupUi(self)

        ##### --- Buttons --- #####
        self.bills.pushButton_Home.clicked.connect(lambda: show_dashboard("Auto"))
        self.bills.pushButton_NewBill.clicked.connect(show_BillsAdd)
        ##### --- #####
        
        ##### --- Edit QTableWidget --- ##### 
        self.bills.tableWidget_Bills.setColumnCount(10)
        self.bills.tableWidget_Bills.setHorizontalHeaderLabels(["ID", "Name", "Description", "Pay Freq." ,"Amount", "Yearly Amt", "Monthly Amt", "Weekly Amt", "Account", "Enabled"])
        ##### --- #####


        ##### --- Get Bills from DB --- #####
        bills = db.get_bills() 
        
        
        ##### --- #####


        ##### --- Set items in table --- #####
        if bills != False:
            enabled_list = []
            disabled_list = []
            for bill in bills:
                if bill[9] == "Enabled":
                    enabled_list.append(bill)
                else:
                    disabled_list.append(bill)
            enabled_list = sorted(enabled_list, key=lambda x: x[4], reverse = True)
            disabled_list = sorted(disabled_list, key=lambda x: x[4], reverse = True)
            bills = sorted(bills, key=lambda x: x[8], reverse=True)

            row_count = len(bills)
            self.bills.tableWidget_Bills.setRowCount(row_count)
            row = 0
            col = 0
            for x in enabled_list:
                for y in x:
                    if col == 9:
                        combo = ComboBillsEnable(self, f"{row}_{col}", y)
                        self.bills.tableWidget_Bills.setCellWidget(row, col, combo)
                    
                    self.bills.tableWidget_Bills.setItem(row, col, qtw.QTableWidgetItem(str(y)))
                    
                    col += 1                  
                col = 0
                row += 1
            for x in disabled_list:
                for y in x:
                    if col == 9:
                        combo = ComboBillsEnable(self, f"{row}_{col}", y)
                        self.bills.tableWidget_Bills.setCellWidget(row, col, combo)
                    
                    self.bills.tableWidget_Bills.setItem(row, col, qtw.QTableWidgetItem(str(y)))
                    self.bills.tableWidget_Bills.item(int(row), int(col)).setBackground(QtGui.QColor("#9ba89f"))
                    col += 1                  
                col = 0
                row += 1
        ##### --- #####

        ##### --- Set totals bar --- #####

        if bills != False:
            enabled_count = 0
            yearly_total = 0
            monthly_total = 0
            weekly_total = 0
            disabled_count = 0
            disabled_yearly = 0
            disabled_monthly = 0
            disabled_weekly = 0

            ## Column Designations ##
            yearly_col = 5
            monthly_col = 6
            weekly_col = 7
            enabled_col = 9
            for bill in bills:
                
                if bill[enabled_col] == "Enabled":
                    enabled_count += 1
                    yearly_total += float(bill[yearly_col])
                    monthly_total += float(bill[monthly_col])
                    weekly_total += float(bill[weekly_col])
                else:
                    disabled_count += 1
                    disabled_yearly += float(bill[yearly_col])
                    disabled_monthly += float(bill[monthly_col])
                    disabled_weekly += float(bill[weekly_col])
            

            self.bills.label_enabled_count_2.setText(f"{round(enabled_count,2):,}")
            self.bills.label_yearly_total_2.setText(f"$ {round(yearly_total,2):,}")
            self.bills.label_monthly_total_2.setText(f"$ {round(monthly_total,2):,}")
            self.bills.label_weekly_total_2.setText(f"$ {round(weekly_total,2):,}")
            self.bills.label_disabled_count_2.setText(f"{round(disabled_count,2):,}")
            self.bills.label_disabled_yearly_2.setText(f"$ {round(disabled_yearly,2):,}")
            self.bills.label_disabled_monthly_2.setText(f"$ {round(disabled_monthly,2):,}")
            self.bills.label_disabled_weekly_2.setText(f"$ {round(disabled_weekly,2):,}")

        
            ### --- Fit to column
            self.bills.tableWidget_Bills.resizeColumnsToContents() 
            for row in range(len(bills)):
                
                for col in range(len(bills[0])):
                    if col != 8:
                        item = self.bills.tableWidget_Bills.item(row, col)
                        item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
                    



        ##### --- #####
        
class BillsAdd_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bills_add = UI_BillsAdd()
        self.bills_add.setupUi(self)

        ##### --- Buttons --- #####
        self.bills_add.pushButton_Cancel.clicked.connect(show_Bills)
        self.bills_add.pushButton_Save.clicked.connect(self.save_bill)
        ##### --- #####

        ##### --- Set Combo Box --- #####
        items = ["Monthly", "Yearly", "Weekly"]
        self.bills_add.comboBox_PayFreq.addItems(items)
        self.bills_add.comboBox_PayFreq.setCurrentIndex(0)
        ##### --- #####

        ##### --- Set Accounts --- #####
        accounts = db.accounts
        self.bills_add.comboBox_Account.addItem("--")
        for account in accounts:
            self.bills_add.comboBox_Account.addItem(account[1])

        ##### --- #####


        

    def save_bill(self):
        name = self.bills_add.lineEdit_BillName.text()
        description = self.bills_add.lineEdit_Description.text()
        pay_freq = self.bills_add.comboBox_PayFreq.currentText()
        amount = float(self.bills_add.lineEdit_Amount.text())
        account = self.bills_add.comboBox_Account.currentText()
        enabled = "Enabled"

        if pay_freq == "Yearly":
            yearly = round((amount),2)
            monthly = round((amount/12),2)
            weekly = round((amount / 52),2)

        elif pay_freq == "Monthly":
            yearly = round((amount * 12),2)
            monthly = round((amount),2)
            weekly = round(((amount * 12)/52),2)
        else:
            yearly = round((amount * 52),2)
            monthly = round(((amount * 52)/12),2)
            weekly = round((amount),2)
        
        if db.add_bill(name, description, pay_freq, amount, yearly, monthly, weekly, account, enabled) == True:
            show_Bills()

class NewAccount_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newaccount = Ui_NewAccount()
        self.newaccount.setupUi(self)
        #Buttons
        self.newaccount.pushButton_Cancel.clicked.connect(show_accounts)
        self.newaccount.pushButton_Submit.clicked.connect(self.submit)

    def submit(self):
        account_name = self.newaccount.lineEdit_AccountName.text()
        account_type = self.newaccount.comboBox_AccountTypes.currentText()
        #prohibited characters from file names or folders
        chars = ["#", "%", "&", "{", "}", "\", '<', >", "*", "?", "/", "$", "!", "'", '"', ":", "@", "+", ",", "|", "="]
        chars_text = ""
        for i in chars:
            chars_text += str(i) + " "
        verify = False
        for x in account_name:
            if x != " ": verify = True
        for x in chars:
            if x in account_name:
                verify = False
        #Check if folder directory already exists for account
        if fm.check_account(account_name) == False:
            verify = False

        if verify == True and len(account_name) > 1:
            db.add_account(account_name, account_type, 99, 99, 99, 99, "Config", 99, "Config")
            show_accounts()
            fm.create_account(account_name)
        else:
            alert = AlertMessage(self, "Failed to Add Account","Failed to add account", "Cannot use any prohibited characters and name must be more than two characters", chars_text)
            alert.exec_()

class AccountsConfig_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accountsconfig = Ui_AccountsConfig()
        self.accountsconfig.setupUi(self)
        #Buttons
        self.accountsconfig.pushButton_Cancel.clicked.connect(show_accounts)
        self.accountsconfig.pushButton_Config.clicked.connect(self.config)
        self.accountsconfig.pushButton_Cancel_Config.clicked.connect(show_AccountsConfig)
        self.accountsconfig.pushButton_Save.clicked.connect(self.config_save)
        #Hide 
        self.accountsconfig.label_Account.hide()
        self.accountsconfig.label_TransDate.hide()
        self.accountsconfig.label_PostedDate.hide()
        self.accountsconfig.label_Description.hide()
        self.accountsconfig.label_Amount1.hide()
        self.accountsconfig.label_Amount2.hide()
        self.accountsconfig.label_Sign1.hide()
        self.accountsconfig.label_Sign2.hide()
        self.accountsconfig.comboBox_TransDateCol.hide()
        self.accountsconfig.comboBox_PostedDateCol.hide()
        self.accountsconfig.comboBox_DescriptionCol.hide()
        self.accountsconfig.comboBox_Amount1Col.hide()
        self.accountsconfig.comboBox_Amount2Col.hide()
        self.accountsconfig.comboBox_Sign1.hide()
        self.accountsconfig.comboBox_Sign2.hide()
        self.accountsconfig.pushButton_Cancel_Config.hide()
        self.accountsconfig.pushButton_Save.hide()
        

        for x in db.accounts:
            self.accountsconfig.comboBox_Accounts.addItem(x[1])

    def config(self):
        self.accountsconfig.label_Account.show()
        self.accountsconfig.label_TransDate.show()
        self.accountsconfig.label_PostedDate.show()
        self.accountsconfig.label_Description.show()
        self.accountsconfig.label_Amount1.show()
        self.accountsconfig.label_Amount2.show()
        self.accountsconfig.label_Sign1.show()
        self.accountsconfig.label_Sign2.show()
        self.accountsconfig.comboBox_TransDateCol.show()
        self.accountsconfig.comboBox_PostedDateCol.show()
        self.accountsconfig.comboBox_DescriptionCol.show()
        self.accountsconfig.comboBox_Amount1Col.show()
        self.accountsconfig.comboBox_Amount2Col.show()
        self.accountsconfig.comboBox_Sign1.show()
        self.accountsconfig.comboBox_Sign2.show()
        self.accountsconfig.pushButton_Cancel_Config.show()
        self.accountsconfig.pushButton_Save.show()
        self.accountsconfig.pushButton_Config.hide()
        self.accountsconfig.pushButton_Cancel.hide()

        self.accountsconfig.label_Account.setText(self.accountsconfig.comboBox_Accounts.currentText())
        self.accountsconfig.comboBox_Accounts.hide()
        self.accountsconfig.comboBox_TransDateCol.addItem("Dont Need")
        for i in range(1, 11, 1): self.accountsconfig.comboBox_TransDateCol.addItem(str(i))
        for i in range(1, 11, 1): self.accountsconfig.comboBox_PostedDateCol.addItem(str(i))
        for i in range(1, 11, 1): self.accountsconfig.comboBox_DescriptionCol.addItem(str(i))
        for i in range(1, 11, 1): self.accountsconfig.comboBox_Amount1Col.addItem(str(i))
        for i in range(1, 11, 1): self.accountsconfig.comboBox_Amount2Col.addItem(str(i))
        self.accountsconfig.comboBox_Amount2Col.addItem("Dont Need")
        self.accountsconfig.comboBox_Sign1.addItems(["Use original sign", "Reverse Sign"])
        self.accountsconfig.comboBox_Sign2.addItems(["Use original sign", "Reverse Sign"])

    def config_save(self):
        account_name = self.accountsconfig.label_Account.text()
        trans_date_col = self.accountsconfig.comboBox_TransDateCol.currentText()
        posted_date_col = self.accountsconfig.comboBox_PostedDateCol.currentText()
        desc_col = self.accountsconfig.comboBox_DescriptionCol.currentText()
        amt1_col = self.accountsconfig.comboBox_Amount1Col.currentText()
        sign1_col = self.accountsconfig.comboBox_Sign1.currentText()
        amt2_col = self.accountsconfig.comboBox_Amount2Col.currentText()
        sign2_col = self.accountsconfig.comboBox_Sign2.currentText()
        
        for x in db.accounts:
            if x[1] == account_name:
                id = x[0]
                account_type = x[2]
        db.update_account(id, account_name, account_type, trans_date_col, posted_date_col, desc_col, amt1_col, sign1_col, amt2_col, sign2_col)

        show_AccountsConfig()

class ImportManager_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.importmanager = Ui_ImportManager()
        self.importmanager.setupUi(self)

        #Buttons
        self.importmanager.pushButton_Home.clicked.connect(lambda: show_dashboard("Auto"))
        self.importmanager.pushButton_Import.clicked.connect(self.import_data)
        self.importmanager.pushButton_SaveNote.clicked.connect(self.update_note)

        #Notes 
        import_notes = db.get_import_notes()
        self.importmanager.textEdit_ImportNotes.setText(import_notes)

        self.importmanager.treeWidget_Imports.setHeaderLabels(["Account", "File"])
        if db.accounts[0][0] != "NA":
            account_files = fm.get_import_data(db.accounts)
            for i in account_files:
                item = qtw.QTreeWidgetItem([i[0], f"{i[1]} Files"])
                for x in i[2]:
                    c_item = qtw.QTreeWidgetItem(["----", x])
                    item.addChild(c_item)

                self.importmanager.treeWidget_Imports.addTopLevelItem(item)
            self.importmanager.treeWidget_Imports.expandAll()
        else:
            self.importmanager.pushButton_Import.setDisabled(True)
    
    def import_data(self):
        account_files = fm.get_import_data(db.accounts)

        #Loop through Accounts
        imported_count = 0
        failed_count = 0
        import_status_text = []
        import_file_text = []

        for i in account_files:
            if i[1]== 0:
                print(f"\nIMPORTING ACCOUNT: {i[0]}...No Files to Import")
            else:
                #Loop through files
                for x in i[2]:
                    #Get File that is being imported for pop up window
                    import_file_text.append(x)
                    #Getting Config Settings for Accounts
                    for accounts in db.accounts:
                        if accounts[1] == i[0]:
                            file = (f"Accounts/{i[0]}/{x}")
                            fname = x
                            
                            if accounts[3] != "Dont Need":
                                TransDateCol = int(accounts[3])
                            else:
                                TransDateCol = accounts[3]

                            PostedDateCol = int(accounts[4])
                            DescCol = int(accounts[5])
                            Amt1Col = int(accounts[6])
                            Sign1 = accounts[7]

                            if accounts[8] != "Dont Need":
                                Amt2Col = int(accounts[8])
                            else:
                                Amt2Col = accounts[8]
                            Sign2 = accounts[9]
                            
                            if Sign1 != "Config":
                                print(f"\nIMPORTING ACCOUNT: {i[0]}...IMPORTING Accounts/{i[0]}/{x}")
                                import_data = CSV_Manager.get_data(file,i[0],TransDateCol, PostedDateCol, DescCol,Amt1Col, Sign1,Amt2Col,Sign2)
                                
                                if import_data[0] == "Success":
                                    data = import_data[1]

                                    ##### --- INSERT KEY WORKD TAGGING HERE --- #####
                                    keyword_rules = db.get_keywordrules()
                                    data_keyword_tagging = []
                                    tagged = False
                                    if db.get_keywordrules() != False:
                                        for expense in data:
                                            tagged = False
                                            #Index 5 is the expense description
                                            for rule in keyword_rules:
                                                if rule[1].upper() in expense[18].upper():
                                                    print(f'Found Tag: {rule} --- {expense[19]}')
                                                    data_keyword_tagging.append([expense[0], expense[1], expense[2], expense[3], expense[4], expense[5], expense[6], expense[7], expense[8], expense[9], expense[10], expense[11], expense[12], expense[13], expense[14], expense[15], expense[16], expense[17], expense[18], expense[19], rule[2], rule[3], expense[22], expense[23]])
                                                    tagged = True
                                            if not tagged:
                                                data_keyword_tagging.append([expense[0], expense[1], expense[2], expense[3], expense[4], expense[5], expense[6], expense[7], expense[8], expense[9], expense[10], expense[11], expense[12], expense[13], expense[14], expense[15], expense[16], expense[17], expense[18], expense[19], expense[20], expense[21], expense[22], expense[23]])
                                    else:
                                        data_keyword_tagging = data
                                    ##### --- #####
                                
                                    #Import/Save Expenses
                                    #(Account, Month, Year, Data)
                                    
                                    db.import_expenses(data_keyword_tagging[0][0], data_keyword_tagging[0][5], data_keyword_tagging[0][7], data_keyword_tagging)

                                    print(f"data[0][0]: {data[0][0]}")
                                    #Move Files to processed folder
                                    fm.move_files(file, fname, accounts[1])

                                    imported_count +=1
                                    import_status_text.append("Successfully Imported Data")
                                else:
                                    print(f"{import_data[0]}..FAILED TO IMPORT FILE: {file}")

                                    import_status_text.append(import_data[1])
                                    failed_count +=1
                            else:
                                print(f"\nIMPORTING ACCOUNT: {i[0]}...CONFIG ACCOUNT REQUIRED")
                                import_status_text.append("Config Account Required")
                                failed_count +=1
        pop_up_details = ""
        x = 0
        for i in import_file_text:
            pop_up_details = pop_up_details + f"\nFile: {i}....{import_status_text[x]}"
            x+=1

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Successfully Imported Data")
        msg.setInformativeText(f"Imported {imported_count} Files\nFailed Count: {failed_count}")
        msg.setWindowTitle("Import Manager")
        msg.setDetailedText(pop_up_details)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QLabel{min-width: 700px;}");
        msg.exec_()
        show_ImportManager()
    
    def update_note(self):
        update_note = db.update_import_notes(self.importmanager.textEdit_ImportNotes.toPlainText())
        if update_note:
            status = AlertMessage(self, "Update Note Status ", "Successfully updated note...", "", "")
            status.exec_()
        else:
            status = AlertMessage(self, "Update Note Status ", "Failed to update note...", "", "")
            status.exec_()



        #CSV_Manager.get_data("Eastex.csv", 2, 3, 4, "Use Original Sign", "Dont Need", "Use original sign")

class TagManager_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tagmanager = Ui_TagManager()
        self.tagmanager.setupUi(self)

        ##### --- Buttons --- #####
        self.tagmanager.pushButton_Home.clicked.connect(lambda: show_dashboard("Auto"))
        self.tagmanager.pushButton_RefreshData.clicked.connect(self.refresh_data)
        self.tagmanager.pushButton_UpdateDatabase.clicked.connect(self.update_database)
        self.tagmanager.commandLinkButton_EditTags.clicked.connect(show_Tags)
        #self.tagmanager.pushButton_LockAll.clicked.connect(self.lock_all)
        self.tagmanager.commandLinkButton_LockAll.clicked.connect(self.lock_all)
        self.tagmanager.commandLinkButton_UnlockAll.clicked.connect(self.unlock_all)
        self.tagmanager.commandLinkButton_LockTagged.clicked.connect(self.lock_tagged)
        ##### --- #####

        ##### --- Set Dates From/To for Filtering to have 4 digit years --- #####
        self.tagmanager.dateEdit_From.setDisplayFormat("M/dd/yyyy")
        self.tagmanager.dateEdit_To.setDisplayFormat("M/dd/yyyy")
        ##### --- #####

        ##### --- Set up Status Bar for Table --- #####

        self.tagmanager.tableWidget_Expenses.itemSelectionChanged.connect(self.update_status_bar)

        ##### --- #####

        #Edit QTableWidget 
        self.tagmanager.tableWidget_Expenses.setColumnCount(25)
        self.tagmanager.tableWidget_Expenses.setHorizontalHeaderLabels(["id", "Account", "TransMonth", "TransDay", "TransYear", "TransDate","PostedMonth", "PostedDay", "PostedYear", "PostedDate","OvrBoolean","OvrMonth", "OvrDay", "OvrYear", "OvrDate","CalcMonth", "CalcDay", "CalcYear", "CalcDate", "Description", "Amount", "Tag 1", "Tag 2", "Lock", "Note"])
        #Edit Combo Boxes
        self.tagmanager.comboBox_Filter.addItems(["Month-Year","Untagged", "Show All", "Month-Year-To-From"])
        tag1s = []
        for tag in db.get_tag1s():
            tag1s.append(tag[1])
        self.tagmanager.comboBox_Tag1s.addItems(["*"])
        self.tagmanager.comboBox_Tag1s.addItems(tag1s)

        accounts = []
        for account in db.accounts:
            accounts.append(account[1])
        self.tagmanager.comboBox_Accounts.addItems(["*"])
        self.tagmanager.comboBox_Accounts.addItems(accounts)

        #Set Date Edits
        dates = jarvis.get_date_bounds(int(m), int(y))
        from_year = dates[0][2]
        from_month = dates[0][0]
        from_day = dates[0][1]

        to_year = dates[1][2]
        to_month = dates[1][0]
        to_day = dates[1][1]
        from_date = qtc.QDate(from_year,from_month, from_day)
        to_date = qtc.QDate(to_year, to_month, to_day)
        self.tagmanager.dateEdit_From.setDate(from_date)
        self.tagmanager.dateEdit_To.setDate(to_date)

        

    def refresh_data(self):
        #https://www.youtube.com/watch?v=8RUxvqt2tAk&t=336s  - Tiered Combo boxes
        mode = self.tagmanager.comboBox_Filter.currentText()
        tag_selection = self.tagmanager.comboBox_Tag1s.currentText()
        account_selection = self.tagmanager.comboBox_Accounts.currentText()
        if mode == "Show All": 
            data = db.get_expenses(mode,1,1,1,1, tag_selection, account_selection)
        elif mode == "Month-Year" or mode == "Month-Year-To-From": 
            from_date = self.tagmanager.dateEdit_From.text()
            from_date = from_date.split("/")
            to_date = self.tagmanager.dateEdit_To.text()
            to_date = to_date.split("/")
            
            month_1 = from_date[0]
            year_1 = from_date[2]
            month_2 = to_date[0]
            year_2 = to_date[2]
            
           
            data = db.get_expenses(mode, month_1, year_1, month_2, year_2, tag_selection, account_selection)
            
            

        elif mode == "Untagged":
            data = db.get_expenses(mode, 1, 1, 1, 1)

        #If there was data sent back from db.getexpenses, will send back False if no data fits criteria
        total_sum = 0
        if data != False:
            
            #data = db.get_expenses(mode, 1, 1, 1, 1)
            self.tagmanager.tableWidget_Expenses.clearContents()
            row_count = len(data)
            self.tagmanager.tableWidget_Expenses.setRowCount(row_count)
            row = 0
            col = 0                 
            tags1 = db.get_tag1s()
                
            tags2 = db.get_tag2s()

            for x in data:
                # For status bar below the table
                total_sum += float(x[20])
                for y in x:
                    if col == 21:
                        if tags1 != False:
                            tags1.sort(key=lambda x: x[1]) #Sort Tags Alphabetically
                            #Locked
                            combo3 = ComboTag3(self, f"{row}_{col+2}_3", x[23])
                            self.tagmanager.tableWidget_Expenses.setCellWidget(row, col+2, combo3)
                            #If Tag 1s are set up but none of the expenses are Tagged, they will equal NA until they are tagged
                            if y != "NA":
                                for tag in tags1:
                                    if tag[1] == y and tag[4] != "False":
                                        combo2 = ComboTag2(self, f"{row}_{col+1}_2", x[22], y, tags2)
                                        combo = ComboTag1(self, f"{row}_{col}", y, tags1, True, tags2)
                                        self.tagmanager.tableWidget_Expenses.setCellWidget(row, col+1, combo2)
                                        self.tagmanager.tableWidget_Expenses.setCellWidget(row, col, combo)
                                    else:
                                        self.tagmanager.tableWidget_Expenses.setItem(row, col, qtw.QTableWidgetItem(str(y)))
                                        self.tagmanager.tableWidget_Expenses.setItem(row, col+1, qtw.QTableWidgetItem(str("--")))
                            else:
                                combo2 = ComboTag2(self, f"{row}_{col+1}_2", x[22], "NA", tags2)
                                combo = ComboTag1(self, f"{row}_{col}", y, tags1, False, tags2)
                                self.tagmanager.tableWidget_Expenses.setCellWidget(row, col+1, combo2)
                                self.tagmanager.tableWidget_Expenses.setCellWidget(row, col, combo)
                            
                        else:
                            #Set Tag Columns to Black when Tags are not set up
                            item = qtw.QTableWidgetItem(str("-"))
                            item_1 = qtw.QTableWidgetItem(str("-"))
                            item.setTextAlignment(qtc.Qt.AlignCenter)
                            self.tagmanager.tableWidget_Expenses.setItem(row, col, item)
                            self.tagmanager.tableWidget_Expenses.setItem(row, col+1, item_1)
                            self.tagmanager.tableWidget_Expenses.item(int(row), int(21)).setBackground(QtGui.QColor("#0b120d"))
                            self.tagmanager.tableWidget_Expenses.item(int(row), int(22)).setBackground(QtGui.QColor("#0b120d"))

                    elif col == 10:
                        name = f"Overide_{row}_{col}"
                        ComboOvr = ComboTag5(self,name,y)
                        self.tagmanager.tableWidget_Expenses.setCellWidget(row, col,ComboOvr)


                    elif col !=22 and col != 23 and col != 10:
                        item = qtw.QTableWidgetItem(str(y))
                        item.setTextAlignment(qtc.Qt.AlignCenter)
                        self.tagmanager.tableWidget_Expenses.setItem(row, col, item)
                    #Increment through Columns
                    col += 1
                #Increment through Rows and set Colummn back to Column 0
                row += 1
                col = 0
        self.tagmanager.tableWidget_Expenses.horizontalHeader().setStyleSheet("::section {background-color: #e0e0ff;font: 12pt ""Arial Rounded MT Bold"";border: 1px solid black}")
        self.tagmanager.tableWidget_Expenses.resizeColumnsToContents()  

        ##### --- Hide Columns --- #####
        hide = True
        if hide == True:
            self.tagmanager.tableWidget_Expenses.hideColumn(0)
            self.tagmanager.tableWidget_Expenses.hideColumn(2)
            self.tagmanager.tableWidget_Expenses.hideColumn(3)
            self.tagmanager.tableWidget_Expenses.hideColumn(4)
            self.tagmanager.tableWidget_Expenses.hideColumn(6)
            self.tagmanager.tableWidget_Expenses.hideColumn(7)
            self.tagmanager.tableWidget_Expenses.hideColumn(8)
            self.tagmanager.tableWidget_Expenses.hideColumn(11)
            self.tagmanager.tableWidget_Expenses.hideColumn(12)
            self.tagmanager.tableWidget_Expenses.hideColumn(13)
            self.tagmanager.tableWidget_Expenses.hideColumn(15)
            self.tagmanager.tableWidget_Expenses.hideColumn(16)
            self.tagmanager.tableWidget_Expenses.hideColumn(17)

        ##### --- Disable Columns --- ####
        for row in range(self.tagmanager.tableWidget_Expenses.rowCount()):
            Account = self.tagmanager.tableWidget_Expenses.item(row, 1)
            Account.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)

            TransDate = self.tagmanager.tableWidget_Expenses.item(row, 5)
            TransDate.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)

            PostedDate = self.tagmanager.tableWidget_Expenses.item(row, 9)
            PostedDate.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)

            CalcDate = self.tagmanager.tableWidget_Expenses.item(row, 14)
            CalcDate.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)

            CalcDate = self.tagmanager.tableWidget_Expenses.item(row, 18)
            CalcDate.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)

            Description = self.tagmanager.tableWidget_Expenses.item(row, 19)
            Description.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)

            Amount = self.tagmanager.tableWidget_Expenses.item(row, 20)
            Amount.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)
        ##### --- #####

        ##### --- Update Status Bar at the bottom --- #####
        self.tagmanager.label_table_total.setText(f"TOTAL: {str(round(total_sum,2))}")

        ##### --- #####
         
    def update_database(self):
        row_count = self.tagmanager.tableWidget_Expenses.rowCount()
        col_count = self.tagmanager.tableWidget_Expenses.columnCount()
        table_data_clean = []
        if row_count != 0:
            for row in range(row_count):
                table_data = []
                for col in range(col_count):
                    #print(f"({row}, {col})")
                    if col == 21 or col == 22 or col == 10 or col == 23:
                        cell_widget = self.tagmanager.tableWidget_Expenses.cellWidget(row, col)
                        if isinstance(cell_widget, QComboBox):
                            table_data.append(cell_widget.currentText())
                        else:
                            table_data.append(self.tagmanager.tableWidget_Expenses.item(row, col).text())
                    else:
                        table_data.append(self.tagmanager.tableWidget_Expenses.item(row, col).text())
                        #print(self.tagmanager.tableWidget_Expenses.item(row, col).text())
                table_data_clean.append(table_data)
            #OLD ---df = pd.DataFrame(data= table_data_clean, columns = ["id", "Account", "Month", "Day", "Year", "Date", "Description", "Amount", "Tag 1", "Tag 2", "Lock"])
            #print(df)
            db.update_expenses(table_data_clean)
            show_TagManager()
        else:
            alert = AlertMessage(self, "Cannot Update Database","No data in Table to update", "Please refresh table and make changes and then try to update", False)
            alert.exec_()
    
    def lock_all(self):
        if self.tagmanager.tableWidget_Expenses.rowCount() >0:
            row_count = self.tagmanager.tableWidget_Expenses.rowCount()
            row = 0
            col = 23
            for i in range(row_count):
                cell_widget = self.tagmanager.tableWidget_Expenses.cellWidget(row, col)
                if cell_widget.currentText() == "Unlocked":
                    if cell_widget.currentIndex() == 0:
                        cell_widget.setCurrentIndex(1)
                    else:
                        cell_widget.setCurrentIndex(0)
                row +=1

    def unlock_all(self):
        if self.tagmanager.tableWidget_Expenses.rowCount() > 0:
            row_count = self.tagmanager.tableWidget_Expenses.rowCount()
            row = 0
            col = 23
            for i in range(row_count):
                cell_widget = self.tagmanager.tableWidget_Expenses.cellWidget(row, col)
                if cell_widget.currentText() == "Lock":
                    if cell_widget.currentIndex() == 0:
                        cell_widget.setCurrentIndex(1)
                    else:
                        cell_widget.setCurrentIndex(0)
                row +=1

    def lock_tagged(self):
        if self.tagmanager.tableWidget_Expenses.rowCount() > 0:
            row_count = self.tagmanager.tableWidget_Expenses.rowCount()
            row = 0
            col_tag1 = 21
            col_lock = 23
            for i in range(row_count):
                cell_widget_tag1 = self.tagmanager.tableWidget_Expenses.cellWidget(row, col_tag1)
                if cell_widget_tag1.currentText() != "NA":
                    cell_widget_lock = self.tagmanager.tableWidget_Expenses.cellWidget(row, col_lock)
                    if cell_widget_lock.currentText() == "Unlocked":
                        if cell_widget_lock.currentIndex() == 0:
                            cell_widget_lock.setCurrentIndex(1)
                        else:
                            cell_widget_lock.setCurrentIndex(0)
                row +=1

    def update_status_bar(self):
        selected_ranges = self.tagmanager.tableWidget_Expenses.selectedRanges()
        total_sum = 0
        for selected_range in selected_ranges:
            for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):
                number = self.tagmanager.tableWidget_Expenses.item(row, 20).text()
                amount = float(number)
                #total_sum += float(item.text())
                total_sum += amount
                
        self.tagmanager.label_table_sum.setText(f"SELECTED: {str(round(total_sum,2))}")

class Analytics_Widget(qtw.QWidget):
    def __init__(self, year_selection):
        super().__init__()

        self.anaylytics = UI_Analytics()
        self.anaylytics.setupUi(self)

        ##### --- Buttons --- #####
        self.anaylytics.pushButton_Home.clicked.connect(show_dashboard)
        ##### --- #####

        ##### --- Set Year Combo Box --- #####
        years = db.get_expense_years()
        for i in years:
            self.anaylytics.comboBox_year.addItem(i)
        self.anaylytics.comboBox_year.setCurrentText(str(year_selection))
        self.anaylytics.comboBox_year.currentIndexChanged.connect(lambda: show_Analytics(int(self.anaylytics.comboBox_year.currentText())))
        ##### --- #####
        
        tag1s = db.get_tag1s()
        tag2s = db.get_tag2s()
        

        ##### --- Tree Widget Setup --- #####
        year = year_selection
        self.anaylytics.treeWidget_Analytics.clear()
        self.anaylytics.treeWidget_Analytics.setHeaderLabels(["Tag", "Jan", "Feb", "Mar", "Apr", "May", "Jun", 'Jul', 'Aug', "Sep", 'Oct', "Nov", "Dec", 'Total'])
        
        

        # Center-align header text
        header = self.anaylytics.treeWidget_Analytics.header()
        header.setDefaultAlignment(qtc.Qt.AlignCenter)

        expenses_by_month = []
        for month in range(1, 13):
            
            expenses = db.get_expenses("Month-Year", str(month), str(year), 0, 0)
            if expenses != False:
                expenses_cleaned = jarvis.remove_overridden_expenses(expenses, month, year)
                expenses_by_month.append(expenses_cleaned)

        ##### --- Create empty tree dict object to update --- #####
        tree_data = {}
        for tag1 in tag1s:
            tree_data[tag1[1]] = None

        for tag1 in tag1s:
            dummy_dict = {}
            for tag2 in tag2s:
                tag1_2 = tag2[1]
                tag2_text = tag2[2]
                if tag1_2 == tag1[1]:
                    dummy_dict[tag2_text] = [0,0,0,0,0,0,0,0,0,0,0,0]

            dummy_dict["--"] = [0,0,0,0,0,0,0,0,0,0,0,0]
            tree_data[tag1[1]] = [[0,0,0,0,0,0,0,0,0,0,0,0], dummy_dict]
            

        tree_data["NA"] = [[0,0,0,0,0,0,0,0,0,0,0,0], {"NA": [0,0,0,0,0,0,0,0,0,0,0,0]}]
        ##### --- #####

        ##### --- Send expenses and data to jarvis to update tree_dict --- #####
        tree_data_final = jarvis.analytics_create_data(tree_data, expenses_by_month)
        ##### --- #####
        
        ##### --- Insert Data into Tree Widget --- #####
        if tag1s != False:
            for tag1 in tree_data_final:
                top_list_item = [tag1]
                total = float(0)
                for i in range(0, 12):
                    top_list_item.append(str(tree_data_final[tag1][0][i]))
                    total += float(tree_data_final[tag1][0][i])
                
                
                top_list_item.append(str(round(total,2)))

                item = qtw.QTreeWidgetItem(top_list_item)

                # Align items to center
                for i in range(1, 13):
                    item.setTextAlignment(i, qtc.Qt.AlignCenter)
            
                for tag2 in tree_data_final[tag1][1]:
                    child_list_items = [tag2]

                    child_totals = float(0)
                    for i in range(0, 12):
                        child_list_items.append(str(tree_data_final[tag1][1][tag2][i]))
                        child_totals += float(tree_data_final[tag1][1][tag2][i])
                        
                    child_list_items.append(str(round(child_totals,2)))

                    c_item = qtw.QTreeWidgetItem(child_list_items)

                    # Align child items text to center
                    for i in range(1, 13):
                        c_item.setTextAlignment(i, qtc.Qt.AlignCenter)
                    

                    item.addChild(c_item)
                    
                for i in range(0,14):
                    item.setBackground(i, QtGui.QColor("#ADD8E6"))   
                    
                # Define bold font
                bold_font = QtGui.QFont()
                bold_font.setBold(True)
                bold_font.setPointSize(12)  # Increase text size
                for i in range(0,14):
                    item.setFont(i, bold_font)

                
                self.anaylytics.treeWidget_Analytics.addTopLevelItem(item)
                count = 0
                for amount in top_list_item:
                    for t_1 in tag1s:
                        if t_1[1] == tag1 and count != 0 and count != 13:
                            budget = float(t_1[2])
                            if t_1[5] == "False":
                                item.setBackground(count, QtGui.QColor("#808080"))
                            elif float(amount) < budget:
                                item.setBackground(count, QtGui.QColor("#FF0000"))
                            else:
                                item.setBackground(count, QtGui.QColor("#00FF00"))
                        elif t_1[1] == tag1 and count == 13:
                            budget = (float(t_1[2])) * 12
                            if t_1[5] == "False":
                                item.setBackground(count, QtGui.QColor("#808080"))
                            elif float(amount) < budget:
                                item.setBackground(count, QtGui.QColor("#FF0000"))
                            else:
                                item.setBackground(count, QtGui.QColor("#00FF00"))                            
                    count += 1
                                
        delegate = CustomDelegate(self.anaylytics.treeWidget_Analytics)
        self.anaylytics.treeWidget_Analytics.setItemDelegate(delegate) 
        self.anaylytics.treeWidget_Analytics.resizeColumnToContents(0) #Resize column 0 to text width
        #self.anaylytics.treeWidget_Analytics.resizeColumnToContents(12) #Resize column 0 to text width
        #for i in range(0, 14):
            #self.anaylytics.treeWidget_Analytics.resizeColumnToContents(i) #Resize column 0 to text width


        # Apply Stylesheet to simulate grid lines
        test = False
        if test:
            self.anaylytics.treeWidget_Analytics.setStyleSheet("""
                QTreeWidget::item:has-children {
                    border: 2px solid rgb(11, 9, 8);  /* Border color for top-level items */
                    background-color:rgba(114, 132, 222, 0.93);  /* Light blue background */
                    color: rgb(11, 11, 8);
                    padding: 5px;
                }
                
                QTreeWidget::item:!has-children {
                    border: 2px solid rgb(11, 9, 8);  /* Border color for top-level items */
                    background-color:rgba(99, 107, 145, 0.93);  /* Light blue background */
                    padding: 5px;
                }

                QTreeWidget::item:selected {
                    background-color: lightblue;  /* Change this to any color */
                    color: black;  /* Ensure text remains visible */
                }

                QTreeWidget::item:hover {
                    background-color: #f0f0f0;  /* Light gray on hover */
                }
            """)
        
        ##### --- #####

class CustomDelegate(qtw.QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        
        # Only apply the border to the first column of top-level items
        if index.column() == 0 and not index.parent().isValid():  # Top-level items in column 0
            painter.save()
            pen = QtGui.QPen(QtGui.QColor("#FF5733"))  # Red border color
            pen.setWidth(2)  # Border width
            painter.setPen(pen)

            rect: qtc.QRect = option.rect
            painter.drawLine(rect.topLeft(), rect.topRight())  # Top border
            painter.drawLine(rect.topLeft(), rect.bottomLeft())  # Left border
            painter.drawLine(rect.topLeft(), rect.bottomLeft())
            painter.drawLine(rect.topRight(), rect.bottomRight())

            painter.restore()

        # Only apply the border to the first column of top-level items
        painter.save()
        pen = QtGui.QPen(QtGui.QColor("#000000"))  # Red border color
        pen.setWidth(2)  # Border width
        painter.setPen(pen)

        rect: qtc.QRect = option.rect
        painter.drawLine(rect.topLeft(), rect.topRight())  # Top border
        painter.drawLine(rect.topLeft(), rect.bottomLeft())  # Left border
        painter.drawLine(rect.topLeft(), rect.bottomLeft())
        painter.drawLine(rect.topRight(), rect.bottomRight())
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        painter.restore()

class KeywordTagging_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywordtagging = UI_KeywordTagging()
        self.keywordtagging.setupUi(self)

        #Buttons
        self.keywordtagging.pushButton_home.clicked.connect(show_dashboard)
        self.keywordtagging.pushButton_addRule.clicked.connect(show_AddKeywordRule)
        self.keywordtagging.pushButton_editeRule.clicked.connect(self.showEditRule)

        #Table Setup
        self.keywordtagging.tableWidget_rules.clear()
        keyword_rules = db.get_keywordrules()
        self.keywordtagging.tableWidget_rules.setColumnCount(4)
        self.keywordtagging.tableWidget_rules.setHorizontalHeaderLabels(["ID", "Keyword", "Tag 1", 'Tag 2'])
        row = 0
        
        if keyword_rules:
            for rule in keyword_rules:
                self.keywordtagging.tableWidget_rules.setRowCount(len(keyword_rules))
                self.keywordtagging.tableWidget_rules.setItem(row, 0, qtw.QTableWidgetItem(str(rule[0])))
                self.keywordtagging.tableWidget_rules.setItem(row, 1, qtw.QTableWidgetItem(rule[1]))
                self.keywordtagging.tableWidget_rules.setItem(row, 2, qtw.QTableWidgetItem(rule[2]))
                self.keywordtagging.tableWidget_rules.setItem(row, 3, qtw.QTableWidgetItem(rule[3]))

                self.keywordtagging.comboBox_editRule.addItem(str((rule[0])))
                
                row += 1
            self.keywordtagging.tableWidget_rules.cellClicked.connect(self.update_edit_rule)
            self.keywordtagging.tableWidget_rules.cellDoubleClicked.connect(self.showEditRule_1)
            
        else:
            self.keywordtagging.tableWidget_rules.setRowCount(1)
            self.keywordtagging.tableWidget_rules.setItem(0,0,qtw.QTableWidgetItem("No Rules Defined"))

    def showEditRule(self):
        id = self.keywordtagging.comboBox_editRule.currentText()
        show_EditKeywordRule(id)
    def showEditRule_1(self):
        row = self.keywordtagging.tableWidget_rules.currentItem().row()
        id = self.keywordtagging.tableWidget_rules.item(row, 0).text()
        show_EditKeywordRule(id)

    def update_edit_rule(self):
        current_row = self.keywordtagging.tableWidget_rules.currentItem().row()
        id = self.keywordtagging.tableWidget_rules.item(current_row, 0).text()
        self.keywordtagging.comboBox_editRule.setCurrentIndex(current_row)
                       
class EditKeywordRule_Widget(qtw.QWidget):
    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.editkeywordrule = UI_EditKeywordRule()
        self.editkeywordrule.setupUi(self)
       

        ##### --- Buttons --- #####
        self.editkeywordrule.pushButton_cancel.clicked.connect(show_KeywordTagging)
        self.editkeywordrule.pushButton_update.clicked.connect(self.update_keyword_rule)
        self.editkeywordrule.pushButton_deleteRule.clicked.connect(self.delete_rule)
        ##### --- #####

        ##### --- Database Calls --- #####
        tag1s = db.get_tag1s()
        tag2s = db.get_tag2s()
        rules = db.get_keywordrules()
        ##### --- #####

        ##### --- Set ID Label --- #####
        self.editkeywordrule.label_id.setText(str(id))
        ##### --- #####

        tag1_names, tag2_names = self.get_tag_names(tag1s, tag2s)
        count = 0
        for i in tag1_names:
            self.editkeywordrule.comboBox_tag1.addItem(i,tag2_names[count])
            count+=1

        for rule in rules:
            if str(rule[0]) == id:
                keyword = rule[1]
                tag1 = rule[2]
                tag2 = rule[3]

        self.editkeywordrule.lineEdit_key.setText(keyword)
        tag1_index = self.editkeywordrule.comboBox_tag1.findText(tag1)
        self.editkeywordrule.comboBox_tag1.setCurrentIndex(tag1_index)
        self.editkeywordrule.comboBox_tag2.clear()
        self.editkeywordrule.comboBox_tag2.addItems(self.editkeywordrule.comboBox_tag1.currentData())
        tag2_index = self.editkeywordrule.comboBox_tag2.findText(tag2)
        self.editkeywordrule.comboBox_tag2.setCurrentIndex(tag2_index)
        self.editkeywordrule.comboBox_tag1.currentIndexChanged.connect(self.update_combo_2)
        
    def update_keyword_rule(self):
        id = int(self.editkeywordrule.label_id.text())
        keyword = self.editkeywordrule.lineEdit_key.text()
        if len(keyword) >=3:
            tag1 = self.editkeywordrule.comboBox_tag1.currentText()
            tag2 = self.editkeywordrule.comboBox_tag2.currentText()
            new_rule = [keyword, tag1, tag2]
            existing_rules = db.get_keywordrules()
            check_keyword = jarvis.check_keyword_rules(new_rule, existing_rules, id)

            if check_keyword == True:
                db.update_keyword_rule(id, keyword, tag1, tag2)
                show_KeywordTagging()
            else:
                alert = AlertMessage(self, "Error with keyword rule", "Keyword rule is too similar to existing rule", "Any part of the new rule cannot exist within existing rules", "")
                alert.exec_()



    def delete_rule(self):
        id = int(self.editkeywordrule.label_id.text())
        db.delete_keyword_rule(id)
        show_KeywordTagging()

            
    def get_tag_names(self, tags1, tags2):
        tag1_names = []
        for i in tags1:
            if i[4] == "True":
                tag1_names.append(i[1])

        tag2_names = []
        if tags2 != False:
            for tag1 in tag1_names:
                tag2_holder = []
                check = False
                for tag2 in tags2:
                    if tag2[1] == tag1:
                        tag2_holder.append(tag2[2])
                        check = True
                if check == True:
                    tag2_names.append(tag2_holder)
                else:
                    tag2_names.append(["--"])
        else:
            for i in tags1:
                tag2_names.append(["--"])
        return tag1_names, tag2_names

    def update_combo_2(self):
        combo_2_data = self.editkeywordrule.comboBox_tag1.currentData()
        self.editkeywordrule.comboBox_tag2.clear()
        self.editkeywordrule.comboBox_tag2.addItems(combo_2_data)
        
class AddKeywordRule_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addkeywordrule = UI_AddKeywordRule()
        self.addkeywordrule.setupUi(self)

        #Buttons
        self.addkeywordrule.pushButton_cancel.clicked.connect(show_KeywordTagging)
        self.addkeywordrule.pushButton_save.clicked.connect(self.save_rule)

        #ComboBox - Tag 1 Setup
        tags1 = db.get_tag1s()
        tags2 = db.get_tag2s()
        tag1_names, tag2_names = self.get_tag_names(tags1, tags2)

        count = 0
        for i in tag1_names:
            self.addkeywordrule.comboBox_tag1.addItem(i,tag2_names[count])
            count+=1
        
        self.update_combo_2()
        self.addkeywordrule.comboBox_tag1.currentIndexChanged.connect(self.update_combo_2)

    def save_rule(self):
        key_word = self.addkeywordrule.lineEdit_key.text()
        if len(key_word) >= 3:
            tag1 = self.addkeywordrule.comboBox_tag1.currentText()
            tag2= self.addkeywordrule.comboBox_tag2.currentText()
            existing_keyword_rules = db.get_keywordrules()
            new_rule = [key_word, tag1, tag2]
            check_rule = jarvis.check_keyword_rules(new_rule, existing_keyword_rules)
            if check_rule == True:
                db.add_keyword_rule(key_word, tag1, tag2)
                show_KeywordTagging()
            else:
                alert = AlertMessage(self, "Error with keyword rule", "Keyword rule is too similar to existing rule", "Any part of the new rule cannot exist within existing rules", "")
                alert.exec_()
        else:
            alert = AlertMessage(self, "Error with keyword rule", "Keyword rule is too short", "Keyword rule must be a minimum length of 3 characters", "")
            alert.exec_()

    def update_combo_2(self):
        combo_2_data = self.addkeywordrule.comboBox_tag1.currentData()
        self.addkeywordrule.comboBox_tag2.clear()
        self.addkeywordrule.comboBox_tag2.addItems(combo_2_data)

    def get_tag_names(self, tags1, tags2):
        tag1_names = []
        for i in tags1:
            if i[4] == "True":
                tag1_names.append(i[1])
                
        tag2_names = []
        if tags2 != False:
            for tag1 in tag1_names:
                tag2_holder = []
                check = False
                for tag2 in tags2:
                    if tag2[1] == tag1:
                        tag2_holder.append(tag2[2])
                        check = True
                if check == True:
                    tag2_names.append(tag2_holder)
                else:
                    tag2_names.append(["--"])
        else:
            for i in tags1:
                tag2_names.append(["--"])
        return tag1_names, tag2_names

class Settings_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = Ui_Settings()
        self.settings.setupUi(self)


        #Buttons
        self.settings.pushButton_Home.clicked.connect(lambda: show_dashboard("Auto"))
        self.settings.pushButton_Tags.clicked.connect(show_Tags)
        self.settings.pushButton_DeveloperDetails.clicked.connect(show_Developer_Details)
        self.settings.pushButton_ApplicationSettings.clicked.connect(show_ApplicationSettings)
        self.settings.pushButton_keywordTagging.clicked.connect(show_KeywordTagging)

class DevloperDetails_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.developerdetails = UI_DeveloperDetails()
        self.developerdetails.setupUi(self)


        #Buttons
        self.developerdetails.pushButton_Settings.clicked.connect(show_Settings)

class ApplicationSettings_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applicationsettings = UI_ApplicationSettings()
        self.applicationsettings.setupUi(self)


        #Buttons
        self.applicationsettings.pushButton_Settings.clicked.connect(show_Settings)
        self.applicationsettings.pushButton_UpdateSettings.clicked.connect(self.update_settings)

        #Update Options
        settings = db.get_application_settings()
        StartUp = settings[1]
        BarChartZeros = settings[3
        ]
        if StartUp == "True":
            self.applicationsettings.comboBox_StartUpProcess.setCurrentIndex(0) #Index 0 is Enabled
        else:
            self.applicationsettings.comboBox_StartUpProcess.setCurrentIndex(1) #Index 1 is Diabled

        if BarChartZeros == "True":
            self.applicationsettings.comboBox_BarChartZeros.setCurrentIndex(0) #Index is Enabled
        else:
            self.applicationsettings.comboBox_BarChartZeros.setCurrentIndex(1) #Index is Disabled


    def update_settings(self):
        start_up_process = self.applicationsettings.comboBox_StartUpProcess.currentText()
        bar_chart_zeros = self.applicationsettings.comboBox_BarChartZeros.currentText()
        if start_up_process == "Enabled":
            StartUp = "True"
        else:
            StartUp = "False"

        if bar_chart_zeros == "Enabled":
            BarChartZeros = "True"
        else:
            BarChartZeros = "False"
        
        settings = [1, StartUp, BarChartZeros]

        status = db.update_application_settings(settings)

        if status:
            alert = AlertMessage(self, "Update Application Settings", "Successfully updated application settings..", "", "")
            alert.exec_()
        else:
            alert = AlertMessage(self, "Update Application Settings", "Failed to update application settings..", "", "")
            alert.exec_()

class Tags_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = UI_Tags()
        self.tags.setupUi(self)

        ##### --- Buttons --- #####
        self.tags.pushButton_Home.clicked.connect(lambda: show_dashboard("Auto"))
        self.tags.pushButton_AddTag1.clicked.connect(show_AddTag1)
        self.tags.pushButton_Edit_Tag1.clicked.connect(self.show_EditTag1)
        self.tags.pushButton_convert_tags.clicked.connect(self.convert_tags)
        self.tags.pushButton_DeleteTag1.clicked.connect(show_DeleteTag1)
        ##### --- #####

        if db.get_tag1s() == False:
            self.tags.pushButton_Edit_Tag1.setDisabled(True)
            self.tags.pushButton_AddTag2.setDisabled(True)
            self.tags.pushButton_convert_tags.setDisabled(True)
        else:
            self.tags.pushButton_AddTag2.clicked.connect(show_AddTag2)

        #Tree Widget
        tags1 = db.get_tag1s()
        tags2 = db.get_tag2s()
        self.tags.treeWidget_Tags.setHeaderLabels(["Tag 1", "Budget", "Enabled", "Use in Calculations", "Count"])
        
        expenses = db.get_expenses("Show All", 0, 0, 0,0)
        tier1_delete_check = True
        tier2_delete_check = True
        if tags1 != False:
            #Sort Tag1s
            tags1.sort(key=lambda x: x[1])
            for i in tags1:
                if i[1] != "NA":
                    self.tags.comboBox_EditTag1.addItem(i[1])
                    tier1_count = 0
                    # Get count of tag 1's used in database
                    for expense in expenses:
                        if expense[21] == i[1]:
                            tier1_count += 1
                            
                    if tier1_count == 0:
                        tier1_delete_check = False
                    item = qtw.QTreeWidgetItem([i[1], f"$ {i[2]}", i[4], i[5], str(tier1_count)])
                    if tags2 != False:
                        for x in tags2:
                            if x[1] == i[1]:
                                tier2_count = 0
                                for expense in expenses:
                                    if expense[21] == i[1] and expense[22] == x[2]:
                                        tier2_count += 1
                                        
                                if tier2_count == 0:
                                    tier2_delete_check = False
                                c_item = qtw.QTreeWidgetItem([f" {x[2]}", "", "", "", str(tier2_count)])
                                item.addChild(c_item)
                    
                    self.tags.treeWidget_Tags.addTopLevelItem(item)
        if tier1_delete_check:
            self.tags.pushButton_DeleteTag1.setEnabled(False)
        if tier2_delete_check:
            self.tags.pushButton_DeleteTag2.setEnabled(False)

    def convert_tags(self):
        show_TagsConvert()

    def show_EditTag1(self):
        current_text = self.tags.comboBox_EditTag1.currentText()
        show_EditTag1(current_text)

class TagsConvert_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tagsconvert = UI_TagsConvert()
        self.tagsconvert.setupUi(self)

        ##### --- Buttons --- #####
        self.tagsconvert.pushButton_cancel.clicked.connect(show_Tags)
        self.tagsconvert.pushButton_convert.clicked.connect(self.convert_tags)
        ##### --- #####



        tag1s = db.get_tag1s()
        tag2s = db.get_tag2s()
        ##### --- Update Old Tag combo boxes --- #####
        for tag in tag1s:
            tag2 = []
            
            if tag2s != False:
                for x in tag2s:
                    if x[1] == tag[1]:
                        tag2.append(x[2])
            
            tag2.append("--")
            self.tagsconvert.comboBox_old_tag1.addItem(tag[1], tag2)
        
        index = self.tagsconvert.comboBox_old_tag1.currentIndex()
        self.tagsconvert.comboBox_old_tag2.clear()
        self.tagsconvert.comboBox_old_tag2.addItems(self.tagsconvert.comboBox_old_tag1.itemData(index))
        self.tagsconvert.comboBox_old_tag1.currentIndexChanged.connect(self.update_old_tag2)
        ##### --- #####

        ##### --- Update New Tag combo boxes --- #####
        for tag in tag1s:
            tag2 = []
            
            if tag2s != False:
                for x in tag2s:
                    if x[1] == tag[1]:
                        tag2.append(x[2])
        
            tag2.append("--")
            self.tagsconvert.comboBox_new_tag1.addItem(tag[1], tag2)
        
        index = self.tagsconvert.comboBox_new_tag1.currentIndex()
        self.tagsconvert.comboBox_new_tag2.clear()
        self.tagsconvert.comboBox_new_tag2.addItems(self.tagsconvert.comboBox_new_tag1.itemData(index))
        self.tagsconvert.comboBox_new_tag1.currentIndexChanged.connect(self.update_new_tag2)
        ##### --- #####


    def convert_tags(self):
        tag1 = self.tagsconvert.comboBox_old_tag1.currentText()
        tag2 = self.tagsconvert.comboBox_old_tag2.currentText()

        new_tag1 = self.tagsconvert.comboBox_new_tag1.currentText()
        new_tag2 = self.tagsconvert.comboBox_new_tag2.currentText()

        expense_ids = db.get_tags_to_convert(tag1, tag2)

        if expense_ids:
            print(f'Number of expenses to convert: {len(expense_ids)}')
            

            ids = []
            for expense in expense_ids:
              ids.append(expense[0])

            db.convert_tags(ids, [new_tag1, new_tag2])

            alert = AlertMessage(self, "Successfully Converted Tags", f"Converted {len(expense_ids)} tags -------", "See detailed text for conversion details", f"Tag 1: {tag1} --> {new_tag1} \nTag 2: {tag2} ---> {new_tag2}")
            alert.exec_()
            show_Tags()

        else:
            print("No expenses contain these tags")
            alert = AlertMessage(self, "Converted Tags", f"No expenses in database were assigned these tags", "", f"Tag 1: {tag1} \nTag 2: {tag2}")
            alert.exec_()

    def update_old_tag2(self):
        index = self.tagsconvert.comboBox_old_tag1.currentIndex()
        self.tagsconvert.comboBox_old_tag2.clear()
        self.tagsconvert.comboBox_old_tag2.addItems(self.tagsconvert.comboBox_old_tag1.itemData(index))

    def update_new_tag2(self):
        index = self.tagsconvert.comboBox_new_tag1.currentIndex()
        self.tagsconvert.comboBox_new_tag2.clear()
        self.tagsconvert.comboBox_new_tag2.addItems(self.tagsconvert.comboBox_new_tag1.itemData(index))

class DeleteTag1_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deletetag1 = UI_DeleteTag1()
        self.deletetag1.setupUi(self)


        ##### --- Buttons --- #####
        self.deletetag1.pushButton_cancel.clicked.connect(show_Tags)
        self.deletetag1.pushButton_delete.clicked.connect(self.delete)
        ##### --- #####

        tag1s = db.get_tag1s()        
        expenses = db.get_expenses("Show All", 0,0,0,0)
        tag1s_not_used = []

        if tag1s != False and expenses != False:
            for tag1 in tag1s:
                tier1_count = 0
                tag = tag1[1]
                tag_id = tag1[0]
                for expense in expenses:
                    if expense[21] == tag:
                        tier1_count += 1
                if tier1_count == 0:
                    tag1s_not_used.append([tag_id, tag])
                    
            if tag1s_not_used != []:
                for tag in tag1s_not_used:
                    self.deletetag1.comboBox_tag1s.addItem(tag[1], tag[0])

            if tag1s == False:
                alert = AlertMessage(self, "No Tag1s Created", "There are no Tag 1's created in the database", "", "")
                alert.exec_()
            elif expenses == False:
                alert = AlertMessage(self, "No Tag1s Created", "There are no Tag 1's created in the database", "", "")
                alert.exec_()
            elif tag1s_not_used == []:
                alert = AlertMessage(self, "Tag 1s Unavailable", "There are no Tag 1's not being used in the database ", "Please use the convert tags to free a tag 1 for deletion", "")
                alert.exec()

            if tag1s == False or expenses == False or tag1s_not_used == []:
                
                print("here")



    def delete(self):
        tag1_id = int(self.deletetag1.comboBox_tag1s.currentData())
        tag1 = self.deletetag1.comboBox_tag1s.currentText()
        ##### --- Delete Any Keyword Rules created with this tag --- #####
        keyword_rules_deleted = 0
        keyword_rules = db.get_keywordrules()
        for rule in keyword_rules:
            if rule[2] == tag1:
                db.delete_keyword_rule(rule[0])
                keyword_rules_deleted += 1
        ##### --- #####

        ##### --- Delete any tag 2 that is using this tag1 --- #####
        tag2s_deleted = 0
        tag2s = db.get_tag2s()
        for tag2 in tag2s:
            if tag2[1] == tag1:
                db.delete_tag2(tag2[0])
                tag2s_deleted += 1
        ##### --- #####

        ##### --- Delete Tag1 --- #####
        db.delete_tag1(tag1_id)
        ##### --- #####

        alert = AlertMessage(self, "Deleted Tag 1", "Successfully deleted Tag 1", f'Tag 1: {tag1}', f' Tag 2s Deleted: {tag2s_deleted}\n Keyword Rules Deleted: {keyword_rules_deleted}')
        alert.finished.connect(show_Tags) 
        alert.exec_()
            
class MoveFiles_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movefiles = UI_MoveFiles()
        self.movefiles.setupUi(self)
        self.setAcceptDrops(True)

        #Buttons
        self.movefiles.pushButton_Home.clicked.connect(lambda: show_dashboard("Auto"))
        self.movefiles.pushButton_MoveToTable.clicked.connect(self.move_to_table)
        self.movefiles.pushButton_MoveFiles.clicked.connect(self.move_files)
        self.movefiles.pushButton_MoveFiles.setEnabled(False)

        #ListBox
        self.movefiles.listWidget_DropFiles.setAcceptDrops(True)

    def move_to_table(self):
        count = self.movefiles.listWidget_DropFiles.count()
        if count != 0:
            self.movefiles.tableWidget_files.setColumnCount(4)
            self.movefiles.tableWidget_files.setHorizontalHeaderLabels(["Orginal Path", "File Name", "Account", "New Path"])
            self.movefiles.tableWidget_files.setRowCount(count)
            
            for i in range(count):
                original_path = self.movefiles.listWidget_DropFiles.item(i).text()
                fname = str(os.path.basename(original_path))
                self.movefiles.tableWidget_files.setItem(i, 0, qtw.QTableWidgetItem(original_path))
                self.movefiles.tableWidget_files.setItem(i, 1, qtw.QTableWidgetItem(fname))
                combo4 = ComboTag4(self, f"{i}_{2}", "--")
                self.movefiles.tableWidget_files.setCellWidget(i, 2, combo4)

        self.movefiles.listWidget_DropFiles.clear()
        self.movefiles.pushButton_MoveFiles.setEnabled(True)

    def move_files(self):
        row_count = self.movefiles.tableWidget_files.rowCount()
        check = True
        for i in range(row_count):
            original_path = self.movefiles.tableWidget_files.item(i, 0).text()
            new_path = self.movefiles.tableWidget_files.item(i, 3).text()
            status = fm.move_files_for_import(original_path, new_path)
            if status != True:
                check = False
        if check == True:
            alert = AlertMessage(self, "File Move Status", "Successfully moved files, ready for import", "", "")
            alert.exec_()
            
        else:
            alert = AlertMessage(self, "File Move Status", "Failed to move all files, please review", "", "")
            alert.exec_()

        self.movefiles.tableWidget_files.clear()
        self.movefiles.pushButton_MoveFiles.setEnabled(False)
            

    #https://www.youtube.com/watch?v=KVEIW2htw0A&t=558s - Tutorial for drag/drop stuff 
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(qtc.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(qtc.Qt.CopyAction)
            event.accept()
            check_ftypes = True
            files = []
            bad_files = []
            #print(event.mimeData().urls())
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    fpath = str(url.toLocalFile())
                    ftype = fpath[-3:].upper()
                    if ftype == "CSV":
                        files.append(fpath)
                    else:
                        bad_files.append(fpath)
                        check_ftypes = False
            if check_ftypes == True:
                for i in files:
                    self.movefiles.listWidget_DropFiles.addItem(i)
            else:
                error_files = ""
                for i in bad_files:
                    error_files += (f"{os.path.basename(i)}\n")
                alert = AlertMessage(self, "File Type Error", f"{len(bad_files)} Files have the incorrect file typer", "", error_files)
                alert.exec_()
            
class AddTag1_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addtag1 = UI_AddTag1()
        self.addtag1.setupUi(self)

        #Init
        self.addtag1.label_ColorCode.setText("SELECT COLOR")

        #Buttons
        self.addtag1.pushButton_Cancel.clicked.connect(show_Tags)
        self.addtag1.pushButton_ColorPicker.clicked.connect(self.pick_color)
        self.addtag1.pushButton_SaveTag.clicked.connect(self.save_tag)

        #Radio Buttons
        self.addtag1.radioButton_VisibleEnabled.setChecked(True)
        self.addtag1.radioButton_VisibleDisabled.setChecked(False)
        self.addtag1.radioButton_CalcEnabled.setChecked(True)
        self.addtag1.radioButton_CalcDisabled.setChecked(False)
        
        self.addtag1.radioButton_VisibleEnabled.clicked.connect(self.radio_visibleEnabled)
        self.addtag1.radioButton_VisibleDisabled.clicked.connect(self.radio_visibleDisabled)
        self.addtag1.radioButton_CalcEnabled.clicked.connect(self.radio_calcEnabled)
        self.addtag1.radioButton_CalcDisabled.clicked.connect(self.radio_calcDisabled)


    def pick_color(self):
        color = QColorDialog.getColor()
        self.addtag1.label_ColorCode.setText(color.name())
        self.addtag1.label_ColorCode.setStyleSheet(f"background-color: {color.name()}")

    def save_tag(self):
        tag_name_check = True
        budget_check = True
        color_picker_check = True
        error_text = ""

        ##### --- Check Tag Name --- #####
        tag_name = self.addtag1.lineEdit_TagName.text()
        if len(tag_name) == 0:
            tag_name_check = False
            error_text += "\n - Tag name Required"

        if tag_name.upper() == "NA" or tag_name == "--":
            tag_name_check = False
            error_text += "\n - Tag name cannot be NA or --"
        ##### --- #####

        ##### --- Check that Tag 1 does not already exist --- #####
        tag_data = db.get_tag1s()
        if tag_data != False:
            for tag in tag_data:
                if tag_name == tag[1]:
                    tag_name_check = False
                    error_text += "\n - Tag already exists in database"
        ##### --- #####

        ##### --- Check Budget Amount --- #####
        try:
            tag_budget = float(self.addtag1.lineEdit_Budget.text())
        except:
            budget_check = False
            error_text += "\n - Budget must be a positive numeric value"
        ##### --- #####

        ##### --- Check Color Code --- #####
        color_code = self.addtag1.label_ColorCode.text()
        if color_code == "SELECT COLOR":
            color_picker_check = False
            error_text += "\n - Required to select a color assignment for tag"
        ##### --- #####

        ##### --- Get Radio Button - Visible --- #####
        visible = self.addtag1.radioButton_VisibleEnabled.isChecked()
        if visible  == True:
            visible_text = "True"
        else:
            visible_text = "False"
        ##### --- #####

        ##### --- Get Radio Button - Calc --- #####
        calc = self.addtag1.radioButton_CalcEnabled.isChecked()
        if calc == True:
            calc_text = "True"
        else:
            calc_text = "False"
        ##### --- #####
        
        ##### --- Check and save Expense --- #####
        if tag_name_check == True and budget_check == True and color_picker_check == True:
            communicate("AddTag1_Widget",f'Saving Tag: {tag_name}, {tag_budget}, {color_code}, {visible_text}, {calc_text}' )
            db.add_tag1(tag_name, tag_budget, color_code, visible_text, calc_text)
            show_Tags()
        else:
            alert = AlertMessage(self, "Issue with Nameing of Tags", "One or more fields are invalide, see below:", error_text, "")
            alert.exec_()
        ##### --- #####

    def radio_visibleEnabled(self):
        if self.addtag1.radioButton_VisibleEnabled.isChecked() == True:
            self.addtag1.radioButton_VisibleDisabled.setChecked(False)
        else:
            self.addtag1.radioButton_VisibleDisabled.setChecked(True)
    def radio_visibleDisabled(self):
        if self.addtag1.radioButton_VisibleDisabled.isChecked() == True:
            self.addtag1.radioButton_VisibleEnabled.setChecked(False)
        else:
            self.addtag1.radioButton_VisibleEnabled.setChecked(True)

    def radio_calcEnabled(self):
        if self.addtag1.radioButton_CalcEnabled.isChecked() == True:
            self.addtag1.radioButton_CalcDisabled.setChecked(False)
        else:
            self.addtag1.radioButton_CalcDisabled.setChecked(True)
    def radio_calcDisabled(self):
        if self.addtag1.radioButton_CalcDisabled.isChecked() == True:
            self.addtag1.radioButton_CalcEnabled.setChecked(False)
        else:
            self.addtag1.radioButton_CalcEnabled.setChecked(True)

class AddTag2_Widget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addtag2 = UI_AddTag2()
        self.addtag2.setupUi(self)

        ##### --- Buttons --- #####
        self.addtag2.pushButton_Cancel.clicked.connect(show_Tags)
        self.addtag2.pushButton_SaveTag.clicked.connect(self.save_tag)
        ##### --- #####

        ##### --- Add Tag 1 Items to Tag 1 Combo Box --- #####
        tags1 = db.get_tag1s()
        if tags1 != False:
            for i in tags1:
                self.addtag2.comboBox_Tag1.addItem(i[1])
        ##### --- #####

    def save_tag(self):
        tag2_name_check = True
        tag1_name = self.addtag2.comboBox_Tag1.currentText()
        tag2_name = self.addtag2.lineEdit_Tag2Name.text()
        error_text = ""

        ##### --- Check Tag2 Name --- #####
        if len(tag2_name) == 0:
            tag2_name_check = False
            error_text += "\n - Tag name Required"

        if tag2_name.upper() == "NA" or tag2_name == "--":
            tag2_name_check = False
            error_text += "\n - Tag name cannot be NA or --"
        ##### --- #####
        
        ##### --- Check that Tag 2 does not already exists --- #####
        tag2_data = db.get_tag2s()
        if tag2_data != False:
            for tag2 in tag2_data:
                if tag2_name == tag2[2]:
                    if tag1_name == tag2[1]:
                        tag2_name_check = False
                        error_text += "\n - Tag already exists in database"
        ##### --- #####
        
        ##### --- Check tag and save --- #####
        if tag2_name_check == True:
            communicate("AddTag2_Widget", f"Adding Tag2. Tag1: {tag1_name}, Tag2: {tag2_name}")
            db.add_tag2(tag1_name, tag2_name)
            show_Tags()
        else:
            alert = AlertMessage(self, "Issue with Nameing of Tags", "One or more fields are invalide, see below:", error_text, "")
            alert.exec_()
        ##### --- #####

class EditTag1_Widget(qtw.QWidget):
    def __init__(self,current_text):
        super().__init__()
        self.edittag1 = UI_EditTag1()
        self.edittag1.setupUi(self)

        ##### --- Buttons --- #####
        self.edittag1.pushButton_SaveTag.clicked.connect(self.save_tag)
        self.edittag1.pushButton_Cancel.clicked.connect(show_Tags)
        self.edittag1.pushButton_ColorPicker.clicked.connect(self.pick_color)
        ##### --- #####

        ##### --- Radio Buttons --- #####
        self.edittag1.radioButton_VisibleEnabled.clicked.connect(self.radio_visibleEnabled)
        self.edittag1.radioButton_VisibleDisabled.clicked.connect(self.radio_visibleDisabled)
        self.edittag1.radioButton_CalcEnabled.clicked.connect(self.radio_calcEnabled)
        self.edittag1.radioButton_CalcDisabled.clicked.connect(self.radio_calcDisabled)
        ##### --- #####

        ##### --- Update the Tag 1 to what the user selected --- #####
        self.edittag1.lineEdit_TagName.setText(current_text)
        self.edittag1.lineEdit_TagName.setDisabled(True)
        ##### --- #####
        
        ##### --- Set all of the options to what is currently set for the Tag 1 selected --- #####
        tags1 = db.get_tag1s()
        if tags1 != False:
            for i in tags1:
                if i[1] == current_text:
                    self.edittag1.label_ColorCode.setText(i[3])
                    self.edittag1.label_ColorCode.setStyleSheet(f"background-color: {i[3]}")

                    self.edittag1.label_TagID_Value.setText(str(i[0]))
                    self.edittag1.lineEdit_Budget.setText(str(i[2]))
                    
                    if i[4] == "True":
                        self.edittag1.radioButton_VisibleEnabled.setChecked(True)
                        self.edittag1.radioButton_VisibleDisabled.setChecked(False)
                    else:
                        self.edittag1.radioButton_VisibleEnabled.setChecked(False)
                        self.edittag1.radioButton_VisibleDisabled.setChecked(True)

                    if i[5] == "True":
                        self.edittag1.radioButton_CalcEnabled.setChecked(True)
                        self.edittag1.radioButton_CalcDisabled.setChecked(False)
                    else:
                        self.edittag1.radioButton_CalcEnabled.setChecked(False)
                        self.edittag1.radioButton_CalcDisabled.setChecked(True)
        ##### --- #####

    def radio_visibleEnabled(self):
        if self.edittag1.radioButton_VisibleEnabled.isChecked() == True:
            self.edittag1.radioButton_VisibleDisabled.setChecked(False)
        else:
            self.edittag1.radioButton_VisibleDisabled.setChecked(True)
    def radio_visibleDisabled(self):
        if self.edittag1.radioButton_VisibleDisabled.isChecked() == True:
            self.edittag1.radioButton_VisibleEnabled.setChecked(False)
        else:
            self.edittag1.radioButton_VisibleEnabled.setChecked(True)

    def radio_calcEnabled(self):
        if self.edittag1.radioButton_CalcEnabled.isChecked() == True:
            self.edittag1.radioButton_CalcDisabled.setChecked(False)
        else:
            self.edittag1.radioButton_CalcDisabled.setChecked(True)
    def radio_calcDisabled(self):
        if self.edittag1.radioButton_CalcDisabled.isChecked() == True:
            self.edittag1.radioButton_CalcEnabled.setChecked(False)
        else:
            self.edittag1.radioButton_CalcEnabled.setChecked(True)

    def save_tag(self):
        tag_name_check = True
        budget_check = True
        color_picker_check = True

        ##### --- Get Tag ID --- #####
        tag_id = int(self.edittag1.label_TagID_Value.text())
        ##### --- #####

        ##### --- Get Tag Name --- #####
        tag_name = self.edittag1.lineEdit_TagName.text()
        if len(tag_name) == 0:
            tag_name_check = False
        ##### --- #####

        ##### --- Check Budget Amount --- #####
        try:
            tag_budget = float(self.edittag1.lineEdit_Budget.text())
        except:
            budget_check = False
        ##### --- #####

        ##### --- Check Color Code --- #####
        color_code = self.edittag1.label_ColorCode.text()
        if color_code == "SELECT COLOR":
            color_picker_check = False
        ##### --- #####

        ##### --- Get Radio Button - Visible --- #####
        visible = self.edittag1.radioButton_VisibleEnabled.isChecked()
        if visible  == True:
            visible_text = "True"
        else:
            visible_text = "False"
        ##### --- #####

        ##### --- Get Radio Button - Calc --- #####
        calc = self.edittag1.radioButton_CalcEnabled.isChecked()
        if calc == True:
            calc_text = "True"
        else:
            calc_text = "False"
        ##### --- #####
        
        ##### --- Check settings and save --- #####
        if tag_name_check == True and budget_check == True and color_picker_check == True:
            communicate("EditTag1_Widget", f'Updating Tag: {tag_id}, {tag_name}, {tag_budget}, {color_code}, {visible_text}, {calc_text}')
            db.update_tag1(tag_id, tag_name, tag_budget, color_code, visible_text, calc_text)
            show_Tags()
        else:
            print("Issues with inputs")
            alert = AlertMessage(self, "Issue with Tag 1 settings", "One or more fields are invalide, see below:", "Check that budget is set to a number value with no symbols (ex: do not include a $)", "")
            alert.exec_()
        ##### --- #####

    def pick_color(self):
        color = QColorDialog.getColor()
        self.edittag1.label_ColorCode.setText(color.name())
        self.edittag1.label_ColorCode.setStyleSheet(f"background-color: {color.name()}")

#Link used: https://www.youtube.com/watch?v=KMJTJNUzo4E&t=90s
class ComboTag1(QComboBox):
    def __init__(self, parent, name, value, tags1, preset, tags2):
        super().__init__(parent)
        self.objectName = name
        self.setStyleSheet('Font-size: 15px')

        tag1_names, self.tag1_colors, tag2_names = self.get_tag_names(tags1, tags2)

        self.location = self.objectName.split("_")
        self.table_widget = self.parentWidget().parentWidget().findChild(qtw.QTableWidget, "tableWidget_Expenses")
        #print(self.table_widget.objectName())
        self.combo2_widget = self.table_widget.cellWidget(int(self.location[0]), int(self.location[1])+1)

        #Get Tag 2 information
        if tags2 != False:
            self.tag_2_clean = []
            for i in tags2:
                tag = []
                tag1_name = i[1]
                tag.append(tag1_name)
                for x in tags2:
                    if x[1] == tag1_name:
                        tag.append(x[2])
                self.tag_2_clean.append(tag)
        
        count = 0
        for i in tag1_names:
            self.addItem(i,tag2_names[count])
            count+=1
        
            
        if preset == True:
            self.setCurrentText(value)
            self.addItem("NA", ["NA"])
            ##### --- Set Tag 2 Combo --- #####

            ##### --- #####
            for i in self.tag1_colors:
                if i[0] == self.currentText():
                    for x in range(24):
                        if x != 21 and x != 22 and x != 23 and x!= 10:
                            #IF X does not equal any of the combo box columns
                            self.table_widget.item(int(self.location[0]), x).setBackground(QtGui.QColor(i[1]))
                    
                    
        else:
            self.addItem("NA", ["NA"])
            self.setCurrentText("NA")
    
        self.currentIndexChanged.connect(self.getCombo_row)

    def getCombo_row(self, tag1_colors):
        location = self.objectName.split("_")
        table_widget = self.parentWidget().parentWidget()
        combo2_widget = table_widget.cellWidget(int(location[0]), int(location[1])+1)
        if isinstance(combo2_widget, QComboBox):
            current_index = self.currentIndex()
            combo2_widget.clear()
            combo2_widget.addItems(self.itemData(int(current_index)))

            ### --- Add in -- to the tag 2 options, let the user assign it to just the tag 1 --- ###
            if combo2_widget.findText("--") == -1:
                combo2_widget.addItem("--")
            ### --- ###
            for i in self.tag1_colors:
                if i[0] == self.currentText():
                    for col in range(25):
                        if col != 10 and col != 21 and col != 22 and col != 23:
                            table_widget.item(int(location[0]), col).setBackground(QtGui.QColor(i[1]))
                    
                elif self.currentText() == "NA":
                    ### - "#FFFFFF" = White
                    for col in range(25):
                        if col != 10 and col != 21 and col != 22 and col != 23:
                            table_widget.item(int(location[0]), col).setBackground(QtGui.QColor("#FFFFFF"))

            
           
        else:
            print("issue")
    
    def get_tag_names(self, tags1, tags2):
        tag1_names = []
        tag1_colors = []
        for i in tags1:
            if i[4] == "True":
                tag1_names.append(i[1])
                tag1_colors.append([i[1],i[3]])

        tag2_names = []
        if tags2 != False:
            for tag1 in tag1_names:
                tag2_holder = []
                check = False
                for tag2 in tags2:
                    if tag2[1] == tag1:
                        tag2_holder.append(tag2[2])
                        check = True
                if check == True:
                    tag2_names.append(tag2_holder)
                else:
                    tag2_names.append(["--"])
        else:
            for i in tags1:
                tag2_names.append(["--"])
        return tag1_names, tag1_colors, tag2_names
        
#Link used: https://www.youtube.com/watch?v=KMJTJNUzo4E&t=90s
class ComboTag2(QComboBox):
    def __init__(self, parent, name, value, tag1, tags2):
        super().__init__(parent)
        self.setStyleSheet('Font-size: 15px')
        self.addItem(value)
        self.objectName = name

        if tag1 != "NA":
            for tag2 in tags2:
                if tag2[1] == tag1:
                    ### --- Remove the item adden on definition to replace it with the correct order of tag 2s
                    if tag2[2] == value:
                        self.removeItem(0)
                    ### --- ###
                    self.addItem(tag2[2])
            ### --- Add in -- to the items to let the user assign the expense to only the tag 1 --- ###
            if self.findText('--') == -1:
                self.addItem("--")
            ### --- ###
            self.setCurrentText(value)

class ComboTag3(QComboBox):
    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.setStyleSheet('Font-size: 15px')
        self.addItem(value)
        self.objectName = name

        if value == "Unlocked":
            self.addItem("Lock")
        else:
            self.addItem("Unlocked")

class ComboTag4(QComboBox):
    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.setStyleSheet('Font-size: 15px')
        self.addItem(value)
        self.objectName = name
        

        self.location = self.objectName.split("_")
        #self.table_widget = self.parentWidget().parentWidget().findChild(qtw.QTableWidget, "tableWidget_Files")
        self.table_widget = self.parentWidget().findChild(qtw.QTableWidget, "tableWidget_files")
        self.currentIndexChanged.connect(self.update_new_path)

        #Add Accounts to drop down
        for i in db.accounts:
            self.addItem(i[1])

    def update_new_path(self):
        account = self.currentText()
        print(f"{self.location[0]}, {self.location[1]}")
        print(self.table_widget.rowCount())
        row = int(self.location[0])
        fname = self.table_widget.item(row, 1).text()
        new_path = (f"Accounts/{account}/{fname}")
        self.table_widget.setItem(int(self.location[0]), 3, qtw.QTableWidgetItem(new_path))

class ComboTag5(QComboBox):
    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.objectName = name

        self.addItems(["--", "Enabled"])

        self.setCurrentText(value)

        self.table_widget = self.parentWidget().parentWidget().findChild(qtw.QTableWidget, "tableWidget_Expenses")

        self.location = self.objectName.split("_")

        if value == "--":
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(1)

        self.currentIndexChanged.connect(self.show_calendar_widget)

    def show_calendar_widget(self):
        if self.currentText() == "Enabled":
            dialog = CalendarDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                selected_date = dialog.calendar.selectedDate().toString(qtc.Qt.ISODate)
                selected_date_object = datetime.strptime(selected_date, "%Y-%m-%d")
                month_selected = str(int(selected_date_object.month))
                day_selected = str(int(selected_date_object.day))
                year_selected = str(int(selected_date_object.year))

                row = int(self.location[1])
                col = int(self.location[2])

                month_item = qtw.QTableWidgetItem(month_selected)
                day_item = qtw.QTableWidgetItem(day_selected)
                year_item = qtw.QTableWidgetItem(year_selected)
                date_item = qtw.QTableWidgetItem(selected_date_object.strftime("%m/%d/%Y"))
                
                
                
                self.table_widget.setItem(row, col+1, month_item)
                self.table_widget.setItem(row, col+2, day_item)
                self.table_widget.setItem(row, col+3, year_item)
                self.table_widget.setItem(row, col+4, date_item)
        else:
            month_item = qtw.QTableWidgetItem("--")
            day_item = qtw.QTableWidgetItem("--")
            year_item = qtw.QTableWidgetItem("--")
            date_item = qtw.QTableWidgetItem("--")
            row = int(self.location[1])
            col = int(self.location[2])
            self.table_widget.setItem(row, col+1, month_item)
            self.table_widget.setItem(row, col+2, day_item)
            self.table_widget.setItem(row, col+3, year_item)
            self.table_widget.setItem(row, col+4, date_item)

class ComboBillsEnable(QComboBox):
    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.objectName = name

        self.addItems(["Enabled", "Disabled"])

        self.setCurrentText(value)

        self.table_widget = self.parentWidget().findChild(qtw.QTableWidget, "tableWidget_Bills")

        self.location = self.objectName.split("_")

        self.currentIndexChanged.connect(self.save_setting)
    
    def save_setting(self):
        bill_id = int(self.table_widget.item(int(self.location[0]),0).text())
        db.update_bill(bill_id, self.currentText())
        show_Bills()
        
class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a Date")
        self.resize(400,400)

        #Create calendar Widget
        self.calendar = qtw.QCalendarWidget()
        self.selected_date_label = qtw.QLabel("Double-Click a date to select")

        #Layout
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.selected_date_label)
        layout.addWidget(self.calendar)
        self.setLayout(layout)

        #Connect the double click signal
        self.calendar.activated.connect(self.date_selected)

    def date_selected(self, date):
        self.selected_date_label.setText(f'Selected Date: {date.toString(qtc.Qt.ISODate)}')
        self.accept()

class AlertMessage(QMessageBox):
    def __init__(self, parent, title, text, informative_text, detailed_text):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)
        self.setText(text)
        if informative_text != False:
            self.setInformativeText(informative_text)
        if detailed_text != False:
            self.setDetailedText(detailed_text)
        self.setStandardButtons(QMessageBox.Ok)

class Matplotlib_Widget(qtw.QWidget):
    def __init__(self, parent, tags, colors, values, title):
        super().__init__(parent)
        self.figure = Figure(facecolor="black")
        self.canvas = FigureCanvas(self.figure)
        layout = qtw.QVBoxLayout()
        self.title_text = title
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_example(tags, colors, values)

    def plot_example(self, tags, colors, values):
        ax = self.figure.add_subplot(111)
        categories = tags
        values_new = []
        for value in values:
            v = round(value,2)
            values_new.append(v)
        
        # Customize backgrounds and labels
        ax.set_facecolor('black')  # Chart area background
        bars = ax.bar(categories, values_new, color=colors)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # X-coordinate (center of the bar)
                height,  # Y-coordinate (top of the bar)
                f'$ {height}',  # Text to display
                ha='center',  # Horizontal alignment
                va='bottom',  # Vertical alignment
                color='white',  # Text color
                fontsize=7  # Text size
            )

        # Customizing labels and title
        ax.set_title(self.title_text, color='white')
        ax.tick_params(axis='x', colors='white', labelsize = 7)
        ax.tick_params(axis='y', colors='white')
        ax.set_xticks(categories)
        ax.set_xticklabels(categories, rotation=45, ha='right', color='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        self.canvas.draw()

def show_dashboard(month_choice, year = y, side_bar = True):
    if month_choice == "Auto":
        widget = Dashboard_Widget(int(m), int(y), side_bar)
        window.setCentralWidget(widget)
    else:
        widget = Dashboard_Widget(int(month_choice), int(year), side_bar)
        window.setCentralWidget(widget)
    
def show_accounts():
    widget = Accounts_Widget()
    window.setCentralWidget(widget)

def show_Bills():
    widget = Bills_Widget()
    window.setCentralWidget(widget)
def show_BillsAdd():
    widget = BillsAdd_Widget()
    window.setCentralWidget(widget)

def show_NewAccount():
    widget = NewAccount_Widget()
    window.setCentralWidget(widget)

def show_AccountsConfig():
    widget = AccountsConfig_Widget()
    window.setCentralWidget(widget)

def show_ImportManager():
    widget = ImportManager_Widget()
    window.setCentralWidget(widget)

def show_TagManager():
    widget = TagManager_Widget()
    window.setCentralWidget(widget)

def show_Settings():
    widget = Settings_Widget()
    window.setCentralWidget(widget)

def show_ApplicationSettings():
    widget = ApplicationSettings_Widget()
    window.setCentralWidget(widget)

def show_Developer_Details():
    widget = DevloperDetails_Widget()
    window.setCentralWidget(widget)

def show_Tags():
    widget = Tags_Widget()
    window.setCentralWidget(widget)

def show_DeleteTag1():
    widget = DeleteTag1_Widget()
    window.setCentralWidget(widget)

def show_MoveFiles():
    widget = MoveFiles_Widget()
    window.setCentralWidget(widget)

def show_AddTag1():
    widget = AddTag1_Widget()
    window.setCentralWidget(widget)

def show_AddTag2():
    widget = AddTag2_Widget()
    window.setCentralWidget(widget)
    
def show_EditTag1(current_text):
    widget = EditTag1_Widget(current_text)
    window.setCentralWidget(widget)

def show_KeywordTagging():
    widget = KeywordTagging_Widget()
    window.setCentralWidget(widget)

def show_AddKeywordRule():
    widget = AddKeywordRule_Widget()
    window.setCentralWidget(widget)

def show_EditKeywordRule(id):
    widget = EditKeywordRule_Widget(id)
    window.setCentralWidget(widget)

def show_TagsConvert():
    widget = TagsConvert_Widget()
    window.setCentralWidget(widget)

def communicate(function, text):
    """
    Function prints out a text statement into the terminal for logging purposes.

    :Parameters:
    - function/class (string) = "Dashboard_Widget"
    - text (string) = "Print this text"

    :Example: Communicate:
    >>> communicate("Dashboard_widget", "Print this text as example")
    [APP]/[Dashboard_Widget]...Print this text as example
    """
    new_text = f'[APP]/{function}...{text}'
    print(new_text)

def show_Analytics(year_selection):
    widget = Analytics_Widget(year_selection)
    print(year_selection)
    window.setCentralWidget(widget)


if __name__ == "__main__":

    ##### --- Connect to Database and File Managaer --- #####
    db = database()
    fm = File_Manager()
    ##### --- #####

    
    application_settings = db.get_application_settings()
    setting_1 = application_settings[1] #Start Up Process Boolean
    setting_2 = application_settings[2] #Application Version


    if setting_1 == "True":
        start_up = True
    else: start_up = False
    if start_up: 
        proceed = StartUp()

    ### --- Added for macOS integration --- ###
    import os
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
    ### --- ###


    app = qtw.QApplication([])

    ### --- Added for macOs --- ###
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(palette.Window, QColor(240, 240, 240))
    palette.setColor(palette.WindowText, qtc.Qt.black)
    palette.setColor(palette.Base, qtc.Qt.white)
    palette.setColor(palette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(palette.Text, qtc.Qt.black)
    palette.setColor(palette.Button, QColor(240, 240, 240))
    palette.setColor(palette.ButtonText, qtc.Qt.black)
    app.setPalette(palette)
    ### --- ###


    window = MainWindow()
    window.show()

    show_dashboard("Auto")

    app.exec_()



