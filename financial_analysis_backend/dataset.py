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
        self.dataframe = Dataset.get_dataset(
            symbols=symbols, interval=interval, period=period, start=start, end=end
        )
        self.current_index = 0
        self.total_rows = len(self.dataframe)

    def reset(self):
        self.current_index = 0

    def is_empty(self):
        return self.total_rows == 0

    def has_next(self) -> bool:
        return self.current_index < self.total_rows

    def next(self) -> pd.Series:
        if self.current_index >= self.total_rows:
            return None

        row = self.dataframe.iloc[self.current_index]
        self.current_index += 1
        return DataPoint(row)

    @classmethod
    def get_dataset(
        cls,
        symbols: List[str],
        interval: str,
        period: str,
        start: str | datetime = None,
        end: str | datetime = None,
    ) -> pd.DataFrame:
        try:
            file_name = cls.get_dataset_file_name(symbols, interval, period)
            dataframe = pd.read_pickle(file_name)
        except:
            dataframe = cls.download_dataset(symbols, interval, period)
        return dataframe

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
        cls.store_dataset(symbols, interval, period, dataframe)
        return dataframe

    @classmethod
    def store_dataset(
        cls,
        symbols: List[str],
        interval: str,
        period: str,
        dataframe: pd.DataFrame
    ):
        file_name = cls.get_dataset_file_name(symbols, interval, period)
        dataframe.to_pickle(file_name)

    @classmethod
    def get_dataset_file_name(
        cls,
        symbols: List[str],
        interval: str,
        period: str
    ):
        return f"datas/{'_'.join(symbols)}_{interval}_{period}.pkl"

if __name__ == "__main__":
    dataset = Dataset(symbols=["PLTR"], interval="15m", period="5d")
    print(dataset.next().timestamp())
    print(dataset.next().timestamp())
    print(dataset.next().timestamp())
    print(dataset.next().open("PLTR"))
    print(dataset.next().open("PLTR"))
    print(dataset.next().open("PLTR"))
    print(dataset.next().open("PLTR"))
