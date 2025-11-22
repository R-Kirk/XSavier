import datetime
import pandas as pd

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

def get_line_series(data, tag_data, month, year):
    date_data = []
    amount_data = []
    for i in data:
        ovr_check = i[10]
        
        ##### --- Check if expense is overridden and month is no longer in this month, if so pass --- #####
        if i[10] == "Enabled" and int(i[11]) != int(month):
            #print("pass")
            #print(year)
            pass
        ##### --- #####

        else:
            if tag_data != False:
                
                tag = i[21]
                
                if tag == "NA":
                    YearCalc = int(i[17])
                    MonthCalc = int(i[15])
                    DayCalc = int(i[16])
                    if ovr_check == "--":
                        date_data.append(datetime.date(YearCalc, MonthCalc , DayCalc))
                    else:
                        OvrYear = int(i[13])
                        OvrMonth = int(i[11])
                        OvrDay = int(i[12])
                        date_data.append(datetime.date(OvrYear, OvrMonth, OvrDay))

                    
                    amount_data.append(float(i[20]))

                else:
                    ##### --- Check to see if tag is used in calculations --- #####
                    for x in tag_data:
                        # if tag = expense tag and tag setting is enabled in calculation
                        if tag == x[1] and x[5] != "False":
                            YearCalc = int(i[17])
                            MonthCalc = int(i[15])
                            DayCalc = int(i[16])

                            if ovr_check == "--":
                                date_data.append(datetime.date(YearCalc, MonthCalc , DayCalc))
                            else:
                                OvrYear = int(i[13])
                                OvrMonth = int(i[11])
                                OvrDay = int(i[12])
                                date_data.append(datetime.date(OvrYear, OvrMonth, OvrDay))

                            
                            amount_data.append(float(i[20]))
            else:

                YearCalc = int(i[17])
                MonthCalc = int(i[15])
                DayCalc = int(i[16])
                if ovr_check == "--":

                    date_data.append(datetime.date(YearCalc, MonthCalc , DayCalc))
                else:
                    OvrYear = int(i[13])
                    OvrMonth = int(i[11])
                    OvrDay = int(i[12])
                    date_data.append(datetime.date(OvrYear, OvrMonth, OvrDay))

                amount_data.append(float(i[20]))
        
    ##### ---  Get Days From Date Data --- #####
    days_data = []
    for i in date_data:
        days_data.append(int(i.day))
    ##### --- #####

    ##### --- Last Day of the Month - NOT USED IN CODE YET IF EVER --- #####
    mth = date_data[0].month
    yr = date_data[0].year
    if mth == 12:
        mth = 1
        yr +=1
    else:
        mth +=1
    last_day = (datetime.date(yr, mth, 1) - datetime.timedelta(days = 1)).day
    ##### --- #####

    ##### --- Get Mix/Max for Days --- #####
    min_day = min(days_data)
    max_day = last_day
    ##### --- #####
    
    ##### --- Get Sums for each day --- #####
    series_data = []
    x = 0
    for i in days_data:
        series_data.append([i, amount_data[x]])
        x +=1 

    remove_duplicate_dates = list(set(days_data))
    new_series_data = []
    for i in remove_duplicate_dates:
        day_total = float(0)
        for x in series_data:
            if i == x[0]:
                day_total += x[1]
        new_series_data.append([i, day_total])
    ##### --- #####

    ##### --- Get Running Total --- #####
    sorted_data = sorted(new_series_data, key=lambda t: t[0], reverse=False)
    running_total = float(0)
    sorted_data_2 = []
    for i in sorted_data:
        running_total += i[1]
        sorted_data_2.append([i[0], running_total])
    ##### --- #####

    ##### Get Min and Maxs for Amounts
    amount_totals = []
    for i in sorted_data_2:
        amount_totals.append(i[1])

    min_amount = min(amount_totals)
    max_amount = max(amount_totals)
    if max_amount <0:
        max_amount = 100
    
    ##### Set Data in format for QTGraph
    sorted_series = []
    for i in sorted_data_2:
        sorted_series.append((i[0], i[1]))

    ##### PRINT DF To Show Data when print_check = True - This is a manual set when needing to check data
    print_check = True
    if print_check:
        df = pd.DataFrame(sorted_data_2, columns = ["Date", "$ Total"])
        #print(df)

    communicate("Returned line series...")
    return sorted_series, min_day, max_day, min_amount, max_amount  

