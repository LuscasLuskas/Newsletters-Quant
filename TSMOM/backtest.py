import pandas as pd
from functions import calculate_lookback_return, generate_signal, calculate_strategy_returns

def tsmom_backtest(prices, lookback=252): 
    df = pd.DataFrame(index=prices.index)
    df['price'] = prices
    
    # Step 1: Daily returns
    df['daily_return'] = prices.pct_change()
    
    # Step 2: Lookback return
    df['lookback_return'] = calculate_lookback_return(prices, lookback)
    
    # Step 3: Signal
    df['signal'] = generate_signal(df['lookback_return'])
    
    # Step 4: Strategy return
    df['tsmom_return'] = calculate_strategy_returns(df['signal'], df['daily_return'])
    
    # Step 5: Cumulative returns
    df['cumulative_tsmom'] = (1 + df['tsmom_return'].fillna(0)).cumprod()
    df['cumulative_buyhold'] = (1 + df['daily_return'].fillna(0)).cumprod()
    
    return df

