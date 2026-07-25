import csv
from dateutil.parser import parse
from datetime import datetime
import pandas as pd

def get_data(file, Account, TransDateCol, PostedDateCol, DescCol, Amt1Col, Sign1, Amt2Col, Sign2):
    communicate(f"IMPORTING ACCOUNT: {Account} - FILE: {file}")

    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        #Skip the header row
        next(csv_reader)

        trans_date_data = []
        posted_date_data = []
        desc_data = []
        amt1_data = []
        amt2_data = []

        ##### --- Set Column Data to Integers
        if TransDateCol != 'Dont Need':
            TransDateCol = int(TransDateCol)
        PostedDateCol = int(PostedDateCol)
        DescCol = int(DescCol)
        Amt1Col = int(Amt1Col)
        if Amt2Col != "Dont Need":
            Amt2Col = int(Amt2Col)
        

        count = 1
        for line in csv_reader:
            if line!= []:
                count +=1

                if TransDateCol != "Dont Need":
                    trans_date_data.append(line[TransDateCol-1])

                posted_date_data.append(line[PostedDateCol-1])

                desc_data.append(line[DescCol-1])

                if len(line[Amt1Col-1]) == 0: 
                    amt1_data.append(float(0))
                else: amt1_data.append(line[Amt1Col-1])

                if Amt2Col != "Dont Need": 
                    ##### --- If there is not a value for Amount 2 in the current row, set equal to 0, else take the value
                    if len(line[Amt2Col-1]) == 0:
                        amt2_data.append(float(0))
                    else: 
                        amt2_data.append(float(line[Amt2Col-1]))
            else:
                count +=1

    ##### --- Verify if Trans dates are valid --- ####
    trans_date_data_1 = []
    trans_months = []
    trans_days = []
    trans_years = []
    
    trans_date_error_text = []

    if TransDateCol != "Dont Need":
        verify_trans_dates_data = verify_dates(trans_date_data, "Trans")
        if verify_trans_dates_data[0] != False:
            #[date_data_1, months, days, years, dates_verify]
            trans_date_data_1 = verify_trans_dates_data[0]
            trans_months = verify_trans_dates_data[1]
            trans_days = verify_trans_dates_data[2]
            trans_years = verify_trans_dates_data[3]
            trans_dates_verify = verify_trans_dates_data[4]
            trans_date_error_text = verify_trans_dates_data[5]
        else:
            #[False, dates_verify, date_error_text]
            trans_dates_verify = verify_trans_dates_data[1]
            trans_date_error_text = verify_trans_dates_data[2]
    else:
        for i in posted_date_data:
            trans_date_data_1.append("--")
            trans_months.append("--")
            trans_days.append("--")
            trans_years.append("--")
            trans_dates_verify = True
            trans_date_error_text = ["NO TRANSACTION DATE COLUMN FOR THIS ACCOUNT"]
    ##### --- #####
    
    ##### --- Verify if posted dates are valid --- ####

    verify_posted_dates_data = verify_dates(posted_date_data, "Posted")
    if verify_posted_dates_data[0] != False:
        #[date_data_1, months, days, years, dates_verify]
        posted_date_data_1 = verify_posted_dates_data[0]
        posted_months = verify_posted_dates_data[1]
        posted_days = verify_posted_dates_data[2]
        posted_years = verify_posted_dates_data[3]
        posted_dates_verify = verify_posted_dates_data[4]
        posted_date_error_text = verify_posted_dates_data[5]
    else:
        #[False, dates_verify, date_error_text]
        posted_dates_verify = verify_posted_dates_data[1]
        posted_date_error_text = verify_posted_dates_data[2]
    ##### --- #####

    ##### --- Check which dates are older between transaction and posted, if tranasction date is needed, pass value in mode for this
    if trans_dates_verify != False and posted_dates_verify != False:
        if TransDateCol != "Dont Need":
            calc_date_data_1, calc_months, calc_days, calc_years = compare_two_dates(trans_date_data_1, posted_date_data_1, True)
        else:
            calc_date_data_1, calc_months, calc_days, calc_years = compare_two_dates(trans_date_data_1, posted_date_data_1, False)
    
        print("\n\n")
        print(f'Length of posted_date_data: {len(posted_date_data)} --- Len of calc_date_data {len(calc_date_data_1)}')
        print("\n\n")


        ovr_months = []
        ovr_days = []
        ovr_years = []
        ovr_date_data_1 = []
        for i in calc_date_data_1:
            ovr_months.append("--")
            ovr_days.append("--")
            ovr_years.append("--")
            ovr_date_data_1.append("--")
    ##### --- #####

    ##### --- CHECK AMOUNT 1 --- #####
    amt1_verify = True
    amt1_error_line_no = 2
    amt1_error_text = "\tAmount 1 Error, Lines: "
    for i in amt1_data:
        try: value = float(i)
        except: 
            amt1_verify = False
            amt1_error_text = amt1_error_text + str(amt1_error_line_no) + ", "

        amt1_error_line_no+= 1

    if amt1_verify == True: communicate("\tAmount 1 Column is valid")
    else: communicate(f"{amt1_error_text}")
    ##### --- #####

    ##### --- CHECK AMOUNT 2 --- #####
    if Amt2Col != "Dont Need":
        amt2_verify = True
        amt2_error_line_no = 2
        amt2_error_text = "Amount 2 Error, Lines: "
        if amt2_data != []:
            for i in amt2_data:
                try: value = float(i)
                except: 
                    amt2_verify = False 
                    amt2_error_text = amt2_error_text + str(amt2_error_line_no) + ", "

                amt2_error_line_no += 1
            if amt2_verify == True: communicate("\tAmount 2 Column is valid")
            else: communicate(f"{amt2_error_text}")
    else:
        amt2_verify = True
    ##### --- #####

    if amt1_verify == True and amt2_verify == True and trans_dates_verify == True and posted_dates_verify == True:
        if Amt2Col != "Dont Need": 
            amt_clean = two_amounts_clean(amt1_data, Sign1, amt2_data, Sign2)
            if amt_clean != "Issue with amount Data in CSV":
                communicate(f"\tAmount Data has been cleaned")
            else:
                communicate("\tIssue with amount Data in CSV") 
        else:
            amt_clean = one_amounts_clean(amt1_data, Sign1)
            communicate("\tAmount Data has been cleaned")

        if len(posted_date_data) == len(desc_data) == len(trans_date_data_1) == len(posted_date_data) == len(amt_clean) == len(posted_months) == len(posted_years):
            data = []
            x = 0
            accounts = []
            communicate(posted_date_data)
            if Account == "Test Account 3":

                for i in trans_date_data_1:
                    print(i)
            for i in posted_date_data:
                hide = True
                if hide:
                    pass
                    # 0 -- id
                    # 1 -- Account text,
                    #   
                    # 2 -- MonthTrans text,
                    # 3 -- DayTrans text,
                    # 4 -- YearTrans text,         
                    # 5 -- TransDate text,

                    # 6 -- MonthPosted text,
                    # 7 -- DayPosted text,
                    # 8 -- YearPosted text,         
                    # 9 -- PostedDate text,

                    # 10 -- DateOverrideBool text,
                    # 11 -- OvrMonth text,
                    # 12 -- OvrDay text,
                    # 13 -- OvrYear text,
                    # 14 -- OvrDate text,

                    # 15 -- MonthCalc text,
                    # 16 -- DayCalc text,
                    # 17 -- YearCalc text,         
                    # 18 -- CalcDate text,

                    # 19 -- Description text, 
                    # 20 -- Amount Real, 
                    # 21 -- Tag1 text, 
                    # 22 -- Tag2 text,
                    # 23 -- Lock text,
                    # 24 -- Note text
                
                accounts.append(Account)
                data.append([
                    Account, 

                    trans_months[x], 
                    trans_days[x], 
                    trans_years[x], 
                    trans_date_data_1[x], 

                    posted_months[x], 
                    posted_days[x], 
                    posted_years[x], 
                    posted_date_data_1[x], 

                    "--",
                    ovr_months[x], 
                    ovr_days[x], 
                    ovr_years[x], 
                    ovr_date_data_1[x], 

                    calc_months[x], 
                    calc_days[x], 
                    calc_years[x], 
                    calc_date_data_1[x], 

                    desc_data[x], 
                    amt_clean[x], 
                    "NA", 
                    "NA", 
                    "Unlocked",
                    ""])
                
                x += 1
            ovr_boolean = []
            tag1 = []
            tag2 = []
            lock = []
            note = []
            for i in trans_date_data_1:
                ovr_boolean.append("--")
                tag1.append("NA")
                tag2.append("NA")
                lock.append("Unlocked")
                note.append(" ")
            
            dict_print = {'Account':accounts, 'TransMonth':trans_months, 'TransdDay':trans_days, 'TransYear':trans_years, 'TransdDate':trans_date_data_1,'PostedMonth':posted_months, 'PostedDay':posted_days, 'PostedYear':posted_years, 'PostedDate':posted_date_data_1,'OvrBoolean': ovr_boolean, 'OvrMonth':ovr_months, 'OvrDay':ovr_days, 'OvrYear':ovr_years, 'OvrdDate':ovr_date_data_1,'CalcMonth':calc_months, 'CalcdDay':calc_days, 'CalcYear':calc_years, 'CalcDate':calc_date_data_1, 'Desc':desc_data, "Amount":amt_clean, 'tag1':tag1, 'tag2':tag2, 'lock':lock,'note':note}
            data_1 = [accounts, posted_months, posted_days, posted_years, posted_date_data, desc_data, amt_clean] #Not used yet, see note above
            df = pd.DataFrame(dict_print)
            #print(df)
            
            communicate("SUCCESS\tData Is avalaible in data variable")
            return "Success", data
        else:
            communicate("BIGGER ISSUE")
            return "Fail", "Bigger Issue"
        
    else:
        Error_Text = ""
        if amt1_verify != True:
            Error_Text = "\n\t" + amt1_error_text
        if amt2_verify != True: 
            Error_Text += "\n\t" + amt2_error_text
        if posted_dates_verify != True:
            Error_Text += "\n\t" + posted_date_error_text
        communicate("ERROR\t" + Error_Text)
        return "Fail", Error_Text