def get_bar_series(expenses, tag_data, show_zeros):
    tags_calc = []
    colors = []
    for tag in tag_data:
        ##### --- If used in Calculations --- #####
        if tag[5] != "False":
            tags_calc.append(tag[1])
        ##### --- #####

    series_totals = []
    tags_amount = []
    for current_tag in tags_calc:
        total = float(0)
        
        for expense in expenses:
            tag1 = expense[21]
            amount = float(expense[20])

            if tag1 == current_tag:
                total += amount

        if total < 0:
            total = total *-1
            colors.append("red")
        else:
            colors.append("green")

        series_totals.append(total)
        tags_amount.append(f"{tag}: {total}")


    ##### --- Sort te tags based on Largest to Smallest --- #####
    dummy_list = []
    index = 0
    for x in series_totals:
        tag =   tags_calc[index]
        color = colors[index]
        total = x
        if show_zeros:
            dummy_list.append([tag,color, total])
        else:
            if total > 0:
                dummy_list.append([tag,color, total])

        index += 1

    
    sorted_data = sorted(dummy_list, key=lambda x: x[2], reverse = True)

    tags_calc_1 = []
    colors_1 = []
    series_totals_1 = []
    
    for x in sorted_data:
        tags_calc_1.append(x[0])
        colors_1.append(x[1])
        series_totals_1.append(x[2])
    ##### --- #####
    communicate("Returned bar series...")
    # I was orginally returning tags_cals, colors, series_totals, but I changed this to what you see now so it so it looks better on the bar chart
    return tags_calc_1, colors_1, series_totals_1

def get_bar_series_1(expenses, tag_data):
    tags_calc = []
    for tag in tag_data:
        #If used in Calculations
        if tag[5] != "False":
            tags_calc.append(tag[1])

    series_totals_positive = []
    series_totals_negative = []
    tags_amount_positive = []
    tags_amount_negative = []
    tags_positive = []
    tags_negative = []
    for current_tag in tags_calc:
        total = 0
        for expense in expenses:
            tag1 = expense[21]
            if tag1 == current_tag:
                total += float(expense[20])
        if total < 0:
            total = total *-1
            series_totals_negative.append(total)
            tags_amount_negative.append(f"{tag}: {total}")
            tags_negative.append(tag)
        else:
            series_totals_positive.append(total)
            tags_amount_positive.append(f"{tag}: {total}")
            tags_positive.append(tag)

    
    communicate("Returned bar series...")
    return tags_positive, series_totals_positive, tags_negative, series_totals_negative
        
def get_date_bounds(month, year):
    start_date = datetime.date(year, month, 1)
     ##### Last Day of the Month - NOT USED IN CODE YET IF EVER
    mth = month
    yr = year
    if mth == 12:
        mth = 1
        yr +=1
    else:
        mth +=1
    last_day = (datetime.date(yr, mth, 1) - datetime.timedelta(days = 1)).day

    dates = [(start_date.month, start_date.day, start_date.year), (start_date.month, int(last_day), start_date.year)]
    communicate("Returned date bounds...")
    return dates

