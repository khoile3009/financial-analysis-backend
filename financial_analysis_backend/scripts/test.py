from financial_analysis_backend.dataset import Dataset
from financial_analysis_backend.metrics.metric import SMA, Close, Power


if __name__ == "__main__":
    dataset = Dataset(symbols=["PLTR"], interval="15m", period="5d")
    close_metric = Close("PLTR")
    power_metric = Power(close_metric, 2)
    power_metric_3 = Power(close_metric, 3)
    sma = SMA(close_metric, 3)
    dataset.subscribe(power_metric, power_metric_3, sma)
    dataset.next()
    print(close_metric.value)
    print(sma.value)
    dataset.next()
    print(close_metric.value)
    print(sma.value)
    dataset.next()
    print(close_metric.value)
    print(sma.value)
    dataset.next()
    print(close_metric.value)
    print(sma.value)
    