def verify_dates(date_data, date_type = "Posted"):
    ##### ---- Check Dates ---- #####

    #Values to send: date_data
    dates_verify = True
    date_error_line_no = 2
    date_error_text = "\tDate Error, Lines: "
    months = []
    years = []
    days = []
    #Create a new date_data so that I can save all dates in the same format
    date_data_1 = []
    for i in date_data:
        mode = "date_format"
        if check_dates(i, mode) != True: 
            dates_verify = False 
            date_error_text = date_error_text + str(date_error_line_no) + ", "
        else:
            parsed = False
            for fmt in ('%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S'):
                try:
                    date_object = datetime.strptime(i, fmt)
                    parsed = True
                    break
                except ValueError:
                    continue
            if not parsed:
                raise ValueError(f"Unrecognized date format: {i!r}")

            date_data_1.append(str(date_object.strftime("%m/%d/%Y")))

            try:
                month_dummy = str(int(i[:i.find('/')]))
            except:
                month_dummy = str(int(date_object.month))
            months.append(month_dummy)

            try:
                year_dummy = str(int(i[len(i)-4:]))
            except:
                year_dummy = str(int(date_object.year))
            years.append(year_dummy)

            days.append(str(int(date_object.day)))
            date_error_line_no += 1

    if date_type != "Trans":
        mode = "same_month_check"
        if check_dates(months, mode) != True:
            dates_verify = False
            date_error_text = date_error_text + " All dates do not have the same month"


    if dates_verify == True: 
        communicate("\tDates Column is valid")
        return [date_data_1, months, days, years, dates_verify, date_error_text]
    
    else: 
        communicate(f"{date_error_text}")
        return [False, dates_verify, date_error_text]
    ##### --- #####

