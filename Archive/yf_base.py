'''
A base class for querying yahoo finance apis for data and doing predictions on them.
Builds on top of yahoo_finance. Some sources for additional info:
- https://pypi.python.org/pypi/yahoo-finance
'''
import requests
import json
import yahoo_finance as YFin
import pandas as pd
import csv
from pandas.tseries.offsets import BDay

from pprint import pprint

# BaseUrl = "http://finance.yahoo.com/webservice/v1/symbols/COALINDIA.NS/quote?format=json&view=detail"
class YahooFClient(object):
    BaseUrl = "http://finance.yahoo.com/webservice/v1/symbols/COALINDIA.NS/quote?format=json&view=detail"
    def __init__(self):
        # pass
        # self.fetch_sp_500()
        self.test_fcn('AAPL')

    # Checks Most Recent Logged data and fetches remaining
    def refresh_data(self):
        pass

    def fetch_sp_500(self):
        stocks = []
        print('Fetching list of stocks')
        with open('constituents.csv') as csvfile:
             reader = csv.DictReader(csvfile)
             for row in reader:
                stocks.append(row['Symbol'])
        print('Found {} stocks'.format(len(stocks)))

        with open('s&p500_contituent_prices.csv', 'wb') as csvfile:
            for j in range(len(stocks)):
                stock = stocks[j]
                print('Fetching yearly data for {}'.format(stock))
                data = self.get_yearly_data(stock, years=15)
                fieldnames = ['Symbol', 'Date', 'Volume', 'Open',
                              'Close', 'Adj_Close', 'High', 'Low']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(len(data)):
                    day_data = data[i]
                    writer.writerow(day_data)


    def get_yearly_data(self, stock, years=15):
        share = YFin.Share(stock)
        if share is not None:
            td = pd.datetime.today()
            ed = str(td.date())
            sd = str(td.year - years) + '-01-01'
            return share.get_historical(sd, ed)

    # TODO Doesn't yet get the right number of elements requested
    def get_historical_data(self, stock_sym, count=10):
        share = YFin.Share(stock_sym)
        if share is not None:
            today = pd.datetime.today()
            end_date = str(today.date())
            start_date = str((today-BDay(count)).date())
            return share.get_historical(start_date, end_date)

    def get_quote(self, stock_sym, detail=False):
        return self.api_get_request()

    # Base Functions TODO: Legacy Delete
    def api_get_request(self, url):
        resp = requests.get(url)
        if(resp.status_code != 200):
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        else:
            return resp.json()

    def test_fcn(self, stock_sym):
        share = YFin.Share(stock_sym)
        # print dir(share)

        if share is not None:
            # pprint(share.get_historical('2015-1-1', '2015-1-2'))
            # pprint(share.get_days_range())
            # pprint(share.get_earnings_share())
            # pprint(share.get_market_cap())
            pprint(share.get_one_yr_target_price())


# If not used dynamically, this file acts as a data grabber
# Gets daily trade data for all the companies in constituents.csv
if __name__ == "__main__":
    yf_client = YahooFClient()
    # yf_client.fetch_sp_500() # Use this method carefully
    del yf_client

