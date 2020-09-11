import csv

placeholder = 'placeholder'
old_row = []
new_row = [placeholder]
current_row = 0

#wrote this to merge two csv files based on matching dates.
#one file had almost daily rows, another weekly rows.

#open file to write to
with open('2000-2019_gas_station_and_WTI_prices.csv', 'a') as output:
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #open file to read from
    with open('WeeklyGasPrices.csv', 'r') as gas_price:
        gas_file = csv.reader(gas_price)
        #open the other file to read from
        with open('DailyWTIprices.csv', 'r') as WTI:
            WTI_file = csv.reader(WTI)
            #for every line in weekly file, I search whole daily file for a match(not efficient but files weren't huge)
            for grow in gas_file:
                #check if weekly file didn't have a match in daily file
                #breaks and prints row number(to fix manually)
                if new_row == old_row:
                    print(f'row {current_row} had no match')
                    break
                current_row += 1
                #updates old row
                old_row = new_row
                #loops through daily file
                for wrow in WTI_file:
                    if grow[0] == wrow[0]:
                        new_row = [grow[0], grow[1], wrow[1]]
                       # print(new_row)
                        writer.writerow(new_row)
                        break