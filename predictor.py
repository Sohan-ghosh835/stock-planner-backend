import numpy as np
from sklearn.linear_model import LinearRegression

def predict_prices(prices):
    days = np.arange(len(prices)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(days, prices.values)
    future_days = np.arange(len(prices), len(prices) + 30).reshape(-1, 1)
    return model.predict(future_days).tolist()
