import csv
month = ''
day = ''
year = ''
date = ''
new_row = []

with open('2000-2019-gasPricesDatesFixed.csv', 'a') as output:
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open('2000-2019_gasPrices.csv', 'r') as original:
            prices = csv.reader(original)
            for row in prices:
                if row[0][0:3] == 'Jan':
                    month = '1/'
                if row[0][0:3] == 'Feb':
                    month = '2/'
                if row[0][0:3] == 'Mar':
                    month = '3/'
                if row[0][0:3] == 'Apr':
                    month = '4/'
                if row[0][0:3] == 'May':
                    month = '5/'
                if row[0][0:3] == 'Jun':
                    month = '6/'
                if row[0][0:3] == 'Jul':
                    month = '7/'
                if row[0][0:3] == 'Aug':
                    month = '8/'
                if row[0][0:3] == 'Sep':
                    month = '9/'
                if row[0][0:3] == 'Oct':
                    month = '10/'
                if row[0][0:3] == 'Nov':
                    month = '11/'
                if row[0][0:3] == 'Dec':
                    month = '12/'
                day = row[0][4:6] + '/'
                year = row[0][8:12]
                date = month + day + year
                new_row = [date, row[1]]

                writer.writerow(new_row)    

                    #print(new_row)