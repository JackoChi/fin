import tushare as ts 
import pandas as pd
import matplotlib.pyplot as plt

ts.set_token('66d6adc50f850a0cfaf56f9ec023db9ec88179e8d1b314f08850a28d')   
pro = ts.pro_api()  

#002475.SZ 立讯精密
df_temp = ts.pro_bar(ts_code='002475.SZ', adj='qfq', start_date='20190101', end_date='20200121')
#dates = pd.date_range('20190101', '20200121')
#df = pd.DataFrame(index=dates)
df= df_temp[['trade_date', 'close']]
#df = df.join(df_temp)
#df['date'] = pd.to_datetime(df['trade_date'])
#df.drop('trade_date', axis = 1, inplace = True)
df.set_index('trade_date', inplace = True)

def get_rolling_mean(values, window):
    return pd.roll_mean(values, window)

def get_rolling_std(values, window):
    return pd.rolling_std(values, window)

def get_bollinger_band(rm, rstd):
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd
    return upper_band, lower_band 

def get_daily_returns(df):
    return ((df / df.shift(1)) - 1).fillna(0)

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def plot_dailyreturns(df, bins = 20, title = "Hist of Daily returns"):
    
    return df.hist(bins = bins)
    

def get_tbill(field = 'm3'):
    """
    request the US Treasury bill interest rate
    
    argument:
    different type of Tbill, default value is 3 month

    """

    tbill = pro.us_tycr(start_date = '20190101', end_date='20200121', field = field)
    tbill = tbill[['date', 'm3']]
    tbill.set_index('date', inplace = True)
    return tbill['m3'] 

def merge(df, tbill):
    """
    first
    merge portfolio data with risk free rate
    second
    fill na data will ffill, and then bfill

    return merged df
    """
    df_temp = df.join(tbill)
    df_temp.fillna(method = 'pad', inplace = True)
    df_temp.fillna(method = 'bfill', inplace = True)

    return df_temp

def sharpe_ratio(df, stock='close', tbill='m3'):
    """
    calculate the sharpe ratio of given data

    arguments:
    stock - the column of the data represents the price of portfolio
    tbill - the risk free rate

    return 
    sharpe_ratio
    """
    return (df[stock] - df[tbill]).mean() / (df[stock] - df[tbill]).std()

if __name__ == "__main__":
    daily_returns = get_daily_returns(df)
    plot_dailyreturns(daily_returns)
    tbill = get_tbill()
    tbill_returns = get_daily_returns(tbill)
    plot_dailyreturns(tbill)
    plt.show()
    merge = merge(daily_returns, tbill) 
    print (sharpe_ratio(merge))
