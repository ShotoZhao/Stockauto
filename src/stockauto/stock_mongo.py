# coding:utf-8

from pymongo import *
from stock_list2 import INDEX_SYMBOL
import pandas as pd


class StockToMongo(object):
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection

    def kline_tomongo(self, stockdata):
        client = MongoClient(self.host, self.port)
        db = client[self.db]
        collect = db[self.collection]
        for row in stockdata.iterrows():
            ss = row[1]['code'].split('.')
            stockcode = ''.join(ss)
            dat = row[1]['time_key']
            date = dat.split(' ')[0]
            open_price = row[1]['open']
            close_price = row[1]['close']
            high_price = row[1]['high']
            low_price = row[1]['low']
            volume = float(row[1]['volume'])
            turnover = row[1]['turnover']
            collect.update_one({"_id": stockcode}, {"$set": {("%s.%s") % (stockcode, date):
                {
                    "date": date,
                    "open_price": open_price,
                    "close_price": close_price,
                    "high_price": high_price,
                    "low_price": low_price,
                    "volume": volume,
                    "turnover": turnover
                }}}, True)

    def basic_tomongo(self, basic_data):
        client = MongoClient(self.host, self.port)
        db = client[self.db]
        collect = db[self.collection]
        for row in basic_data.iterrows():
            code = row[1]['code']
            name = row[1]['name']
            lot_size = row[1]['lot_size']
            stock_type = row[1]['stock_type']
            stock_child_type = row[1]["stock_child_type"]
            owner_stock_code = row[1]['owner_stock_code']
            listing_date = row[1]['listing_date']
            collect.update_one({"_id": code}, {"$set": {
                "code": code,
                "name": name,
                "lot_size": lot_size,
                "stock_type": stock_type,
                "stock_child_type": stock_child_type,
                "owner_stock_code": owner_stock_code,
                "listing_date": listing_date
            }}, True)



class DatafromMongo(object):
    def __init__(self,host, port, dbs, collection, stockcode_list=[]):
        self.host = host
        self.port = port
        self.dbs = dbs
        self.collection = collection
        self.stockcode_list = stockcode_list

    def get_original_data(self):
        '''
        :param dbs: db of data from
        :param collection: colletion of the db
        :return: yield dataframe and stockcode per stock
        '''

        conn = MongoClient(self.host, self.port)
        db = conn[self.dbs]
        coll = db[self.collection]

        for stock in self.stockcode_list:
            try:
                cursor = coll.find({'_id': stock})
                data = pd.DataFrame(list(cursor))
                data = data[stock][0]
                data = pd.DataFrame(data)
                data = data.T
                yield data, stock  # 逐个返回dataframe和stockcode
            except Exception, e:
                print e


