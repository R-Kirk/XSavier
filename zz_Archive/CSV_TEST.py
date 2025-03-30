import csv
from dateutil.parser import parse


#with open('Eastex.csv', 'r') as csv_file:
#    csv_reader = csv.reader(csv_file)
#    next(csv_reader)
#    amounts = []
#    for line in csv_reader:
#        amounts.append(float(line[3]))
#for i in amounts: print(i)

def get_data(file, DateCol, DescCol, Amt1Col, Sign1, Amt2Col, Sign2):
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) #Skip the header row

        #date_data = []
        #desc_data = []
        #amt1_data = []
        #amt2_data = []
        for line in csv_reader:
        #    date_data.append(line[DateCol])
        #    desc_data.append(line[DescCol])
        #    amt1_data.append(line[Amt1Col])
        #    if Amt2Col != "Dont Need": amt2_data.append(line[Amt2Col])
            print(line)
            print(len(line[6]))


get_data("Capitol One.csv", 2, 4, 6, "Reverse Sign", 7, "Use original sign")
