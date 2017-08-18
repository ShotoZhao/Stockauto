#!/usr/bin/env python
# encoding: utf-8


"""
@author: Shoto_Sakura
@name: stock_data_treatment 
@contact: micalun@gmail.com
@time: 2017/8/17 10:09
"""

import pandas as pd
import numpy as np


class DataTreatment(object):
    def __init__(self, data):
        self.data = data

    def rise_cal(self):
        for data, stock in self.data:
            try:
                data['rise'] = data['close_price'].pct_change()  # 股价实际上涨幅度
                data['krise'] = (data['close_price'] - data['open_price']) / data['open_price']  # k线上涨幅度

                fir = ((data['krise'] > data['rise']) & (data['rise'] > 0))  # 股价上涨时选择k线和实际上涨幅度大值
                sec = (data['krise'] < data['rise']) & (data['rise'] < 0)  # 股价下跌时选择k线和实际下跌幅度大值

                chose_rise = fir | sec
                kline = data['krise']

                data['trise'] = kline[chose_rise]
                data.fillna({'trise': data['rise']}, inplace=True)

                yield data, stock

            except Exception, e:
                print e

    def price_mean(self):
        for data, stock in self.data:
            try:
                data["5d"] = data["close_price"].rolling(window=5, center=False).mean()
                data["10d"] = data["close_price"].rolling(window=10, center=False).mean()
                data["20d"] = data["close_price"].rolling(window=20, center=False).mean()
                data["60d"] = data["close_price"].rolling(window=60, center=False).mean()
                data["120d"] = data["close_price"].rolling(window=120, center=False).mean()

                yield data, stock

            except Exception, e:
                print e

    def volume_mean(self):
        for data, stock in self.data:
            try:
                data['5dv'] = data['volume'].rolling(window=5, center=False).mean()
                data['10dv'] = data['volume'].rolling(window=10, center=False).mean()
                data['5dvp'] = [x * 1.5 for x in data['5dv']]
                yield data, stock

            except Exception, e:
                print e

    def macd_cal(self):
        for data, stock in self.data:
            try:
                data['short_ema'] = pd.ewma(data['close_price'], span=12, adjust=False)
                data['long_ema'] = pd.ewma(data['close_price'], span=26, adjust=False)
                data['diff'] = data['short_ema'] - data['long_ema']
                data['dea'] = pd.ewma(data['diff'], span=9, adjust=False)
                data['macd'] = 2 * (data['diff'] - data['dea'])
                yield data, stock

            except Exception, e:
                print e
