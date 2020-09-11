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
with open('gas_price_avg.csv', 'a') as output:
    price_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open('gasprices.csv', 'r') as original:
        ori_file = csv.reader(original)
        for row in ori_file:
            #print(row[0:3])

            #check if row[0] and row [1] match day and hour
            if row[0] != str(day) or row[1] != str(hour):
                print(f'Row {current_row} had mismatch')
                day = int(row[0])
                hour = int(row[1])

            #add up prices only if row[2] is a number
            if none == row[2]:
                print(f'no price found in row {current_row}')
            else:
                price = price + float(row[2])
                price_count += 1
            #update counters
            counter += 1

            #reset counter, price, and price_count after 14 rows (counter range: 1-14)
            if counter == 15:
                counter = 1
                #divide price by price_count
                price_avg = price/price_count
                #print day, hour, avg price to new file (append)
                new_row = [row[0], row[1], str(price_avg)]
                #reset price and price_count
                price = 0
                price_count = 0
                #write avg to new file
                price_writer.writerow(new_row)
                #print(new_row)
                #update day and hour
                if hour < 23: 
                    hour += 1    
                else:
                    hour = 0
                    if day < 6:
                        day += 1
                    else:
                        day = 0
            #probably not using this
            current_row +=1

ori_file.close()
price_writer.close()