def check_dates(var, mode):
    if mode == "date_format":
        try:
            parse(var, fuzzy=False)
            
            return True
        except ValueError:
            return False
    elif mode == "same_month_check":
        boolean = True
        x = 0
        for i in var:
            if x ==0:
                x+=1
                pass
            else:
                prev_month = var[x-1]
                
                if i != prev_month:
                    boolean = False
        return boolean

def compare_two_dates(trans_date_data_1, posted_date_data_1, TransColumnNeeded):
    calc_months = [] 
    calc_days = []
    calc_years = []
    calc_date_data_1 = []

    if TransColumnNeeded != False:
        
        for x in range(len(trans_date_data_1)):
            if trans_date_data_1[x] < posted_date_data_1[x]:
                month = trans_date_data_1[x][:trans_date_data_1[x].find('/')]
                length = len(trans_date_data_1[x])
                year = trans_date_data_1[x][length-4:]

                day = datetime.strptime(trans_date_data_1[x], '%m/%d/%Y').day

                calc_months.append(str(int(month)))
                calc_days.append(str(int(day)))
                calc_years.append(year)
                calc_date_data_1.append(trans_date_data_1[x])
            else:
                month = posted_date_data_1[x][:posted_date_data_1[x].find('/')]
                length = len(posted_date_data_1[x])
                year = posted_date_data_1[x][length-4:]

                day = datetime.strptime(posted_date_data_1[x], '%m/%d/%Y').day

                calc_months.append(str(int(month)))
                calc_days.append(str(int(day)))
                calc_years.append(year)
                calc_date_data_1.append(posted_date_data_1[x])

        return calc_date_data_1, calc_months, calc_days, calc_years
        
    else:
        for x in range(len(posted_date_data_1)):
            month = posted_date_data_1[x][:posted_date_data_1[x].find('/')]
            length = len(posted_date_data_1[x])
            year = posted_date_data_1[x][length-4:]
            day = datetime.strptime(posted_date_data_1[x], '%m/%d/%Y').day

            calc_months.append(str(int(month)))
            calc_days.append(str(int(day)))
            calc_years.append(year)
            calc_date_data_1.append(posted_date_data_1[x])

        return calc_date_data_1, calc_months, calc_days, calc_years

def two_amounts_clean(amt1,amt1_sign, amt2, amt2_sign):
    amt1_clean = []
    for i in amt1:
        if amt1_sign == "Reverse Sign":
            amt1_clean.append(float(i) * (-1))
        else: 
            amt1_clean.append(float(i))

    amt2_clean = []
    for i in amt2:
        if amt2_sign == "Reverse Sign":
            amt2_clean.append(float(i) * (-1))
        else: 
            amt2_clean.append(float(i))
    
            
    amt_clean = []
    if len(amt1_clean) == len(amt2_clean):
        x = 0
        for i in amt1_clean:
            if i ==0:
                amt_clean.append(amt2_clean[x])
            else:
                amt_clean.append(i)
            x +=1
        return amt_clean
    else: 
        error_text = "Issue with amount Data in CSV"
        return error_text

def one_amounts_clean(amt1, amt1_sign):
    amt1_clean = []
    for i in amt1:
        if amt1_sign == "Reverse Sign":
            amt1_clean.append(float(i) * (-1))
        else: amt1_clean.append(float(i))
    return amt1_clean

def communicate(text):
    print(f"[CSV_Manager]...{text}")   

