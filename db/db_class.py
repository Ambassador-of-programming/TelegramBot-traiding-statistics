import os
import psycopg2
import requests                    # for "get" request to API
import json                        # parse json into a list
import pandas as pd                # working with data frames
import datetime as dt              # working with dates
import plotly.graph_objects as go

from config.db import *


class General_db:
    def search_id():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT vendor_id FROM trigger_table 
                    ORDER BY date ASC LIMIT 1
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_closes():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT closes FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_coin():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT symbol FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_open():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT opens FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_order_id():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT order_id FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_profit():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT profit FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_strategy():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT strategy FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_times():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT date FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()
                
    def db_starttransactTime():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT start_transactTime FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    def db_endtransactTime():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT end_transactTime FROM traidings WHERE id={General_db.search_id()}
                    """
                )
                return list(cursor.fetchone())[0]
        finally:
            if connection:
                connection.close()

    
    def Candlestick():
        # Тикер и таймфрейм
        TICKER = f"{General_db.db_coin()}"
        INTERVAL = "1s"

        # Бэктест начало/конец дата
        START = dt.datetime.fromtimestamp(General_db.db_starttransactTime() / 1000.0)
        END   = dt.datetime.fromtimestamp(General_db.db_endtransactTime() / 1000.0)

        # Получаем данные от Binance
        def get_binance_bars(symbol, interval, startTime, endTime):
                url = "https://api.binance.com/api/v3/klines"
                startTime = str(int(startTime.timestamp() * 1000))
                endTime = str(int(endTime.timestamp() * 1000))
                limit = '1000'
                req_params = {"symbol" : symbol, 'interval' : interval, 'startTime' : startTime, 'endTime' : endTime, 'limit' : limit}
                df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))
                if (len(df.index) == 0):
                    return None
                df = df.iloc[:, 0:5]
                df.columns = ['datetime', 'Open', 'High', 'Low', 'Close']
                df.Open      = df.Open.astype("float")
                df.High      = df.High.astype("float")
                df.Low       = df.Low.astype("float")
                df.Close     = df.Close.astype("float")
                df['adj_close'] = df['Close']
                df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]
                return df

        def pd_datas(TICKER, INTERVAL, START, END):
            df_list = []
            while True:
                new_df = get_binance_bars(TICKER, INTERVAL, START, END)
                if new_df is None:
                    break
                df_list.append(new_df)
                START = max(new_df.index) + dt.timedelta(0, 1)
            return pd.concat(df_list)

        df = pd_datas(TICKER, INTERVAL, START, END)

        fig = go.Figure(data=[go.Candlestick(x=df['datetime'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])

        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.write_image(f"image/{General_db.search_id()}.png", scale=5)
        return 'succes'

    def db_remove_photo():
        return os.remove(f"image/{General_db.search_id()}.png")

    def delete_id():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    delete from trigger_table
                    where vendor_id={General_db.search_id()}
                    """
                )
        finally:
            if connection:
                connection.close()