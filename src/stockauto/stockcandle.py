#!/usr/bin/env python
# encoding: utf-8


"""
@author: Shoto_Sakura
@name: stockcandle 
@contact: micalun@gmail.com
@time: 2017/8/7 8:35
"""
import stock_pandas as sp
import numpy as np
import pandas as pd
import matplotlib.finance as mpf
import matplotlib.pyplot as plt
from pymongo import MongoClient
import datetime
from matplotlib.pylab import date2num, num2date
import matplotlib.dates
from matplotlib import transforms


def draw_candle(dataplus, startdate ,enddate):

    for data, stock in dataplus:
        p1 = data.loc[startdate:enddate]

        del p1['date']
        candle_data = p1[['open_price', 'high_price', 'low_price', 'close_price', 'volume']]
        data_list = []
        data_list2 = []
        # print candle_data
        for dates, row in candle_data.iterrows():

            dates =datetime.datetime.strptime(dates, "%Y-%m-%d").date()
            t = date2num(dates)
            openn, high, low, close, volume = row[:5]
            data1 = (t, openn, high, low, close)
            data2 = (t, openn, high, low, close, volume)
            data_list.append(data1)
            data_list2.append(data2)


        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.title(stock)

        ax.set_ylabel('Price', size=20)

        # fig,ax=plt.subplots()
        # fig.subplots_adjust(bottom=0.2)
        # ax.xaxis_date()
        # ax.xaxis.set_major_formatter(month_formatter)
        # plt.xticks(rotation=45)
        # plt.yticks()
        # plt.title("stockname")
        # plt.xlabel("date")
        # plt.ylabel("price")

        # 画出k线
        mpf.candlestick_ohlc(ax, data_list, colorup='r', colordown='g', width=0.8)
        # mpf.candlestick_ohlc(p1.loc['2016-01-04':'2016-08-07',:], otherseries = "20d")
        # fig.autofmt_xdate()
        # fig.tight_layout()

        pad = 0.5
        yl = ax.get_ylim()
        ax.set_ylim(yl[0] - (yl[1] - yl[0]) * pad, yl[1])

        ax2 = ax.twinx()

        ax2.set_position(transforms.Bbox([[0.125, 0.1], [0.9, 0.32]]))
        dates = [x[0] for x in data_list2]
        dates = np.asarray(dates)
        volume = [x[5] for x in data_list2]
        volume = np.asarray(volume)
        # fig2,axx=plt.subplots()
        # axx.bar(dates,volume)

        # 画出均线
        ax.plot(dates, p1["5d"], 'g-', linewidth=2)
        ax.plot(dates, p1["10d"], 'b-', linewidth=2)
        ax.plot(dates, p1["20d"], 'r-', linewidth=2)
        ax.plot(dates, p1["60d"], 'c-', linewidth=2)
        ax.plot(dates, p1["120d"], 'k-', linewidth=2)

        # 画出量柱，判断涨跌
        position = np.asarray(p1['open_price'] - p1['close_price'])
        # neg=p1['open_price']-p1['close_price']
        ax2.bar(dates[position > 0], volume[position > 0], color='g', width=0.8, align='center')
        ax2.bar(dates[position < 0], volume[position < 0], color='r', width=0.8, align='center')
        ax2.plot(dates, p1["5dvp"], "g-", linewidth = 1.5,label="5dp_volume")
        ax2.plot(dates, p1["10dvp"], "r-", linewidth = 1.5, label = "10dp_volume")
        plt.legend()

        # axx.bar(dates[pos<0],volume[pos<0],color='g',width=0.8,align='center')
        # axx.bar(dates[pos>0],volume[pos>0],color='r',width=0.8,align='center')

        ax2.set_xlim(min(dates), max(dates))
        # # the y-ticks for the bar were too dense, keep only every third one
        yticks = ax2.get_yticks()
        ax2.set_yticks(yticks[::3])

        ax2.yaxis.set_label_position("right")
        ax2.set_ylabel('Volume', size=20)

        #
        # alldays=matplotlib.dates.DayLocator()
        weekdayLo = matplotlib.dates.WeekdayLocator()
        #
        # ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(weekdayLo)
        # plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        ax.grid(True)
        # mpf.volume_overlay3(ax, data_list2, colorup='r', colordown='g', width=1, alpha=1.0)
        # plt.hold(True)
        xt = ax.get_xticks()
        new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
        ax.set_xticklabels(new_xticks, rotation=45, horizontalalignment='right')

        plt.savefig(stock, bbox_inches="tight")
        plt.show()


if __name__ == "__main__":
    data = sp.data_from_mongo("test", "stock_price", stockcode_list=["SH600000","SZ000687", ])
    dataplus = sp.data_treatment(data)
    draw_candle(dataplus, "2017-07-01","2017-08-14")