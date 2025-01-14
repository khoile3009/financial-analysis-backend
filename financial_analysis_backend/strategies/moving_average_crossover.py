
from financial_analysis_backend.data_type import DataPoint
from financial_analysis_backend.metrics.metric import SMA, Close
from financial_analysis_backend.strategies.strategy import Strategy


class MovingAverageCrossover(Strategy):
    def __init__(self, symbol: str, slow_period: int = 100, fast_period: int = 50, *args, **kwargs):
        self.symbol = symbol
        self.close_metric = Close(symbol)
        self.sma_fast = SMA(self.close_metric, fast_period)
        self.sma_slow = SMA(self.close_metric, slow_period)
        self.next_day_order = None

    def next(self, data_point: DataPoint):
        # 
        crossover = self.sma_fast.crossover(self.sma_slow)
        if crossover == 1:
            print("BUY", data_point.close("PLTR"))
        if crossover == -1:
            print("SHORT", data_point.close("PLTR"))     

    @property
    def metrics(self):
        return [self.sma_fast, self.sma_slow]