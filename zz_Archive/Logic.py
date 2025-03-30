import datetime
import pandas as pd
def get_series(data):
    date_data = []
    amount_data = []
    unique_dates = []
    for i in data:
        unique_dates.append(str(i[4]) + "-" + str(i[2]) + "-" + str(i[3]))
        date_data.append(datetime.date(int(i[4]), int(i[2]), int(i[3])))
        amount_data.append(float(i[7]))
    date_data.append(datetime.date(int(2024), int(3), int(3)))
    date_data.append(datetime.date(int(2024), int(3), int(10)))
    date_data.append(datetime.date(int(2024), int(3), int(15)))
    amount_data.append(float(0))
    amount_data.append(float(0))
    amount_data.append(float(0))

    unique_dates_1 = list(set(unique_dates))
    min_y = min(amount_data)
    max_y = min(amount_data)

    
    
    
    series_data = []
    x = 0
    for i in date_data:
        series_data.append([i, amount_data[x]])
        x +=1 
    
    #Get Sums for each day
    unique_dates_2 = list(set(date_data))
    new_series_data = []
    count = 0
    for i in unique_dates_2:
        day_total = float(0)
        for x in series_data:
            if i == x[0]:
                day_total += x[1]
        new_series_data.append([i, day_total])

    df = pd.DataFrame(new_series_data, columns = ["Date", "$ Total"])
    print(df)


    

    sorted_data = sorted(new_series_data, key=lambda t: datetime.datetime.strftime(t[0], '%Y-%m-%d'))
    sorted_series = []
    for i in sorted_data:
        sorted_series.append((i[0], i[1]))

    days_between = (sorted_series[len(sorted_series)-1][0]- sorted_series[0][0])
    print(f" Days between Dates: {days_between.days}")

    

    return sorted_series,min_y, max_y, days_between.days

    #df = pd.DataFrame(sorted_series, columns = ["Date", "Amount"])
    #print(df)
    
    