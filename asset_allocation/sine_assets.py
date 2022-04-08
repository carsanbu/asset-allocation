import numpy as np
import pandas as pd

class SineAsset:
    def __init__(self, min, max, period, phase):
        self.min = min
        self.max = max
        self.period = period
        self.phase = phase
    def history(self):
        inp = np.linspace(-np.pi+self.phase, np.pi+self.phase, self.period)
        return np.sin(inp)
