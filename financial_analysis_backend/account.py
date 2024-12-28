

from dataclasses import dataclass
from typing import Dict

from financial_analysis_backend.dataset import DataPoint


@dataclass
class Account:
    balance: float
    porfolio: Dict[str, float]

    def porfolio_value(self, data_point: DataPoint):
        value = 0
        for symbol, amount in self.porfolio.items():
            value += data_point.close(symbol) * amount
        return value
    
    def total_value(self, data_point: DataPoint):
        return self.balance + self.porfolio_value(data_point)