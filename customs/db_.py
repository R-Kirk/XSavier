import sqlite3
from datetime import date, timedelta
from os.path import exists
today_ = date.today()
d_ = today_.strftime("%d")
m_ = today_.strftime("%m")
y_ = today_.strftime("%Y")


#Define Application Version
version = "2.0"

class database():
    def __init__(self, *args, **kwargs):
        check_for_database_existance= ''
        if not exists('database.db'):
            check_for_database_existance = False
        
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.communicate("Connected to Database")

        if check_for_database_existance == False:
            self.communicate("New User")
            self.create_tables()
        else:
            self.communicate("Returning User")
        self.get_accounts()
    
    def create_tables(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS Accounts (
            id integer PRIMARY KEY,
            Account_Name text,
            Account_Type text,
            TransDate_Col integer, 
            PostedDate_Col integer, 
            Desc_Col integer, 
            Amt1_Col integer, 
            Sign1_Col text, 
            Amt2_Col integer, 
            Sign2_Col text)""")
        
        self.c.execute("""CREATE TABLE IF NOT EXISTS Expense_Tags1 (
            id integer PRIMARY KEY,
            Tag text,
            Budget Real,
            color text,
            visible text, 
            calc text)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS Expense_Tags2 (
            id integer PRIMARY KEY,
            Tag1 text,
            Tag2 text)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS Expenses (
                id integer PRIMARY KEY,
                Account text,  
                MonthTrans text,
                DayTrans text,
                YearTrans text,         
                TransDate text,
                MonthPosted text,
                DayPosted text,
                YearPosted text,         
                PostedDate text,
                DateOverrideBool text,
                OvrMonth text,
                OvrDay text,
                OvrYear text,
                OvrDate text,
                MonthCalc text,
                DayCalc text,
                YearCalc text,         
                CalcDate text,
                Description text, 
                Amount Real, 
                Tag1 text, 
                Tag2 text,
                Lock text,
                Note text)""")
        
        self.c.execute(""" CREATE TABLE IF NOT EXISTS Import_Notes (
                       id integer PRIMARY KEY,
                       Notes text)
                       """)
        
        self.c.execute("""SELECT MAX(id) From Import_Notes""")
        max_id = self.c.fetchone()[0]
        if max_id == None:
            self.c.execute("""INSERT OR REPLACE INTO Import_Notes Values (?, ?) """, [1, "--"])


        self.c.execute(""" CREATE TABLE IF NOT EXISTS Application_Settings (  
            id integer PRIMARY KEY, 
            StartUp_Process text, 
            Application_Version text)""")
        
        self.c.execute("""SELECT MAX(id) From Application_Settings""")
        max_id = self.c.fetchone()[0]
        if max_id == None:
            self.c.execute("INSERT INTO Application_Settings VALUES (?, ?, ?, ?)", [1, "True", version, "True"])
        else:
            self.c.execute("SELECT * From Application_Settings WHERE id = (?)", [1])
            settings = self.c.fetchall()[0]
            if settings[2] != version:
                self.c.execute("INSERT OR REPLACE INTO Application_Settings VALUES (?, ?, ?)", [settings[0], settings[1],version, settings[3]])
                self.communicate("Updated Application Version")

        ###### --- Insert new table for keyword tagging definitions here --- ###
        self.c.execute("""CREATE TABLE IF NOT EXISTS KeywordTagging (
            id integer PRIMARY KEY,
            Keyword text,  
            Tag_1 text,
            Tag_2 text)""")
        

        self.c.execute("ALTER TABLE Application_Settings ADD COLUMN BarChartShowZeros text")
        self.conn.commit()
        
        self.communicate("Created Tables")
   
    def get_accounts(self):
        self.c.execute("""SELECT MAX(id) From Accounts""")
        
        max_id = self.c.fetchone()[0]
        if max_id == None:
            self.accounts = [["NA", "NA", "NA","NA", "NA", "NA","NA", "NA", "NA"]]
        else:
            self.c.execute("""SELECT * From Accounts""")
            self.accounts = self.c.fetchall() 
    
    def get_expenses(self, mode, month_1, year_1, month_2, year_2, tag1 = "*", account = "*"):
        if mode == "Show All":
            self.c.execute("""SELECT MAX(id) From Accounts""")
            max_id = self.c.fetchone()[0]
            if max_id == None:
                return False
            #Tag1 and Account Specific
            elif tag1 != "*" and account != "*":
                self.c.execute("""SELECT * From Expenses WHERE Account = ? and Tag1 = ?""", [account, tag1])
                expenses = self.c.fetchall()
                return expenses
            #Tag 1 only specific
            elif tag1 != "*" and account == "*":
                self.c.execute("""SELECT * From Expenses WHERE Tag1 = ?""", [tag1])
                expenses = self.c.fetchall()
                return expenses
            #Account only specific
            elif tag1 == "*" and account != "*":
                self.c.execute("""SELECT * From Expenses WHERE Account = ?""", [account])
                expenses = self.c.fetchall()
                return expenses
            else:
                self.c.execute("""SELECT * From Expenses""")
                expenses = self.c.fetchall()
                return expenses
            
        elif mode == "Month-Year":
            expenses = []
            self.c.execute("""SELECT MAX(id) From Accounts""")
            max_id = self.c.fetchone()[0]
            if max_id == None:
                return False
            
            ##### --- FILTER: Tag 1 & Account --- #####
            elif tag1 != "*" and account != "*":
                self.c.execute("""SELECT * From Expenses where MonthCalc = ? and YearCalc = ? and Account = ? and Tag1 = ?""",[month_1, year_1, account, tag1])
                expenses = self.c.fetchall()
            ##### --- #####
                
             ##### --- FILTER: Tag 1 ONLY --- #####
            elif tag1 != "*" and account == "*":
                self.c.execute("""SELECT * From Expenses WHERE MonthCalc = ? AND YearCalc = ? AND Tag1 = ?""",(month_1, year_1, tag1))
                expenses = self.c.fetchall()
            ##### --- #####

            ##### --- FILTER: Account ONLY --- #####
            elif tag1 == "*" and account != "*":
                self.c.execute("""SELECT * From Expenses where MonthCalc = ? and YearCalc = ? and Account = ?""",[month_1, year_1, account])
                expenses = self.c.fetchall() 
            ##### --- #####

            ##### --- FILTER: NO FILTER --- #####           
            else:
                self.c.execute("""SELECT * From Expenses where MonthCalc = ? and YearCalc = ?""", [month_1, year_1])
                expenses = self.c.fetchall()

                ##### -- GET OVERRIDDEN DATES for this month
                self.c.execute(""" SELECT * From Expenses WHERE MonthCalc = ? and YearCalc = ? OR OvrMonth = ? and OvrYear = ?""", [month_1, year_1, month_1, year_1])
                expenses = self.c.fetchall()
            ##### --- #####
                
            
            if expenses == []:
                return False
            else:
                return expenses
                
        elif mode == "Untagged":
            self.c.execute("""SELECT MAX(id) From Accounts""")
            max_id = self.c.fetchone()[0]
            if max_id == None:
                return False
            else:
                self.c.execute("""SELECT * From Expenses where Tag1 = ?""", ["NA"])
                expenses = self.c.fetchall()
                if expenses == []:
                    return False
                else:
                    return expenses        

    def get_expense_years(self):

        ##### --- CalcYears --- #####
        self.c.execute("SELECT YearCalc FROM Expenses")
        years = self.c.fetchall()
        calc_years = []
        calc_years_check = False
        if years != []:
            calc_years_check = True
            for year in years:
                calc_years.append(year[0])
        ##### --- #####

        ##### --- Override Years --- #####
        self.c.execute("SELECT OvrYear FROM Expenses")
        years = self.c.fetchall()
        ovr_years = []
        ovr_years_check = False
        if years != []:
            ovr_years_check = True
            for year in years:
                ovr_years.append(year[0])
        ##### --- #####

        ##### --- Remove duplicates from CalcYears --- #####
        uni_calc_years = []
        if calc_years_check == True:
            uni_calc_years = list(set(calc_years))
        ##### --- #####

        ##### --- Remove duplicate from OvrYears --- #####
        uni_ovr_years = []
        if ovr_years_check == True:
            uni_ovr_years = list(set(ovr_years))
        ##### --- #####
        
        ##### --- Combine both Calc Years and Override Years to List --- #####
        combined_years = []
        if calc_years_check:
            for year in uni_calc_years:
                combined_years.append(year)
        if ovr_years_check:
            for year in uni_ovr_years:
                combined_years.append(year)
        ##### --- #####
        
        ##### --- Remove duplicates from Combined Years --- #####
        uni_combined_years = []
        if combined_years != []:
            uni_combined_years = list(set(combined_years))
        else:
            uni_combined_years.append(y_)
        ##### --- #####

        ##### --- Remove unwanted characters froom combined years and add in current year and sort the list from highest to lowest --- #####
        if "--" in uni_combined_years:
            uni_combined_years.remove("--")
        if y_ not in uni_combined_years:
            uni_combined_years.append(y_)

        sorted_years = sorted(uni_combined_years, key=int, reverse=True)
        ##### --- #####

        return sorted_years




        

        ##### --- #####

    def get_tags_to_convert(self, tag1, tag2):
        self.c.execute("""SELECT id FROM Expenses where Tag1 = ? AND Tag2 = ?""", [tag1, tag2])
        ids = self.c.fetchall()

        if ids == []:
            return False
        else:
            return ids

    def get_expenses_year_to_date(self, year):
        self.c.execute(""" SELECT MAX(id) From Accounts """)
        max_id = self.c.fetchone()[0]
        if max_id == None:
            return False
        else:
            self.c.execute("""SELECT * From Expenses where YearCalc = ? OR OvrYear = ?""", [year, year])
            expenses = self.c.fetchall()

            if expenses == []:
                return False
            else:
                return expenses

    def get_tag1s(self):
        self.c.execute("""SELECT MAX(id) FROM Expense_Tags1""")
        max_id = self.c.fetchone()[0]

        if max_id == None:
            return False
        else:
            self.c.execute("""SELECT * FROM Expense_Tags1 """)
            Tags1 = self.c.fetchall()
            return Tags1
    
    def get_tag2s(self):
        self.c.execute("SELECT max(id) FROM Expense_Tags2")
        max_id = self.c.fetchone()[0]

        if max_id == None:
            return False
        else:
            self.c.execute("SELECT * FROM Expense_Tags2")
            Tags2 = self.c.fetchall()
            return Tags2
        
    def get_keywordrules(self):
        self.c.execute("SELECT max(id) FROM KeywordTagging")
        max_id = self.c.fetchone()[0]

        if max_id == None:
            return False
        else:
            self.c.execute("SELECT * FROM KeywordTagging")
            keyword_rules = self.c.fetchall()
            return keyword_rules
    
    def get_import_notes(self):
        self.c.execute("SELECT Notes FROM Import_NOTES WHERE id = ?", [1])
        import_notes = self.c.fetchone()[0]
        return import_notes   
    
    def get_application_settings(self):
        self.c.execute("SELECT * FROM Application_Settings WHERE id = ?", [1])
        application_settings = self.c.fetchall()[0]
        return application_settings        

    def add_account(self, account_name, account_type, trans_date_col, posted_date_col, desc_col, amt1_col, sign1_col, amt2_col,sign2_col):
        self.c.execute("SELECT MAX(id) from Accounts")
        max_id = self.c.fetchone()[0]

        if max_id == None:
            self.communicate("Created first Account")
            max_id = 1
            self.c.execute("INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [max_id, account_name, account_type, trans_date_col, posted_date_col, desc_col, amt1_col, sign1_col, amt2_col,sign2_col])
            self.conn.commit()
        else:
            self.c.execute("INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [max_id + 1,account_name, account_type, trans_date_col, posted_date_col, desc_col, amt1_col, sign1_col, amt2_col,sign2_col])
            self.conn.commit()
        self.get_accounts()

    def add_tag1(self, tag_name, budget, color, visible, calc):
        self.c.execute("SELECT MAX(id) from Expense_Tags1")
        max_id = self.c.fetchone()[0]

        if max_id == None:
            max_id = 1
            self.c.execute("INSERT INTO Expense_Tags1 VALUES (?, ?, ?, ?, ?, ?)", [max_id, tag_name, budget, color, visible, calc])
            self.conn.commit()
        else:
            self.c.execute("INSERT INTO Expense_Tags1 VALUES (?, ?, ?, ?, ?, ?)", [max_id+1, tag_name, budget, color, visible, calc])
            self.conn.commit()

    def add_tag2(self, tag1_name, tag2_name):
        self.c.execute("SELECT MAX(id) from Expense_Tags2")
        max_id = self.c.fetchone()[0]

        if max_id == None:
            max_id = 1
            self.c.execute("INSERT INTO Expense_Tags2 VALUES (?, ?, ?)", [max_id, tag1_name, tag2_name])
            self.conn.commit()
        else:
            self.c.execute("INSERT INTO Expense_Tags2 VALUES (?, ?, ?)", [max_id + 1, tag1_name, tag2_name])
            self.conn.commit()
    
    def add_keyword_rule(self, keyword, tag1, tag2):
        self.c.execute("SELECT MAX(id) from KeywordTagging")
        max_id = self.c.fetchone()[0]

        if max_id == None:
            max_id = 1
            self.c.execute("INSERT INTO KeywordTagging VALUES (?, ?, ?, ?)", [max_id, keyword, tag1, tag2])
            self.conn.commit()
        else:
            max_id += 1
            self.c.execute("INSERT INTO KeywordTagging VALUES (?, ?, ?, ?)", [max_id, keyword, tag1, tag2])
            self.conn.commit()

    def update_tag1(self, tag_id, tag_name, budget, color, visible, calc):
        self.c.execute("INSERT OR REPLACE INTO Expense_Tags1 VALUES (?, ?, ?, ?, ?, ?)", [tag_id, tag_name, budget, color, visible, calc])
        self.conn.commit()

    def update_keyword_rule(self, id, keyword, tag1, tag2):
        self.c.execute("INSERT OR REPLACE INTO KeywordTagging VALUES (?, ?, ?, ?)", [id, keyword, tag1, tag2])
        self.conn.commit()

    def update_account(self, id, account_name, account_type, trans_date_col, posted_date_col, desc_col, amt1_col, sign1_col, amt2_col, sign2_col):
        self.c.execute("INSERT OR REPLACE INTO Accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [id, account_name, account_type, trans_date_col,posted_date_col, desc_col, amt1_col, sign1_col, amt2_col,sign2_col])
        self.conn.commit()
        #Need to update the db.accounts variables after saving so the dashboard can see the updates
        self.get_accounts()
    
    def update_expenses(self, data):
        for i in data:
            id = i[0]
            Account = i[1]

            MonthTrans = i[2]
            DayTrans = i[3]
            YearTrans = i[4]
            TransDate = i[5]

            MonthPosted = i[6]
            DayPosted = i[7]
            YearPosted = i[8]
            PostedDate = i[9]

            OvrBoolean = i[10]
            OvrMonth = i[11]
            OvrDay = i[12]
            OvrYear = i[13]
            OvrDate = i[14]

            MonthCalc = i[15]
            DayCalc = i[16]
            YearCalc = i[17]
            CalcDate = i[18]

            
            Description = i[19]
            Amount = i[20]
            Tag1 = i[21]
            Tag2 = i[22]
            Lock = i[23]
            Note = i[24]

            self.c.execute("""UPDATE Expenses SET 
                           Account = ?, 
                           MonthTrans = ?, DayTrans = ?, YearTrans = ?, TransDate = ?, 
                           MonthPosted = ?, DayPosted = ?, YearPosted = ?, PostedDate = ?, 
                           DateOverrideBool = ?, OvrMonth =?, OvrDay = ?, OvrYear = ?, OvrDate = ?,
                           MonthCalc = ?, DayCalc = ?, YearCalc = ?, CalcDate = ?, 
                           Description = ?, Amount = ?, Tag1 = ?, Tag2 = ?, Lock = ?, Note = ? WHERE id = ?""", [Account, MonthTrans, DayTrans, YearTrans, TransDate, MonthPosted, DayPosted, YearPosted, PostedDate, OvrBoolean, OvrMonth, OvrDay, OvrYear, OvrDate, MonthCalc, DayCalc, YearCalc, CalcDate,  Description, Amount, Tag1, Tag2, Lock,Note, id])
        self.conn.commit()

    def convert_tags(self, ids, new_tags):
        count = 0
        for id in ids:
            self.c.execute("""UPDATE Expenses SET Tag1 = ?, Tag2 = ? WHERE id = ?;""", [new_tags[0], new_tags[1], id])
            count += 1

        self.conn.commit()
        self.communicate(f"Converted {count} Tags")

    def update_import_notes(self, text):
        try:
            self.c.execute("INSERT OR REPLACE INTO Import_Notes VALUES (?, ?)", [1, text])
            self.conn.commit()

            self.communicate("Updated Import Note")
            return True
        except:
            self.communicate("Failed to Update Import Note")
            return False
        
    def update_application_settings(self, settings):
        try:
            self.c.execute("INSERT OR REPLACE INTO Application_Settings VALUES (?, ?, ?, ?)", [settings[0], settings[1], version, settings[2]])
            self.conn.commit()

            self.communicate("Updated Application Settings")
            return True
        except:
            self.communicate("Failed to Update Application Settings")
            return False

    def delete_keyword_rule(self, id):
        self.c.execute("DELETE from KeywordTagging where id=(?)", [id])
        self.conn.commit()
    
    def delete_tag2(self, id):
        self.c.execute("DELETE from Expense_Tags2 where id=(?)", [id])
        self.conn.commit()
    
    def delete_tag1(self, id):
        self.c.execute("DELETE from Expense_Tags1 where id=(?)", [id])
        self.conn.commit()


    def import_expenses(self,account, month, year, data):
        self.communicate(f"Account: {account}")
        self.c.execute("SELECT id FROM Expenses WHERE MonthPosted = (?) AND YearPosted = (?) AND Account = (?) AND Lock = (?)", [str(month), str(year), str(account), "Unlocked"])
        delete_ids = self.c.fetchall()
        if delete_ids == []: self.communicate("NO EXPENSES IN DATABASE FOR THIS ACCOUNT AND DATE")
        else: 
            count = 0
            for i in delete_ids: 
                print(i[0])
                count +=1
                self.c.execute("DELETE FROM Expenses WHERE id = (?)", (i[0],))
            self.conn.commit()    
            self.communicate(f"Deleted {count} expenses")

        self.c.execute("SELECT MAX(id) from Expenses")
        max_id = self.c.fetchone()[0]
        self.communicate(f"MAX ID: {max_id}")
        count = 0
        
        if max_id == None:
            max_id = 1
            for i in data:
                count +=1
                i.insert(0, max_id)
                self.c.execute("INSERT OR REPLACE INTO Expenses VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?)", i)
                self.conn.commit()
                max_id +=1      
        else:
            max_id +=1
            for i in data:
                count +=1
                i.insert(0, max_id)
                self.c.execute("INSERT OR REPLACE INTO Expenses VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?)", i)
                self.conn.commit()
                max_id +=1
                
        self.communicate(f"Saved Expenses: {count} expenses saved")
      
    def communicate(self, text):
        print(f"[DATABASE]....{text}")
        