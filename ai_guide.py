def generate_advice(indicators):
    if indicators["rsi"] < 30:
        return "Stock is oversold. May be a good opportunity to buy."
    elif indicators["rsi"] > 70:
        return "Stock is overbought. Caution advised."
    else:
        return "Stock appears stable. Monitor for more signals."
