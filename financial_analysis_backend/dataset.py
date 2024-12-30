from datetime import datetime
from typing import List
import pandas as pd
import yfinance as yf

from financial_analysis_backend.data_type import DataPoint
from financial_analysis_backend.metrics.metric import Metric


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
        self.subscribed_metrics = []

    def subscribe(self, metric: Metric):
        self.subscribed_metrics.append(metric)
        
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
        data_point = DataPoint(row)
        
        # Update subscribed metrics
        for metric in self.subscribed_metrics:
            metric.next(data_point)
        return data_point

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
