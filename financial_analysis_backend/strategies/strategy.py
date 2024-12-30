from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional
from financial_analysis_backend.data_type import DataPoint
from enum import Enum

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"
    BUY_DOLLAR_AMOUNT = "buy_dollar_amount"

class OrderStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAIL = "fail"

@dataclass
class OrderResult:
    status: OrderStatus
    cash_change: Optional[float] = None
    asset_change: Optional[Dict[str, float]] = None

@dataclass
class Order:
    order_type: OrderType
    amount: float
    symbol: str

    def resolve(self, data_point: DataPoint) -> OrderResult:
        if self.order_type == OrderType.BUY:
            return self.resolve_buy(data_point)
        elif self.order_type == OrderType.BUY_DOLLAR_AMOUNT:
            return self.resolve_buy_cash_amount(data_point)

    def resolve_buy(self, data_point: DataPoint) -> OrderResult:
        asset_change = {
            self.symbol: self.amount
        }
        order_result = OrderResult(status=OrderStatus.SUCCESS, cash_change=-data_point.close(self.symbol) * self.amount, asset_change=asset_change)

    def resolve_buy_cash_amount(self, data_point: DataPoint) -> OrderResult:
        close = data_point.close(self.symbol)
        asset_change = {
            self.symbol: self.amount / close
        }
        order_result = OrderResult(status=OrderStatus.SUCCESS, cash_change=-self.amount, asset_change=asset_change)
        return order_result

class Strategy(ABC):

    @abstractmethod
    def next(self, data_point: DataPoint) -> List[Order]:
        pass

    def set_account(self, account):
        self.account = account

class DoNothing(Strategy):
    def next(self, data_point):
        return []

