import tushare as ts 
ts.set_token('66d6adc50f850a0cfaf56f9ec023db9ec88179e8d1b314f08850a28d')   
pro = ts.pro_api()   

df = ts.pro_bar(ts_code='002475.SZ', adj='qfq', start_date='20190101', end_date='20200121') 
