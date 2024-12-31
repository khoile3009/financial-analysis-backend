from financial_analysis_backend.dataset import Dataset
from financial_analysis_backend.metrics.metric import Close, Power


if __name__ == "__main__":
    dataset = Dataset(symbols=["PLTR"], interval="15m", period="5d")
    close_metric = Close("PLTR")
    power_metric = Power(close_metric, 2)
    power_metric_3 = Power(close_metric, 3)
    dataset.subscribe(power_metric)
    dataset.subscribe(power_metric_3)
    dataset.next()
    print(close_metric.value)
    print(power_metric.value)
    print(power_metric_3.value)
    dataset.next()
    print(close_metric.value)
    print(power_metric.value)
