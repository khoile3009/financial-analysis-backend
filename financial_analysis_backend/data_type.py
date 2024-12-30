import numpy as np
import pandas as pd


class DataPoint:
    def __init__(self, row: pd.Series):
        self.row = row

    def timestamp(self) -> np.datetime64:
        return self.row.name

    def close(self, symbol: str) -> float:
        return self.row.Close[symbol]

    def open(self, symbol: str) -> float:
        return self.row.Open[symbol]

    def high(self, symbol: str) -> float:
        return self.row.High[symbol]

    def low(self, symbol: str) -> float:
        return self.row.Low[symbol]

    def volume(self, symbol: str) -> float:
        return self.row.Volume[symbol]

    def adjusted_close(self, symbol: str) -> float:
        return self.row["Adj Close", symbol]