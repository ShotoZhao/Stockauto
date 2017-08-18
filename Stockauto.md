## About this mini project

* it is time consuming and arduous to find out an expected stock from China A stock market containing nearly 3000 stocks. 

  this mini project can choose expected stocks automaticlly depending on criterion you've settled.

### Dependencies

* this project denpends on [FuTu API](https://github.com/szmile2008/FTPlugin) from which you can get stock data.
* you need to install MongoDB where store the stock data and send the data.
* this project is based on python 2.7. unknown error may appear in python 3.x.

### Usage

1. after you've set up FuTu API, there is a **sample.py** in the package. i've modified it so that the stock data can stored in MongoDB. Using the function **_example_hist_kline()** in this file to get the stock data and the data will be stored in Mongodb because there is a function importing from **stock_mongo.py**. for more info about the usage of this API, please refer the API directions.
2. **stock_index.py**  and **stock_list2** are stock code lists of A stock market. the first is used in FUTU API, the second is used in other function of this project e.g. the function of getting data from Mongodb.
3. **stock_data_treatment.py**  can calculate average price, average volume, macd and so on. you can add some functions in it according to your requirements. *but in this version, i integrate this function into **stock_pands.py**.*
4. **stock_pandas.py** is the primary file within which you can choose the wanted stock from 3000 stocks automatically. and the data_treatment function is also integrated into this file.  there is only one sample strategy about macd saying that if diff cross over dea, i put it into macd_up list otherwise macd_down list. you can write your strategies in this file.
5. **stockcandle.py** is used to plot k-line by day.  just for fun. enjoy it if you like.
6. replace **sample.py** and copy the files into FUTU API folder.

### Others

* this project is a basic version, so you can modify it as you wish. For instance, you can calculate more features such as RSI, Boll band and so on.
* any question is welcome. Please write a comment or contact me.
* **if you get some help from this project, please Star it on the top-right corner. Thank you.**

