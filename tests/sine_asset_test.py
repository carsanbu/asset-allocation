import unittest
import matplotlib.pyplot as plt
from asset_allocation import sine_assets
from asset_allocation.sine_assets import SineAsset

class SineAssetTest(unittest.TestCase):
    def test(self):
        sine = SineAsset(0, 100, 50, 3.14)
        print(sine.history())
        plt.plot(sine.history())
        plt.show()
        self.assertTrue(max(sine.history()) < 1)
        self.assertTrue(max(sine.history()) > -1)
if __name__ == '__main__':
    unittest.main()
