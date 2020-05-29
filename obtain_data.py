#!/usr/bin/env python
# coding:utf8
"""
从bitmex获取k线数据
"""
import datetime
import time

import requests

from gossip import evaluate_model
from mock_exchange import MockExchange
from table_store import save_predict


def get_data(start, end, bin_size):
    """

    :param start:
    :param end:
    :param bin_size:
    :return:
    """
    try:
        url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize={0}&partial=false&symbol=XBTUSD&count=1000&reverse=false&startTime={1}&endTime={2}".format(
            bin_size, start, end)
        header = {
            "Accept": "application/json"
        }
        response = requests.get(url, headers=header)
        return response.json()
    except Exception as e:
        print(e)
    return []


def save_data(datas):
    """

    :param datas:
    :return:
    """
    with open('dataset/xbtusd_1h.csv', 'a') as f:
        for m in datas:
            f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(m['timestamp'],
                                                                 m['open'],
                                                                 m['high'],
                                                                 m['close'],
                                                                 m['low'],
                                                                 m['volume'],
                                                                 m['turnover']
                                                                 ))


def get_period_data():
    """

    :return:
    """
    t = datetime.datetime(2020, 5, 22, 1, 0, 0)
    now = datetime.datetime.now()
    n = 1
    while t <= now:
        start_str = t.strftime("%Y-%m-%d %H:%M:%S")
        end_str = (t + datetime.timedelta(days=n)).strftime("%Y-%m-%d %H:%M:%S")
        print(start_str)
        datas = get_data(start_str, end_str, '1h')
        save_data(datas)
        t = t + datetime.timedelta(days=n)
        # time.sleep(2)


def hour_second():
    """

    :return:
    """
    count = 3600 - time.time() % 3600 + 2.0
    print("sleep {0} second".format(count))
    time.sleep(count)


def get_last_data():
    """

    :return:
    """
    now = datetime.datetime.now()
    start = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:00:00")
    end = now.strftime("%Y-%m-%d %H:%M:%S")
    data = get_data(start, end, '1h')
    day_dict = {}
    with open('dataset/xbtusd_1h.csv') as f:
        for line in f:
            values = line.split('\t')
            day_dict[values[0]] = 1
    s_data = [m for m in data if m['timestamp'] not in day_dict]
    save_data(s_data)
    if s_data:
        hold_pct = evaluate_model("model.30.best", "xbtusd_1h")
        with open("predict_result.txt", 'a') as f:
            f.write("{0}\t{1}\n".format(now.strftime("%Y-%m-%d %H:%M:%S"), hold_pct))
        m = MockExchange()
        m.trade(hold_pct[0])
        save_predict(int(now.strftime("%Y%m%d%H")), "btc", hold_pct)


def run_period():
    """

    :return:
    """
    while True:
        print(datetime.datetime.now().strftime("%H:%M:%S"))
        try:
            get_last_data()
        except Exception as e:
            print(e)
        # hour_second()
        time.sleep(60)


if __name__ == '__main__':
    # get_period_data()
    # get_last_data()
    run_period()
