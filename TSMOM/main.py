import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from backtest import tsmom_backtest
from metrics import calculate_metrics

#Calling ticket symbol
ticket = input( "Enter the stock ticker symbol: " )
data = yf.download(ticket, start="2010-01-01", progress=False, auto_adjust=False)['Adj Close']
df = pd.DataFrame(data)
if isinstance(df.index, pd.DatetimeIndex):
    df.columns.get_level_values(0)
print(df.head())

# Running the backtest

real_results = tsmom_backtest(data, lookback=252)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(real_results['cumulative_tsmom'], label='TSMOM')
plt.plot(real_results['cumulative_buyhold'], label='Buy & Hold')
plt.title('TSMOM on ' + ticket)
plt.legend()
plt.show()

# Calculate metrics for our backtest
tsmom_metrics = calculate_metrics(real_results['tsmom_return'])
buyhold_metrics = calculate_metrics(real_results['daily_return'])

print("=" * 50)
print("PERFORMANCE COMPARISON")
print("=" * 50)
print(f"{'Metric':<20} {'TSMOM':<15} {'Buy & Hold':<15}")
print("-" * 50)
for key in tsmom_metrics:
    print(f"{key:<20} {tsmom_metrics[key]:<15} {buyhold_metrics[key]:<15}")

