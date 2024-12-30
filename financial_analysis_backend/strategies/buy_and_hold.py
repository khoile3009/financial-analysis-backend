from typing import Dict, List
from financial_analysis_backend.data_type import DataPoint
from financial_analysis_backend.strategies.strategy import Order, OrderType, Strategy


class BuyAndHold(Strategy):
    def __init__(self, symbol: str, *args, **kwargs):
        self.symbol = symbol

    def next(self, 
             data_point: DataPoint) -> List[Order]:
        if self.account.balance > 1:
            return [Order(order_type=OrderType.BUY_DOLLAR_AMOUNT, amount=self.account.balance, symbol=self.symbol)]