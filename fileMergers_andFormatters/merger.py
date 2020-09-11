import csv, string

counter = 1
price_count = 0
price = 0.0
price_avg = 0.0
day = 1
hour = 16
none = ' - -'
noners = 0
new_row = []
current_row = 1

#open('gas_price_avg.csv')
with open('gas_station_and_WTI_prices.csv', 'a') as output:
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    with open('gas_price_avg.csv', 'r') as avg_price, open('WTIprices.csv', 'r') as WTI:
        avg_file = csv.reader(avg_price)
        WTI_file = csv.reader(WTI)

        for wrow, arow in zip(WTI_file, avg_file):

            #print(row[0:3])
            # check if day and hour match on both files.
            if wrow[0] != arow[0] or wrow[1] != arow[1]:
                #print current_row of where mismatch found
                print(f'mismatch found in row{current_row}')        
                #break
                break    
            #else make new_row = [day, hour, avg_gas station price, WTI price]
            else:
                new_row = [arow[0], arow[1], arow[2], wrow[2]]
                #print row to file
                writer.writerow(new_row)
            #update current_row
            current_row += 1