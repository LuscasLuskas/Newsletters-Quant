import pandas as pd
import yfinance as YF
import matplotlib.pyplot as plt
import numpy as np

# Download historical data for S&P 500 index from January 1, 2025
data = YF.download("^GSPC", start="2025-01-01", progress=False)
df = pd.DataFrame(data)
if isinstance(df.index, pd.DatetimeIndex):
    df.columns.get_level_values(0)
print(df.head())

#Showing the closing prices
plt.figure(figsize=(16,8))
plt.title("S&P 500 Closing Prices")
plt.plot(data["Close"], label="S&P 500 Close Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

#EMA12 and EMA26
df ['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
df ['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()

#MACD Function
df ['MACD'] = df ['EMA12'] - df ['EMA26']

#Signal Line
df ['Signal Line'] = df ['MACD'].ewm(span=9, adjust=False).mean()

#Histogram
df ['Histogram'] = df ['MACD'] - df ['Signal Line']

# Buy or Sell Signals
df["Signal"] = 0
df["Signal"] = np.where(df["MACD"] > df["Signal Line"], 1, 0)
df["Position"] = df["Signal"].diff()

# 3. Visualization
plt.figure(figsize=(16,8))
plt.title("S&P 500 Closing Prices & MACD")
plt.grid(True)

# Chart Visualization with two y-axes
plt.plot(df["Close"], label="S&P 500 Close Prices", color='black', alpha=0.5)
plt.ylabel("Price (USD)")
plt.legend(loc='upper left')

# Creating a second y-axis for MACD
ax2 = plt.twinx() 
ax2.plot(df.index, df["MACD"], label="MACD", color='blue', linewidth=1.5)
ax2.plot(df.index, df["Signal Line"], label="Signal Line", color='red', linewidth=1.5)
plt.legend(loc='lower left')

#Histogram bars
colors = ['green' if v >= 0 else 'red' for v in df['Histogram']]
ax2.bar(df.index, df['Histogram'], color=colors, alpha=0.3, label='Histogram')

# Signal Visualization
ax2.plot(df[df["Position"] == 1].index,
         df["MACD"][df["Position"] == 1],
         "^", markersize=12, color="g", label="Buy Signal")

ax2.plot(df[df["Position"] == -1].index,
         df["MACD"][df["Position"] == -1],
         "v", markersize=12, color="r", label="Sell Signal")

ax2.set_ylabel("MACD Momentum")

plt.show()
