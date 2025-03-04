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
        if len(self.values) == 0:
            raise ValueError("There is no value to get")
        return self.values[-1]

    def crossover(self, metric: "Metric") -> bool:
        """
        Return  0 if no crossover happen
                1 if crossover and this metric is larger now
                -1 if crossover happened and this metric is smaller now 
        """
        prev_value = self.previous_value
        target_prev_value = metric.previous_value

        if prev_value is None or target_prev_value is None or self.value is None or metric.value is None:
            return 0
        
        if prev_value - target_prev_value > 0 and self.value - metric.value <= 0:
            return 1
    
        if prev_value - target_prev_value < 0 and self.value - metric.value >= 0:
            return -1
        return 0
    
    @property
    def previous_value(self) -> float | None:
        if len(self.values) < 2:
            return None
        
        return self.values[-2]

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

class SMA(Metric):
    def __init__(self, metric: Metric, period: int):
        self.period = period
        super().__init__(wrapped_metrics={"metric": metric})

    def compute_value(self):
        if len(self.wrapped_metrics["metric"].values) < self.period:
            return None
        
        avg = sum(self.wrapped_metrics["metric"].values[-self.period:]) / self.period
        return avg