from dataclasses import dataclass
from typing import Dict, List
from financial_analysis_backend.account import Account
from financial_analysis_backend.dataset import Dataset
from financial_analysis_backend.strategies.buy_and_hold import BuyAndHold
from financial_analysis_backend.strategies.moving_average_crossover import MovingAverageCrossover
from financial_analysis_backend.strategies.strategy import DoNothing, Order, OrderStatus, Strategy

@dataclass
class BacktestReport:
    sharpe_ratio: float = 0 
    start_balance: float = 0
    end_balance: float = 0

class Backtest:

    def __init__(self, strategy: Strategy, dataset: Dataset, initial_balance: float = 100000):
        self.strategy = strategy
        self.dataset = dataset
        self.initial_balance = initial_balance
        self.report = None
        self.account = Account(balance=initial_balance, porfolio={})
        self.strategy.set_account(self.account)
        self.dataset.subscribe(self.strategy.metrics)
        self.order_backlog: List[Order] = []

    def run(self):
        self.report = BacktestReport(start_balance = self.initial_balance)

        if dataset.is_empty():
            raise ValueError("Dataset is empty")
        
        while dataset.has_next():
            data_point = self.dataset.next()
            orders = self.strategy.next(data_point)
            if isinstance(orders, List) and len(orders) > 0:
                self.order_backlog += orders
            self.resolve_orders(data_point)
        self.report.end_balance = self.account.total_value(data_point)
        return self.report

    def resolve_orders(self, data_point):
        index = 0
        while index < len(self.order_backlog):
            order = self.order_backlog[index]
            order_result = order.resolve(data_point)
            if order_result.status == OrderStatus.SUCCESS:
                self.account.balance += order_result.cash_change
                # Go through the current asset and make the update
                for symbol, amount in order_result.asset_change.items():
                    self.account.porfolio[symbol] = self.account.porfolio.get(symbol, 0) + amount
                self.order_backlog.pop(index)
            else:
                index += 1

    

if __name__ == "__main__":
    do_nothing = DoNothing()
    dataset = Dataset(symbols=["PLTR"], interval="1d", period="5y")
    backtest = Backtest(do_nothing, dataset)
    backtest_report = backtest.run()
    print(backtest_report)

    # Buy and hold
    buy_and_hold = BuyAndHold("PLTR")
    dataset.reset()
    backtest = Backtest(buy_and_hold, dataset)
    backtest_report = backtest.run()
    print(backtest_report)

    # SMA Crossover
    sma_crosover = MovingAverageCrossover("PLTR", 100, 50)
    dataset.reset()
    backtest = Backtest(sma_crosover, dataset)
    backtest_report = backtest.run()
    print(backtest_report)