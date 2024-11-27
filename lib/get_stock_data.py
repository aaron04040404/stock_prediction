import logging
import yfinance as yf
import pandas as pd # 資料處理套件
import datetime as dt # 時間套件
import talib
from .get_stock_ids import get_twse_stock_ids

logging.getLogger("yfinance").setLevel(logging.CRITICAL)

def get_stock_data(day = 5):
    with open('stock_ids.txt', 'r', encoding='utf-8-sig') as file:
        stock_ids = file.read().splitlines()
    
    stk_data = pd.DataFrame()
    for stock_id in stock_ids:
        try:
            data = yf.download(stock_id, period="2y", progress=False)  # 下載3個月的數據
            if data.empty:
                print(f"{stock_id} use max")
                data = yf.download(stock_id, period="max", progress=False)
        except Exception as e :
            return None
        data.insert(0, 'stock_id', stock_id)
        data['5MA'] = data['Close'].rolling(window = 5).mean()
        data['20MA'] = data['Close'].rolling(window = 20).mean()
        data['60MA'] = data['Close'].rolling(window = 60).mean()
        data['250MA'] = data['Close'].rolling(window = 250).mean()
        data['K'], data['D'] = talib.STOCH(data['High'], data['Low'], data['Close'],
                                                    fastk_period=9,
                                                    slowk_period=3,
                                                    slowk_matype=1,
                                                    slowd_period=3,
                                                    slowd_matype=1)
        data['MACD'], data['signal'], data['hist'] = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
        stk_data_unit = data.tail(day)
        stk_data = pd.concat([stk_data, stk_data_unit])
    return stk_data