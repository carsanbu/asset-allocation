# Search for assets in https://finance.yahoo.com 
# For more information in https://www.morningstar.com
from sklearn.preprocessing import normalize
from pandas_datareader import data as wb
import yfinance as yf
import pandas as pd
import numpy as np

def drawdown(total, initial_cap, show):
    suma = total / initial_cap
    drawdown = suma - suma.cummax()
    if(show):
        drawdown.plot(figsize=(12,10))
    return np.min(drawdown)

def annual_volatilities(history):    
    v_years = pd.DataFrame()
    for t, history_year in history.resample('A'):
        std = pd.Series((history_year/history_year[:1].values).std())
        std.name = t
        v_years = v_years.append(std)
    return v_years

def volatilities(history):
    return annual_volatilities(history).mean()

def annual_performances(history):    
    performance_years = pd.DataFrame()
    for t, history_year in history.resample('A'):
        perf = pd.Series(((history_year/history_year[:1].values)[-1:]).squeeze())
        perf.name = t
        performance_years = performance_years.append(perf)
    return performance_years-1

def performances(history):
    return annual_performances(history).mean()

from sklearn.preprocessing import normalize
from scipy import stats
class AssetUniverse:
    def __init__(self, stocks, start='2000-1-1'):
        self.stocks = stocks
        self.start = start
    def assets(self):
        return self.stocks.copy()
    @staticmethod
    def search_max_index(history):
        maxim = history[0].index[0]
        asset = history[0].name
        for i in history:
            if maxim < i.index[0]:
                maxim = i.index[0]
                asset = i.name
        #print('Last asset prices:',asset, maxim)
        return maxim
    @staticmethod
    def search_max_len(history):
        max_len = (0, 0)
        for i in range(len(history)):
            if(max_len[0] < len(history[i])):
                max_len = (len(history[i]), i)
        return max_len
    def history(self):
        assets = self.stocks.copy()
        assets.remove('Leftover')
        data = []
        yf.pdr_override()

        for asset in assets:
            df = pd.DataFrame(wb.get_data_yahoo(asset, data_source='yahoo', start=self.start)['Adj Close'])
            # Limpia outliers
            z=np.abs(stats.zscore(df))
            df[(z > 5)] = np.nan
            df = df.fillna(method='ffill')
            df.name = asset
            data.append(df)

        max_index = AssetUniverse.search_max_index(data)
        normalized_index_data = []
        for d in data:
            subset = d[max_index:]
            subset.name = d.name
            normalized_index_data.append(subset)

        max_len = AssetUniverse.search_max_len(normalized_index_data)

        reindexed = normalized_index_data[max_len[1]].copy()        
        reindexed = reindexed.rename(columns={'Adj Close': data[max_len[1]].name})

        for i in range(len(normalized_index_data)):
            if i != max_len[1]:
                h = normalized_index_data[i]
                reindexed[h.name] = h.reindex(normalized_index_data[max_len[1]].index, method='ffill')

        return reindexed

    def crosscorrelation(self, step):
        h = self.history()
        n = len(h)
        corr = []
        for i in range(0, n, step):
            corr.append(h[i:i+step].corr())
        return corr

    def volatility(self):
        return volatilities(self.history())    
    def performance(self):
        return performances(self.history())
    def copy(self):
        return AssetUniverse(self.stocks, self.start)

class AssetUniverseCache:
    def __init__(self, asset_universe):
        self.asset_universe = asset_universe
        self.hist = None
    def assets(self):
        return self.asset_universe.assets()
    def history(self):
        if type(self.hist) != pd.DataFrame:
            self.hist = self.asset_universe.history()
        return self.hist
    def volatility(self):
        return volatilities(self.history())    
    def performance(self):
        return performances(self.history())
    def copy(self):
        c = AssetUniverseCache(self.asset_universe.copy())
        c.hist = self.hist.copy()
        return c
