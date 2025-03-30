import sqlite3
from datetime import date, timedelta
from os.path import exists
today_ = date.today()
d_ = today_.strftime("%d")
m_ = today_.strftime("%m")
y_ = today_.strftime("%Y")


conn = sqlite3.connect("database.db")
c = conn.cursor()


def clean_expenses():
    c.execute("SELECT * from Expenses")
    expenses = c.fetchall()
    expenses_new = []
    for expense in expenses:
        id = expense[0]
        Account = expense[1]

        Monthtrans = "--"
        DayTrans = "--"
        YearTrans  = "--"       
        TransDate = "--"

        MonthPosted = expense[2]
        DayPosted = expense[3]
        YearPosted  = expense[4]        
        PostedDate = expense[5]

        MonthCalc = expense[2]
        DayCalc = expense[3]
        YearCalc  = expense[4]
        CalcDate = expense[5]

        DateOverrideBool = "--"

        MonthOvr = "--"
        DayOvr = "--"
        YearOvr  = "--"       
        OvrDate = "--"

        Description  = expense[6]
        Amount  = float(expense[7])
        Tag1  = expense[8]
        Tag2 = expense[9]
        Lock = expense[10]
        Note = ""

        expenses_new.append([
            id, 
            Account,
            Monthtrans,
            DayTrans,
            YearTrans,
            TransDate,
            MonthPosted,
            DayPosted,
            YearPosted,
            PostedDate,
            DateOverrideBool, 
            MonthOvr,
            DayOvr,
            YearOvr,
            OvrDate,
            MonthCalc,
            DayCalc,
            YearCalc,       
            CalcDate,
            Description,
            Amount,
            Tag1,
            Tag2,
            Lock,
            Note])

    # Create a new table with the desired column order
    c.execute("""CREATE TABLE IF NOT EXISTS ExpensesNew (
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
    conn.commit()


    for expense in expenses_new:
        c.execute("INSERT OR REPLACE into ExpensesNew Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?)", expense)
    conn.commit()

    # Drop the old table
    c.execute("DROP TABLE Expenses;")

    # Rename the new table to the old table's name
    c.execute("ALTER TABLE ExpensesNew RENAME TO Expenses;")
    conn.commit()

def clean_accounts():
    c.execute("SELECT * from Accounts")
    accounts = c.fetchall()
    accounts_new = []
    for account in accounts:
        id = account[0]
        Account_Name = account[1]
        Account_Type = account[2]
        TransDate_Col  = 420
        PostedDate_Col = account[3]
        Desc_Col = account[4]
        Amt1_Col = account[5]
        Sign1_Col = account[6]
        Amt2_Col = account[7]
        Sign2_Col = account[8]

        accounts_new.append([id, Account_Name, Account_Type, TransDate_Col, PostedDate_Col, Desc_Col, Amt1_Col, Sign1_Col, Amt2_Col, Sign2_Col])

    # Create a new table with the desired column order
    c.execute("""CREATE TABLE IF NOT EXISTS AccountsNew (
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
    conn.commit()


    for account in accounts_new:
        c.execute("INSERT OR REPLACE into AccountsNew Values (?,?,?,?,?,?,?,?,?,?)", account)
    conn.commit()

    # Drop the old table
    c.execute("DROP TABLE Accounts;")

    # Rename the new table to the old table's name
    c.execute("ALTER TABLE AccountsNew RENAME TO Accounts;")
    conn.commit()

if __name__ == "__main__":
    clean_expenses()
    clean_accounts()

    input("Completed")