import tushare as ts 
import pandas as pd
import matplotlib.pyplot as plt

ts.set_token('66d6adc50f850a0cfaf56f9ec023db9ec88179e8d1b314f08850a28d')   
pro = ts.pro_api()  

#002475.SZ 立讯精密
data = ts.pro_bar(ts_code='002475.SZ', adj='qfq', start_date='20190101', end_date='20200121')
df = data[ 'close']

def get_rolling_mean(values, window):
    return pd.roll_mean(values, window)

def get_rolling_std(values, window):
    return pd.rolling_std(values, window)

def get_bollinger_band(rm, rstd):
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd
    return upper_band, lower_band 

def get_daily_returns(df):
    return ((df / df.shift(1, fill_value = 0)) - 1)

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

if __name__ == "__main__":
    daily_returns = get_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")