#Line Series
def get_year_cashflow(data, year, tag_data):
    amount_data =[0]
    month_dict = {
    "1": [0], "2": [0], "3": [0], "4": [0], 
    "5": [0], "6": [0], "7": [0], "8": [0], 
    "9": [0], "10": [0], "11": [0], "12": [0]
    }
    
    for expense in data:
        ovr_check = expense[10]
        if tag_data != False:
            ovr_month = expense[11]
            calc_month = expense[15]
            amount = float(expense[20])
            tag1 = expense[21]

            if tag1 == "NA":
                ##### --- Check if expense is overridden --- #####
                if ovr_check == "--":
                    month_dict[calc_month].append(amount)
                else:
                    month_dict[ovr_month].append(amount)
                ##### --- #####

                amount_data.append(amount)
            else:
                for i in tag_data:
                    if i[1] == tag1:
                        if i[5] != "False":
                            ##### --- Check if expense is overridden --- #####
                            if ovr_check == "--":
                                month_dict[calc_month].append(amount)
                            else:
                                month_dict[ovr_month].append(amount)
                            ##### --- #####

                            amount_data.append(amount)
        else:
            ##### --- Check if expense is overridden --- #####
            if ovr_check == "--":
                month_dict[calc_month].append(amount)
            else:
                month_dict[ovr_month].append(amount)
            ##### --- #####
            amount_data.append(amount)
       
    yearly_cashflow = [sum(month_dict["1"]), 
                       sum(month_dict["2"]), 
                       sum(month_dict["3"]), 
                       sum(month_dict["4"]), 
                       sum(month_dict["5"]), 
                       sum(month_dict["6"]), 
                       sum(month_dict["7"]), 
                       sum(month_dict["8"]), 
                       sum(month_dict["9"]), 
                       sum(month_dict["10"]),
                       sum(month_dict["11"]), 
                       sum(month_dict["12"])]
    

    yearly_series = [(0,0)]
    month = int(1)
    running_total = float(0)
    running_total_values = []
    for x in yearly_cashflow:
        running_total += x
        yearly_series.append((month, running_total))
        running_total_values.append(running_total)
        month +=1
    
    min_y = min(running_total_values)
    max_y = max(running_total_values)
    if max_y < 0:
        max_y = 0
    min_x = 1
    max_x = 12
    communicate(f"Returned Yearly Series...")
    
    return yearly_series,  min_x, max_x, min_y, max_y

def check_keyword_rules(new_rule, existing_rules, id=False):
    """
    Function retuns True if keyword is valid and False if keyword is invalid.

    :Parameters:
    - new_rule (list) = [keyword, tag1, tag2]
    - existing_rules (list) = db query of all keyword rules
    - id (integer) = id value of existing keyword rule if editing, don't need to send a value if new keyword rule.

    :Example: New Rule:
    >>> jarvis.check_keyword_rule(new_rule, existing_rule)
    "True"
    :Example: Existing Rule:
    >>> jarvis.check_keyword_rule(new_rule, existing_rule, 2)
    "True"
    """

    if existing_rules != False:
        validity = True
        if id:
            # Check existing rule against new rule
            for rule in existing_rules:
                if rule[0] != id:
                    if new_rule[0].upper() in rule[1].upper():
                        validity = False
                    
            # Check every every rule against new rule
            for rule in existing_rules:
                if rule[0] != id:
                    if rule[1].upper() in new_rule[0].upper():
                        validity = False
        else:
            # Check existing rule against new rule
            for rule in existing_rules:
                
                if new_rule[0].upper() in rule[1].upper():
                    validity = False
                    
            # Check every every rule against new rule
            for rule in existing_rules:
                if rule[1].upper() in new_rule[0].upper():
                    validity = False

        return validity
    else:
        validity = True
        return validity

def remove_overridden_expenses(expenses, month, year):
    expenses_new = []
    for expense in expenses: 
        ovrCheck = expense[10]
        
        
        calcMonth = int(expense[15])
        calcYear = int(expense[17])

        if ovrCheck != "--":
            ovrMonth = int(expense[11])
            ovrYear = int(expense[13])
            if ovrMonth == int(month) and ovrYear == int(year):
                expenses_new.append(expense)
        else:
            expenses_new.append(expense)
    return expenses_new

def analytics_create_data(tree_data, expenses_by_month):
    count = 0
    
    tree_data_1 = tree_data
    for expenses in expenses_by_month:
        


        for expense in expenses:
            tag1 = expense[21]
            tag2 = expense[22]
            amount = float(expense[20])

            OvrBoolean = expense[10]
            OvrMonth = expense[11]
            OvrYear = expense[13]

            CalcMonth = expense[15]
            CalcYear = expense[17]

            if OvrBoolean != "--":
                CalcMonth = OvrMonth
                CalcYear = OvrYear
            
            
            prev_amount_tag2 = float(tree_data_1[tag1][1][tag2][int(CalcMonth)-1])
            tree_data_1[tag1][1][tag2][int(CalcMonth)-1] = round(prev_amount_tag2 + amount,2)

            prev_amount = float(tree_data_1[tag1][0][int(CalcMonth)-1])
            tree_data_1[tag1][0][int(CalcMonth)-1] = round((amount + prev_amount),2)

        count += 1

    return tree_data_1

def communicate(text):
    print(f"[jarvis]...{text}")   