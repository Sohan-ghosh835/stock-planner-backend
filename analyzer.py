import numpy as np

def calculate_indicators(prices):
    sma10 = prices.rolling(window=10).mean().iloc[-1]
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    rs = gain / loss if loss else 0
    rsi = 100 - (100 / (1 + rs))
    volatility = prices.pct_change().std()
    return {"sma10": sma10, "rsi": rsi, "volatility": volatility}
