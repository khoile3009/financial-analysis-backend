from abc import ABC, abstractmethod

import pandas as pd

from financial_analysis_backend.dataset import DataPoint


class Strategy(ABC):
    @abstractmethod
    def next(self, data_point: DataPoint):
        pass
