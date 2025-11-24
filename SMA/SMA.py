import pandas as pd
import yfinance as YF
import matplotlib.pyplot as plt
import numpy as np

# Download historical data for S&P 500 index from January 1, 2025
data = YF.download("^GSPC", start="2025-01-01", progress=False)
df = pd.DataFrame(data)
print(df.head())

#Showing the closing prices
plt.figure(figsize=(16,8))
plt.title("S&P 500 Closing Prices")
plt.plot(data["Close"], label="S&P 500 Close Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

#SMA Function
def SMA (data, period = 30, column = "Close"):
    return data[column].rolling(window=period).mean()
    
#SMA20 and SMA50
df["SMA20"] = SMA(df, period=20)
df["SMA50"] = SMA(df, period=50)

#Buy or Sell Signals
df["Signal"] = 0
df["Signal"] = np.where(df["SMA20"] > df["SMA50"], 1, 0)
df["Position"] = df["Signal"].diff()

#Signal Visualization
plt.figure(figsize=(16,8))
plt.title("S&P 500 Closing Prices with SMA20 and SMA50")    
plt.plot(df["Close"], label="S&P 500 Close Prices", alpha=0.7)
plt.plot(df["SMA20"], label="SMA20", linewidth=1.5)
plt.plot(df["SMA50"], label="SMA50", linewidth=1.5)

#Plot Buy Signals (SMA20 crosses above SMA50)
plt.plot(df[df["Position"] == 1].index,
         df["SMA20"][df["Position"] == 1],
         "^", markersize=12, color="g", label="Buy Signal")

#Plot Sell Signals (SMA20 crosses below SMA50)
plt.plot(df[df["Position"] == -1].index,
         df["SMA20"][df["Position"] == -1],
            "v", markersize=12, color="r", label="Sell Signal")

plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()
