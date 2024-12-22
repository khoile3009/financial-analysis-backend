from datetime import datetime
from typing import List
import pandas as pd
import yfinance as yf
import numpy as np


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


class Dataset:

    def __init__(
        self,
        symbols: List[str],
        interval: str,
        period: str,
        start: str | datetime = None,
        end: str | datetime = None,
    ):
        self.dataframe = Dataset.download_dataset(
            symbols=symbols, interval=interval, period=period, start=start, end=end
        )
        self.current_index = 0

    def next(self) -> pd.Series:
        row = self.dataframe.iloc[self.current_index]
        self.current_index += 1
        return DataPoint(row)

    @classmethod
    def get_dataset(
        cls,
        symbol: str,
        interval: str,
        period: str,
        start: str | datetime = None,
        end: str | datetime = None,
    ) -> pd.DataFrame:
        return None

    @classmethod
    def query_dataset(
        cls,
        symbol: str,
        interval: str,
        period: str,
        start: str | datetime = None,
        end: str | datetime = None,
    ) -> pd.DataFrame:
        return None

    @classmethod
    def download_dataset(
        cls,
        symbols: List[str],
        interval: str,
        period: str,
        start: str | datetime = None,
        end: str | datetime = None,
    ) -> pd.DataFrame:
        dataframe = yf.download(
            tickers=symbols, interval=interval, period=period, start=start, end=end
        )
        return dataframe


if __name__ == "__main__":
    dataset = Dataset(symbols=["PLTR"], interval="15m", period="5d")
    print(dataset.next().timestamp())
    print(dataset.next().timestamp())
    print(dataset.next().timestamp())
    print(dataset.next().open("PLTR"))
    print(dataset.next().open("PLTR"))
    print(dataset.next().open("PLTR"))
    print(dataset.next().open("PLTR"))
