# coding:utf-8

from stock_list2 import INDEX_SYMBOL
import pandas as pd
from pymongo import MongoClient
import numpy as np





def data_from_mongo(dbs, collection, stockcode_list=[]):
    '''
    :param dbs: db of data from
    :param collection: colletion of the db
    :return: yield dataframe and stockcode per stock
    '''

    conn = MongoClient('localhost', 27017)
    db = conn[dbs]
    coll = db[collection]

    for stock in stockcode_list:
        try:
            cursor = coll.find({'_id': stock})
            data = pd.DataFrame(list(cursor))
            data = data[stock][0]
            data = pd.DataFrame(data)
            data = data.T
            yield data, stock  # 逐个返回dataframe和stockcode
        except Exception, e:
            print e
            continue


def data_treatment(data):
    '''
    :param data: original data from mongodb
    :return: dataplus
    '''

    for data, stock in data:
        try:
            data['rise'] = data['close_price'].pct_change()  # 股价实际上涨幅度
            data['krise'] = (data['close_price'] - data['open_price']) / data['open_price']  # k线上涨幅度

            fir = ((data['krise'] > data['rise']) & (data['rise'] > 0))  # 股价上涨时选择k线和实际上涨幅度大值
            sec = (data['krise'] < data['rise']) & (data['rise'] < 0)  # 股价下跌时选择k线和实际下跌幅度大值

            chose_rise = fir | sec
            kline = data['krise']

            data['trise'] = kline[chose_rise]
            data.fillna({'trise': data['rise']}, inplace=True)

            # 均线
            data["5d"] = data["close_price"].rolling(window=5, center=False).mean()
            data["10d"] = data["close_price"].rolling(window=10, center=False).mean()
            data["20d"] = data["close_price"].rolling(window=20, center=False).mean()
            data["60d"] = data["close_price"].rolling(window=60, center=False).mean()
            data["120d"] = data["close_price"].rolling(window=120, center=False).mean()

            # 均量
            data['5dv'] = data['volume'].rolling(window=5, center=False).mean()
            data['10dv'] = data['volume'].rolling(window=10, center=False).mean()
            data['5dvp'] = [x * 1.5 for x in data['5dv']]
            data['10dvp'] = [x * 1.5 for x in data['10dv']]

            # macd
            data['short_ema'] = pd.ewma(data['close_price'], span=12, adjust=False)
            data['long_ema'] = pd.ewma(data['close_price'], span=26, adjust=False)
            data['diff'] = data['short_ema'] - data['long_ema']
            data['dea'] = pd.ewma(data['diff'], span=9, adjust=False)
            data['macd'] = 2 * (data['diff'] - data['dea'])

            # print data.tail()
            # break

            yield data, stock
        except Exception, e:
            print e
            continue


def macd_criterion(data):
    data1 = data[-1:]
    data2 = data[-2:-1]
    a = data1['macd'][0] > 0  # 判断最后一天macd大小
    b = data2['macd'][0] < 0  # 判断倒数第二天macd大小
    if a and b:
        return True
    elif not a and not b:
        return False
    else:
        pass





def forloop(dataplus): 
	'''
	处理dataplus生成器，在for中可以处理多个creterion，并返回相应stockcode list
	'''
    macd_up = []
    macd_down = []

    for data, stock in dataplus:
        macdcri = macd_criterion(data)
        priceloc = price_locate(data, 100, 0.3)

        if macdcri == True:
            macd_up.append(stock)
        elif macdcri == False:
            macd_down.append(stock)

    return {"macd_up": macd_up, "macd_down": macd_down}


if __name__ == "__main__":

    data = data_from_mongo("test", "stock_price", INDEX_SYMBOL)
    dataplus = data_treatment(data)
    stocklist = forloop(dataplus)

    macd_up = stocklist["macd_up"]
    macd_down = stocklist["macd_down"]
    print macd_up

