import numpy as np

def calculate_lookback_return(prices, lookback):
    
    return (prices - prices.shift(lookback)) / prices.shift(lookback)

def generate_signal(lookback_returns):
    
    return np.sign(lookback_returns)

def calculate_strategy_returns(signals, daily_returns):
    
    return signals.shift(1) * daily_returns