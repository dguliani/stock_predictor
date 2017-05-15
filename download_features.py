import urllib2
import csv
import requests
import os
import numpy as np

PRICE_POS = 17
SHARES_UNADJUSTED_POS = 1
SPLIT_FACTOR_POS = 2 # Not actually the split factor pos, but just to delete

CHECK_POS = [[17], [18], [19], [11], [12]]

def fix_features(table):
    # Next Price is the forward quarter price and
    next_price = float(table[1][PRICE_POS])
    cum_gain = 1
    ret_table = []
    ret_table.append(table[0])
    for pos, item in enumerate(table[1:]):
        #
        to_del = np.where(np.array(item)=='None')
        if CHECK_POS in to_del[0]:#len(to_del[0]) > 0:
            pass
        else:
            if len(to_del[0]) > 0:
                # print to_del[0]
                for del_id in to_del[0]:
                    item[del_id] = 0

            # Adds the output variable which is the next quarter's percent gain
            cur_price = float(item[PRICE_POS])
            gain = next_price/cur_price
            next_price = cur_price
            cum_gain = cum_gain*gain
            # print gain
            item.append(gain)

            # Delete share volume unadjusted and  split factor; not really features
            del item[SHARES_UNADJUSTED_POS]
            del item[SPLIT_FACTOR_POS]

            ret_table.append(item)

    return ret_table
    # print "Cumulative: {}".format(cum_gain)

stocks = []
stock_ids = []
with open('constituents.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
        stocks.append(row['Symbol'])
        stock_ids.append(row['Id'])
print('Found {} stocks'.format(len(stocks)))

# Get all CSV names
csv_names = []
for stock in stocks:
    csv_names.append('{}_quarterly_financial_data.csv'.format(stock))
    # print csv_name

# cleanup old file: TODO add try catch around this
try:
    os.remove("features.csv")
except:
    pass
else:
    print("File Removed!")

for i in range(len(csv_names)):
    CSV_URL = 'http://www.stockpup.com/data/' + csv_names[i]
    print CSV_URL
    with requests.Session() as s:
        download = s.get(CSV_URL)
        if download.status_code is not 200:
            print ('Skipping {} at {} due to download error'.format(stocks[i], stock_ids[i]))
        else:
            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            my_data = fix_features(my_list)

            begin_ind = 1
            if i is 0:
                begin_ind = 0
                my_data[0].append('Gain')
                my_data[0].append('Id')
                del my_data[0][SHARES_UNADJUSTED_POS]
                del my_data[0][SPLIT_FACTOR_POS]

            with open('features.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
                for j in range(begin_ind, len(my_data)):
                    if j is 0:
                        pass
                    else:
                        my_data[j].append(stock_ids[i])
                    writer.writerow(my_data[j])
