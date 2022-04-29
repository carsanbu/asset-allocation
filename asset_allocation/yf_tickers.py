import elemental
import time
import random
import pandas as pd
from os.path import exists
import urllib.parse as urlparse
from urllib.parse import parse_qs

class YFTickers:
    '''Extract Yahoo Tickers from ISIN list
        Use a storage_file for caching
    '''
    def __init__(self, browser, storage_file):
        self.browser = browser
        self.tickers_file = storage_file
    def get_ticker(self, isin):
        try:
            self.browser.get_input(id="yfin-usr-qry").fill(isin)
            self.browser.get_button(type="submit").click()
            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(random.randrange(1,10))
            return self.get_ticker(isin)
        return urlparse.urlparse(self.browser.url)
    @staticmethod
    def load_cache_file(tickers_file):
        tickers_df = pd.DataFrame(columns=['ISIN', 'Ticker'])
        if exists(tickers_file):
            tickers_df = pd.read_csv(tickers_file)
        return tickers_df

    def value(self, isins):
        tickers = dict()
        cache_tickers = self.load_cache_file(self.tickers_file)
        # https://github.com/red-and-black/elemental
        self.browser.visit("https://finance.yahoo.com/lookup")
        self.browser.get_button(type="submit").click()
        for isin in isins:
            if isin in cache_tickers['ISIN'].values:
                tickers[isin] = cache_tickers[cache_tickers['ISIN']==isin]['Ticker'].values[0]
                print("ISIN cached: " + tickers[isin])
            else:
                parsed = self.get_ticker(isin)
                try:
                    print("ISIN not cached: " + isin)
                    tickers[isin] = (parse_qs(parsed.query)['p'][0])
                except KeyError:
                    tickers[isin] = "n/a"
                time.sleep(random.randrange(1,10)) # Random sleep to next query
        self.browser.quit()
        return tickers
