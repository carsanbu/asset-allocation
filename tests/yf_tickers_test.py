import unittest
import elemental
import matplotlib.pyplot as plt
from asset_allocation.yf_tickers import YFTickers

class YFTickersTest(unittest.TestCase):
    def test(self):
        tickers = YFTickers(elemental.Browser(headless=True), 'tmp/tickers.csv')
        ticker = list(tickers.value(['US0846707026']).values())[0]
        print(ticker)
        self.assertEqual('BRK-B', ticker)
if __name__ == '__main__':
    unittest.main()

