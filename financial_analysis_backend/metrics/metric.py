from abc import ABC, abstractmethod
from typing import Dict, List

from financial_analysis_backend.data_type import DataPoint


class Metric(ABC):
    def __init__(self, wrapped_metrics: Dict[str, "Metric"] = None):
        self.data_points = []
        self.wrapped_metrics = wrapped_metrics or {}
        self.values = []
        self.last_timestamp = None

    def next(self, data_point: DataPoint):
        # Early breaking, essensially an AST to make sure everything only next once
        if self.last_timestamp == data_point.timestamp():
            return
        self.data_points.append(data_point)
        self.last_timestamp = data_point.timestamp()
        for _, metric in self.wrapped_metrics.items():
            metric.next(data_point)
        self.values.append(self.compute_value())

    @property
    def value(self):
        return self.values[-1]

    @abstractmethod
    def compute_value(self):
        pass

class Close(Metric):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def compute_value(self):
        return self.data_points[-1].close(self.symbol)

class Power(Metric):
    def __init__(self, base: Metric, hat: int):
        self.hat = hat
        super().__init__(wrapped_metrics={"base": base})


    def compute_value(self):
        return self.wrapped_metrics["base"].value ** self.hat
